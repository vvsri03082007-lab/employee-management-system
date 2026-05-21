from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from employees.models import Company, Employee, DeletedEmployee, DynamicField, EmployeeDynamicData, WorkspaceVerification, OTPVerification

class Command(BaseCommand):
    help = 'Safely clears all company, user, employee, session, and verification tables to allow a fresh workspace onboarding.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Resetting WorkSphere HRMS platform data...'))
        
        # 1. Clear active Django sessions
        Session.objects.all().delete()
        self.stdout.write('✓ Cleared Active Sessions')

        # 2. Clear employee custom field values
        EmployeeDynamicData.objects.all().delete()
        self.stdout.write('✓ Cleared Employee Dynamic Fields Data')

        # 3. Clear employee directories
        Employee.objects.all().delete()
        self.stdout.write('✓ Cleared Active Employees')

        # 4. Clear archived profiles
        DeletedEmployee.objects.all().delete()
        self.stdout.write('✓ Cleared Soft-Deleted Employee Logs')

        # 5. Clear custom field configurations
        DynamicField.objects.all().delete()
        self.stdout.write('✓ Cleared Custom Fields Settings')

        # 6. Clear pending OTP verification records
        WorkspaceVerification.objects.all().delete()
        OTPVerification.objects.all().delete()
        self.stdout.write('✓ Cleared Verification / OTP Codes')

        # 7. Clear user profiles
        User = get_user_model()
        User.objects.all().delete()
        self.stdout.write('✓ Cleared User Accounts (Admins, Managers, Employees)')

        # 8. Clear company workspaces
        Company.objects.all().delete()
        self.stdout.write('✓ Cleared Company Workspaces')

        self.stdout.write(self.style.SUCCESS('Successfully reset HRMS platform authentication and data! Ready for a fresh onboarding.'))

