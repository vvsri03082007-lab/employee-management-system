from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Company, Employee, DeletedEmployee, DynamicField, EmployeeDynamicData,
    EmployeeProfile, Conversation, Message, Notification
)

User = get_user_model()

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicField
        fields = '__all__'
        read_only_fields = ['company']

class EmployeeDynamicDataSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='dynamic_field.field_name', read_only=True)
    
    class Meta:
        model = EmployeeDynamicData
        fields = ['id', 'dynamic_field', 'field_name', 'value']

class EmployeeSerializer(serializers.ModelSerializer):
    dynamic_data = EmployeeDynamicDataSerializer(many=True, read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['company']

class DeletedEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeletedEmployee
        fields = '__all__'
        read_only_fields = ['company']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'company']


# ---------------- COLLABORATION SERIALIZERS ----------------

class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ['profile_picture', 'is_online', 'last_seen', 'custom_status', 'status_emoji']


class CoworkerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    designation = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    last_seen = serializers.SerializerMethodField()
    custom_status = serializers.SerializerMethodField()
    status_emoji = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'name', 'department', 'designation', 'profile_picture', 'is_online', 'last_seen', 'custom_status', 'status_emoji']

    def get_name(self, obj):
        emp = Employee.objects.filter(email=obj.email).first()
        if emp:
            return emp.name
        return obj.email.split('@')[0].capitalize() if obj.email else "User"

    def get_department(self, obj):
        emp = Employee.objects.filter(email=obj.email).first()
        if emp:
            return emp.department
        return "Management" if obj.role == 'admin' else "Unassigned"

    def get_designation(self, obj):
        emp = Employee.objects.filter(email=obj.email).first()
        if emp:
            return emp.designation
        return "Administrator" if obj.role == 'admin' else "Staff"

    def get_profile_picture(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return obj.profile.profile_picture
        return None

    def get_is_online(self, obj):
        if not obj.is_active:
            return False
        if hasattr(obj, 'profile'):
            # Consider a coworker online if is_online is True AND they sent a heartbeat within the last 30 seconds
            if obj.profile.is_online and obj.profile.last_seen:
                from django.utils import timezone
                from datetime import timedelta
                is_active_now = timezone.now() - obj.profile.last_seen < timedelta(seconds=30)
                # Auto-update status if they timed out
                if not is_active_now and obj.profile.is_online:
                    obj.profile.is_online = False
                    obj.profile.save(update_fields=['is_online'])
                return is_active_now
            return obj.profile.is_online
        return False

    def get_last_seen(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.last_seen
        return None

    def get_custom_status(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.custom_status
        return None

    def get_status_emoji(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.status_emoji
        return None


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    sender_role = serializers.CharField(source='sender.role', read_only=True)
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_email', 'sender_role', 'sender_name', 'content', 'is_seen', 'created_at']
        read_only_fields = ['sender', 'conversation']

    def get_sender_name(self, obj):
        emp = Employee.objects.filter(email=obj.sender.email).first()
        if emp:
            return emp.name
        return obj.sender.email.split('@')[0].capitalize()


class ConversationSerializer(serializers.ModelSerializer):
    participants = CoworkerSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'company', 'participants', 'last_message', 'unread_count', 'created_at', 'updated_at']
        read_only_fields = ['company', 'participants']

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.messages.filter(is_seen=False).exclude(sender=request.user).count()
        return 0


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['company', 'recipient']