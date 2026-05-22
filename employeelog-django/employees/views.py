from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import Company, Employee, DeletedEmployee, DynamicField, EmployeeDynamicData, WorkspaceVerification, OTPVerification, EmployeeProfile, Conversation, Message, Notification
from .serializers import EmployeeSerializer, DeletedEmployeeSerializer, CompanySerializer, DynamicFieldSerializer, CoworkerSerializer, ConversationSerializer, MessageSerializer, NotificationSerializer
from .permissions import IsCompanyAdmin, IsCompanyAdminOrReadOnly, IsCompanyAdminOrManagerOrReadOnly

from .services import (
    send_verification_otp_email,
    send_password_reset_email,
    send_verification_email,
    send_admin_setup_email,
    send_login_notification_email,
    send_suspicious_login_email,
    send_employee_added_email,
    send_employee_updated_email,
    send_employee_deleted_email
)

import string
import random

# Helper to generate standard JWT tokens programmatically
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['role'] = user.role
    refresh['company_name'] = user.company.company_name if user.company else None
    refresh['username'] = user.email.split('@')[0]
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# ---------------- COMPANY VIEW ----------------
class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def get_queryset(self):
        return Company.objects.filter(id=self.request.user.company_id)

# ---------------- EMPLOYEE VIEW ----------------
class EmployeeView(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdminOrManagerOrReadOnly]

    def get_queryset(self):
        return Employee.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        # Admin creates employee within their company
        employee = serializer.save(company=self.request.user.company)
        
        # Save dynamic data if provided
        dynamic_data = self.request.data.get('dynamic_data', {})
        for field_id, value in dynamic_data.items():
            try:
                field = DynamicField.objects.get(id=field_id, company=self.request.user.company)
                EmployeeDynamicData.objects.create(
                    employee=employee,
                    dynamic_field=field,
                    value=str(value)
                )
            except DynamicField.DoesNotExist:
                pass
        
        # Generate secure random temporary password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not User.objects.filter(email=employee.email).exists():
            User.objects.create_user(
                email=employee.email,
                password=password,
                role='employee',
                company=self.request.user.company
            )
            
        # Trigger credential delivery email alert to new employee
        send_employee_added_email(
            recipient_email=employee.email,
            employee_name=employee.name,
            password=password,
            company_name=self.request.user.company.company_name
        )

    def perform_update(self, serializer):
        # Update core employee details
        employee = serializer.save()
        
        # Update dynamic fields if provided
        dynamic_data = self.request.data.get('dynamic_data', {})
        for field_id, value in dynamic_data.items():
            try:
                field = DynamicField.objects.get(id=field_id, company=self.request.user.company)
                EmployeeDynamicData.objects.update_or_create(
                    employee=employee,
                    dynamic_field=field,
                    defaults={'value': str(value)}
                )
            except DynamicField.DoesNotExist:
                pass
                
        # Trigger updated email alert to admin
        send_employee_updated_email(
            admin_email=self.request.user.email,
            employee=employee,
            company_name=self.request.user.company.company_name
        )

    def perform_destroy(self, instance):
        # Copy to soft-deleted archive before actual deletion
        deleted_employee = DeletedEmployee.objects.create(
            company=instance.company,
            name=instance.name,
            email=instance.email,
            department=instance.department,
            designation=instance.designation,
            salary=instance.salary,
            phone=instance.phone
        )
        # Delete user account associated with employee
        User.objects.filter(email=instance.email).delete()
        
        # Trigger deleted email alert to admin
        send_employee_deleted_email(
            admin_email=self.request.user.email,
            deleted_employee=deleted_employee,
            company_name=self.request.user.company.company_name
        )
        instance.delete()

# ---------------- DELETED EMPLOYEE VIEW ----------------
class DeletedEmployeeView(viewsets.ModelViewSet):
    serializer_class = DeletedEmployeeSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def get_queryset(self):
        return DeletedEmployee.objects.filter(company=self.request.user.company)

# ---------------- DYNAMIC FIELDS VIEW ----------------
class DynamicFieldView(viewsets.ModelViewSet):
    serializer_class = DynamicFieldSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdminOrReadOnly]

    def get_queryset(self):
        return DynamicField.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

# ---------------- JWT TOKEN WITH ROLE & COMPANY ----------------
class MyTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['company_name'] = user.company.company_name if user.company else None
        token['username'] = user.email.split('@')[0]
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['role'] = self.user.role
        data['company_name'] = self.user.company.company_name if self.user.company else None
        data['username'] = self.user.email.split('@')[0]
        
        # Trigger login security alert email notification!
        request = self.context.get('request')
        user_agent = "Unknown Device"
        if request:
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
            
        send_login_notification_email(
            recipient_email=self.user.email,
            company_name=data['company_name'] or 'Corporate',
            role=self.user.role,
            user_agent=user_agent
        )
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenSerializer

# ---------------- EMAIL-FIRST OTP VERIFICATION SYSTEM ----------------

@api_view(['POST'])
@permission_classes([AllowAny])
def request_otp(request):
    """
    Email-First login verification. Sends OTP to company email based on purpose (onboard, login, reset).
    """
    email = request.data.get('email')
    purpose = request.data.get('purpose', 'login') # onboard, login, reset
    
    if not email:
        return Response({"error": "Corporate email address is required."}, status=status.HTTP_400_BAD_REQUEST)
        
    email = email.lower().strip()
    user_exists = User.objects.filter(email=email).exists()
    
    # 1. Onboarding check
    if purpose == 'onboard' and user_exists:
        return Response({"error": "A workspace with this email address already exists. Please login."}, status=status.HTTP_400_BAD_REQUEST)
        
    # 2. Login check
    if purpose == 'login' and not user_exists:
        return Response({"error": "User account does not exist. Please contact your system administrator or onboard your company first."}, status=status.HTTP_400_BAD_REQUEST)
        
    # 3. Password reset check
    if purpose == 'reset' and not user_exists:
        return Response({"error": "User account with this email address does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
    # Generate 6-digit numeric OTP code
    otp = ''.join(random.choices(string.digits, k=6))
    
    # Save/Update in OTPVerification
    OTPVerification.objects.update_or_create(
        email=email,
        defaults={'otp': otp, 'purpose': purpose}
    )
    
    # Log to terminal console for quick local debugging
    print(f"\n======================================================\n[AUTH OTP] Generated OTP: {otp}\n[AUTH OTP] Email: {email}\n[AUTH OTP] Purpose: {purpose}\n======================================================\n")
    
    # Send appropriate email template with exception bubble-up for debugging
    try:
        if purpose == 'reset':
            send_password_reset_email(email, otp)
        else:
            send_verification_otp_email(email, otp)
    except Exception as e:
        # Delete generated OTP verification since dispatch failed
        OTPVerification.objects.filter(email=email, purpose=purpose).delete()
        return Response({
            "error": f"Failed to dispatch verification email via SMTP server. Please verify your Django settings.py and host credentials. SMTP Error Details: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response({
        "message": "A 6-digit verification code has been successfully dispatched.",
        "email": email
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    Verifies 6-digit OTP code. If login purpose, returns JWT tokens directly.
    If onboarding purpose, auto-initializes the workspace and admin.
    If reset purpose, resets user password immediately.
    """
    email = request.data.get('email')
    otp = request.data.get('otp')
    purpose = request.data.get('purpose', 'login')
    new_password = request.data.get('new_password') # Optional, for reset purpose
    
    if not email or not otp:
        return Response({"error": "Email and verification code are required."}, status=status.HTTP_400_BAD_REQUEST)
        
    email = email.lower().strip()
    print(f"\n[AUTH OTP] Verifying OTP request - Email: {email}, OTP: {otp}, Purpose: {purpose}")
    
    try:
        otp_record = OTPVerification.objects.get(email=email, otp=otp, purpose=purpose)
    except OTPVerification.DoesNotExist:
        # Print actual database records to help diagnose mismatched inputs
        all_otps = list(OTPVerification.objects.all().values('email', 'otp', 'purpose'))
        print(f"[AUTH OTP] Failed to match OTP. Stored OTP records: {all_otps}")
        return Response({"error": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)
        
    # Expiration check (5 minutes)
    if timezone.now() - otp_record.created_at > timedelta(minutes=5):
        print(f"[AUTH OTP] OTP code has expired. Time difference: {timezone.now() - otp_record.created_at}")
        otp_record.delete()
        return Response({"error": "Verification code has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)
        
    # Clean up OTP record immediately to prevent reuse
    otp_record.delete()
    print("[AUTH OTP] Verification successful! Purged OTP record from DB.")

    
    # --- ONBOARDING FLOW ---
    if purpose == 'onboard':
        domain = email.split('@')[-1]
        company_name = domain.split('.')[0].capitalize()
        
        # Create Company Workspace
        company = Company.objects.create(
            company_name=company_name,
            company_email=email
        )
        
        # Generate temporary password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # Create Admin
        admin_user = User.objects.create_user(
            email=email,
            password=password,
            role='admin',
            company=company
        )
        
        # Send credentials Setup Welcome Email
        send_admin_setup_email(email, company.company_name, password)
        
        return Response({
            "message": "Company workspace and Admin account initialized successfully.",
            "company_name": company.company_name,
            "admin_email": email,
            "admin_password": password
        }, status=status.HTTP_201_CREATED)
        
    # --- LOGIN FLOW ---
    elif purpose == 'login':
        user = User.objects.get(email=email)
        tokens = get_tokens_for_user(user)
        
        # User agent context for email alert
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
        
        # Suspicious Login Attempt Detection
        # Triggers a critical warning if headless tools, python scripts, or curl are used
        suspicious_keywords = ['python', 'curl', 'headless', 'postman', 'scrappy', 'wget']
        is_suspicious = any(kw in user_agent.lower() for kw in suspicious_keywords)
        
        if is_suspicious:
            send_suspicious_login_email(
                recipient_email=email,
                user_agent=user_agent,
                timestamp=timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        else:
            send_login_notification_email(
                recipient_email=email,
                company_name=user.company.company_name if user.company else 'Corporate',
                role=user.role,
                user_agent=user_agent
            )
            
        return Response({
            "access": tokens['access'],
            "refresh": tokens['refresh'],
            "role": user.role,
            "company_name": user.company.company_name if user.company else None,
            "username": user.email.split('@')[0]
        }, status=status.HTTP_200_OK)
        
    # --- PASSWORD RESET FLOW ---
    elif purpose == 'reset':
        if not new_password:
            return Response({"error": "A new password is required for reset verification."}, status=status.HTTP_400_BAD_REQUEST)
            
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        
        return Response({
            "message": "Your password has been successfully reset. Please log in using your new credentials."
        }, status=status.HTTP_200_OK)
        
    return Response({"error": "Unknown verification request."}, status=status.HTTP_400_BAD_REQUEST)

# Legacy onboarding fallback view
@api_view(['POST'])
@permission_classes([AllowAny])
def onboard_company(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({"error": "A user with this email already exists. Please login."}, status=status.HTTP_400_BAD_REQUEST)
    code = ''.join(random.choices(string.digits, k=6))
    WorkspaceVerification.objects.update_or_create(email=email, defaults={'code': code})
    send_verification_email(email, code)
    return Response({"message": "Verification code has been sent.", "email": email}, status=status.HTTP_200_OK)

# Legacy onboarding verification fallback view
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_onboard(request):
    email = request.data.get('email')
    code = request.data.get('code')
    if not email or not code:
        return Response({"error": "Email and verification code are required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        verification = WorkspaceVerification.objects.get(email=email, code=code)
    except WorkspaceVerification.DoesNotExist:
        return Response({"error": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)
    domain = email.split('@')[-1]
    company_name = domain.split('.')[0].capitalize()
    company = Company.objects.create(company_name=company_name, company_email=email)
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    admin_user = User.objects.create_user(email=email, password=password, role='admin', company=company)
    send_admin_setup_email(email, company.company_name, password)
    verification.delete()
    return Response({
        "message": "Company workspace created.",
        "company_name": company.company_name,
        "admin_email": admin_user.email,
        "admin_password": password
    }, status=status.HTTP_201_CREATED)


# ---------------- COLLABORATION & MESSAGING VIEWS ----------------

from rest_framework.decorators import action
from django.db.models import Q


class CoworkerListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to list coworkers in the same company tenant.
    """
    serializer_class = CoworkerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Strict company data isolation: only active coworkers in same company!
        return User.objects.filter(company=self.request.user.company, is_active=True).exclude(id=self.request.user.id)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list and manage conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Strict company data isolation: only conversations inside user's company where user is participant
        return Conversation.objects.filter(
            company=self.request.user.company,
            participants=self.request.user
        ).order_by('-updated_at')

    def create(self, request, *args, **kwargs):
        recipient_id = request.data.get('recipient_id')
        if not recipient_id:
            return Response({"error": "recipient_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipient = User.objects.get(id=recipient_id, company=request.user.company)
        except User.DoesNotExist:
            return Response({"error": "Recipient coworker does not exist in your company."}, status=status.HTTP_404_NOT_FOUND)

        # Prevent DMs with oneself
        if recipient == request.user:
            return Response({"error": "You cannot start a conversation with yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Find existing DM conversation
        conversation = Conversation.objects.filter(
            company=request.user.company,
            participants=request.user
        ).filter(participants=recipient).first()

        if not conversation:
            # Create a new conversation
            conversation = Conversation.objects.create(company=request.user.company)
            conversation.participants.add(request.user, recipient)
            conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage messages within a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        if not conversation_id:
            return Message.objects.none()

        # Strict multi-tenant security verification
        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                company=self.request.user.company,
                participants=self.request.user
            )
        except Conversation.DoesNotExist:
            return Message.objects.none()

        # Mark incoming messages as read when fetched!
        conversation.messages.exclude(sender=self.request.user).update(is_seen=True)

        return conversation.messages.order_by('created_at')

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                company=self.request.user.company,
                participants=self.request.user
            )
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation does not exist or you are not authorized.")

        # Save message
        message = serializer.save(sender=self.request.user, conversation=conversation)
        
        # Touch conversation to update updated_at timestamp
        conversation.save()

        # Generate notifications for all other participants in the conversation
        other_participants = conversation.participants.exclude(id=self.request.user.id)
        for participant in other_participants:
            # Get sender name
            emp = Employee.objects.filter(email=self.request.user.email).first()
            sender_name = emp.name if emp else self.request.user.email.split('@')[0].capitalize()

            Notification.objects.create(
                company=self.request.user.company,
                recipient=participant,
                message=message,
                notification_type='message',
                title=f"New Message from {sender_name}",
                description=message.content[:100]
            )

    def destroy(self, request, *args, **kwargs):
        # Allow users to delete their own messages
        instance = self.get_object()
        if instance.sender != request.user:
            return Response({"error": "You are not authorized to delete this message."}, status=status.HTTP_403_FORBIDDEN)
        
        # Delete any notifications related to this message
        Notification.objects.filter(message=instance).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnnouncementViewSet(viewsets.ViewSet):
    """
    API endpoint for admin announcements.
    """
    permission_classes = [IsAuthenticated]

    def create(self, request):
        # Strict role-based messaging check: only admins can post announcements!
        if request.user.role != 'admin':
            return Response({"error": "Only company administrators can dispatch workspace announcements."}, status=status.HTTP_403_FORBIDDEN)

        title = request.data.get('title')
        description = request.data.get('description')

        if not title or not description:
            return Response({"error": "Title and description are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Broadcast notification to EVERY user in the company!
        recipients = User.objects.filter(company=request.user.company)
        for recipient in recipients:
            Notification.objects.create(
                company=request.user.company,
                recipient=recipient,
                notification_type='announcement',
                title=f"📢 {title}",
                description=description
            )

        return Response({"message": f"Announcement successfully broadcast to {recipients.count()} workspace members."}, status=status.HTTP_201_CREATED)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list and manage notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Strict company level filtering
        return Notification.objects.filter(
            company=self.request.user.company,
            recipient=self.request.user
        ).order_by('-created_at')

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "notification marked as read"})

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({"status": "all notifications marked as read"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def presence_heartbeat(request):
    """
    API endpoint triggered by frontend client to keep user online status alive.
    """
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
    profile.is_online = True
    profile.save() # Saves and updates last_seen auto-now
    return Response({"status": "presence updated", "is_online": True})


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    API endpoint to retrieve or update the logged-in user's profile details (such as profile_picture URL).
    """
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
    
    if request.method in ['PUT', 'PATCH']:
        profile_picture = request.data.get('profile_picture')
        custom_status = request.data.get('custom_status')
        status_emoji = request.data.get('status_emoji')
        
        updated = False
        if profile_picture is not None:
            profile.profile_picture = profile_picture
            updated = True
        if custom_status is not None:
            profile.custom_status = custom_status
            updated = True
        if status_emoji is not None:
            profile.status_emoji = status_emoji
            updated = True
            
        if updated:
            profile.save()
            return Response({
                "status": "profile updated successfully",
                "profile_picture": profile.profile_picture,
                "custom_status": profile.custom_status,
                "status_emoji": profile.status_emoji
            })
        return Response({"error": "At least one profile parameter is required for update."}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({
        "email": request.user.email,
        "role": request.user.role,
        "profile_picture": profile.profile_picture,
        "custom_status": profile.custom_status,
        "status_emoji": profile.status_emoji
    })