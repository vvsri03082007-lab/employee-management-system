from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Company(models.Model):
    company_name = models.CharField(max_length=150)
    company_email = models.EmailField(unique=True)
    company_logo = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100)
    salary = models.IntegerField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class DeletedEmployee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100)
    salary = models.IntegerField()
    phone = models.CharField(max_length=15)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Deleted)"

class DynamicField(models.Model):
    FIELD_TYPES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('dropdown', 'Dropdown'),
        ('date', 'Date'),
        ('checkbox', 'Checkbox'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES, default='text')
    required = models.BooleanField(default=False)
    options = models.CharField(max_length=500, blank=True, null=True)  # Comma-separated choices for dropdown

    def __str__(self):
        return f"{self.company.company_name} - {self.field_name}"

class EmployeeDynamicData(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='dynamic_data')
    dynamic_field = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.employee.name} - {self.dynamic_field.field_name}: {self.value}"

class WorkspaceVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.code}"

class OTPVerification(models.Model):
    PURPOSE_CHOICES = (
        ('onboard', 'Onboarding'),
        ('login', 'Login'),
        ('reset', 'Password Reset'),
        ('delete_workspace', 'Delete Workspace'),
    )
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='login')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.otp} ({self.purpose})"


# ---------------- COLLABORATION & MESSAGING MODELS ----------------

class EmployeeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    custom_status = models.CharField(max_length=100, blank=True, null=True)
    status_emoji = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} Profile"


class Conversation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='conversations')
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation ({self.id}) - {self.company.company_name}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.email}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('message', 'New Message'),
        ('system', 'System Alert'),
        ('announcement', 'Announcement'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='message')
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.email} - {self.title}"


# Signals for automatic profile creation/saving
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        EmployeeProfile.objects.create(user=instance)
    instance.profile.save()