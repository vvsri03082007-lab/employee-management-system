import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)

def _send_company_email(subject, template_name, context, recipient_email):
    """
    Base email sender function that compiles HTML and text templates,
    sending them using standard Django SMTP/Console configurations.
    Ready to scale to external providers like SendGrid/SES via configurations.
    """
    try:
        html_content = render_to_string(f'emails/{template_name}.html', context)
        text_content = render_to_string(f'emails/{template_name}.txt', context)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        logger.info(f"Successfully sent '{subject}' email to {recipient_email}")
    except Exception as e:
        logger.error(f"Failed to send email '{subject}' to {recipient_email}: {str(e)}")
        raise e

def send_verification_otp_email(recipient_email, otp):
    """
    Onboarding / Login Security: Sends a 6-digit one-time password (OTP) verification email.
    """
    context = {
        'code': otp,
        'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _send_company_email(
        subject="Email Verification Code - WorkSphere HRMS",
        template_name='verification',
        context=context,
        recipient_email=recipient_email
    )

def send_password_reset_email(recipient_email, otp):
    """
    Forgot Password Flow: Sends a 6-digit recovery password reset OTP verification code.
    """
    context = {
        'otp': otp,
        'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _send_company_email(
        subject="Reset Your Password - WorkSphere HRMS Security",
        template_name='password_reset',
        context=context,
        recipient_email=recipient_email
    )

def send_verification_email(recipient_email, code):
    """
    Legacy Workspace Verification code delivery.
    """
    context = {
        'code': code,
        'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _send_company_email(
        subject="Workspace Verification Code - WorkSphere HRMS",
        template_name='verification',
        context=context,
        recipient_email=recipient_email
    )

def send_admin_setup_email(recipient_email, company_name, password):
    """
    Step 2 Onboarding: Sends welcome setup details and generated admin credentials.
    """
    context = {
        'company_name': company_name,
        'email': recipient_email,
        'password': password,
        'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _send_company_email(
        subject=f"Your Workspace Setup Credentials - {company_name}",
        template_name='admin_setup',
        context=context,
        recipient_email=recipient_email
    )

def send_login_notification_email(recipient_email, company_name, role, user_agent):
    """
    Security Alert: Notifies the user of a successful login event with user contexts.
    """
    context = {
        'email': recipient_email,
        'company_name': company_name,
        'role': role,
        'user_agent': user_agent,
        'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _send_company_email(
        subject="Security Notification: Successful Account Login",
        template_name='login_notification',
        context=context,
        recipient_email=recipient_email
    )

def send_suspicious_login_email(recipient_email, user_agent, timestamp):
    """
    Security Warning: Warns admin if anomalous/suspicious login contexts are detected.
    """
    context = {
        'email': recipient_email,
        'user_agent': user_agent,
        'timestamp': timestamp
    }
    _send_company_email(
        subject="CRITICAL: Suspicious Login Attempt Detected",
        template_name='suspicious_login',
        context=context,
        recipient_email=recipient_email
    )

def send_employee_added_email(recipient_email, employee_name, password, company_name):
    """
    Automatically sends welcome onboarding credentials and login link to the newly added employee.
    """
    context = {
        'employee_name': employee_name,
        'email': recipient_email,
        'password': password,
        'company_name': company_name,
        'login_link': "http://localhost:8080/login",
        'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _send_company_email(
        subject=f"Welcome to your WorkSphere HRMS Workspace - {company_name}",
        template_name='employee_added',
        context=context,
        recipient_email=recipient_email
    )

def send_employee_updated_email(admin_email, employee, company_name):
    """
    Crud Alert: Notifies the admin when an employee is successfully updated.
    """
    context = {
        'admin_email': admin_email,
        'company_name': company_name,
        'employee_name': employee.name,
        'designation': employee.designation,
        'department': employee.department or 'N/A',
        'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _send_company_email(
        subject=f"Employee Record Updated: {employee.name}",
        template_name='employee_updated',
        context=context,
        recipient_email=admin_email
    )

def send_employee_deleted_email(admin_email, deleted_employee, company_name):
    """
    Crud Alert: Notifies the admin when an employee is successfully soft-deleted.
    """
    context = {
        'admin_email': admin_email,
        'company_name': company_name,
        'employee_name': deleted_employee.name,
        'designation': deleted_employee.designation,
        'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    _send_company_email(
        subject=f"Employee Deleted: {deleted_employee.name}",
        template_name='employee_deleted',
        context=context,
        recipient_email=admin_email
    )
