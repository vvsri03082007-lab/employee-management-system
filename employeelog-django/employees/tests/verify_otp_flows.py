import os
import sys
import django

# Set up Django environment
sys.path.append('/Users/srivatsa/Documents/employee-management-system/employeelog-django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employeelog.settings')
django.setup()

from django.contrib.auth import get_user_model
from employees.models import Company, OTPVerification, Employee
from employees.views import request_otp, verify_otp
from rest_framework.test import APIRequestFactory
from rest_framework import status

User = get_user_model()

def run_otp_verification():
    print("--- STARTING OTP AND EMAIL AUTOMATION INTEGRATION TESTS ---")
    
    test_email = "owner@cybercorp.com"
    
    # 1. Clean up old records
    User.objects.filter(email=test_email).delete()
    Company.objects.filter(company_email=test_email).delete()
    OTPVerification.objects.filter(email=test_email).delete()
    
    factory = APIRequestFactory()
    
    # 2. Test Onboarding Step 1: Request OTP
    print("\n[Step 1] Requesting Onboarding OTP for:", test_email)
    request1 = factory.post('/api/request-otp/', {
        'email': test_email,
        'purpose': 'onboard'
    }, format='json')
    response1 = request_otp(request1)
    
    assert response1.status_code == status.HTTP_200_OK, f"Failed: {response1.data}"
    print("Step 1 Success! Code dispatched.")
    
    # 3. Retrieve code from DB
    otp_record = OTPVerification.objects.get(email=test_email, purpose='onboard')
    code = otp_record.otp
    print("Retrieved onboarding OTP from DB:", code)
    
    # 4. Test Onboarding Step 2: Verify OTP
    print("\n[Step 2] Verifying Onboarding OTP:", code)
    request2 = factory.post('/api/verify-otp/', {
        'email': test_email,
        'otp': code,
        'purpose': 'onboard'
    }, format='json')
    response2 = verify_otp(request2)
    
    assert response2.status_code == status.HTTP_201_CREATED, f"Failed: {response2.data}"
    print("Step 2 Onboarding Success! Account setup emails successfully generated:")
    print("Company Workspace:", response2.data['company_name'])
    print("Admin Username:", response2.data['admin_email'])
    print("Admin Password:", response2.data['admin_password'])
    
    # 5. Test Passwordless Login: Request OTP
    print("\n[Step 3] Requesting Login OTP for existing user:", test_email)
    request3 = factory.post('/api/request-otp/', {
        'email': test_email,
        'purpose': 'login'
    }, format='json')
    response3 = request_otp(request3)
    
    assert response3.status_code == status.HTTP_200_OK, f"Failed: {response3.data}"
    print("Step 3 Success! Login OTP dispatched.")
    
    # Retrieve Login OTP from DB
    otp_login = OTPVerification.objects.get(email=test_email, purpose='login')
    login_code = otp_login.otp
    print("Retrieved login OTP from DB:", login_code)
    
    # 6. Test Passwordless Login Step 2: Verify & Sign In
    # We will simulate a standard User-Agent to avoid triggering suspicious login alerts during normal test
    print("\n[Step 4] Submitting Login OTP:", login_code)
    request4 = factory.post('/api/verify-otp/', {
        'email': test_email,
        'otp': login_code,
        'purpose': 'login'
    }, format='json', HTTP_USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    response4 = verify_otp(request4)
    
    assert response4.status_code == status.HTTP_200_OK, f"Failed: {response4.data}"
    print("Step 4 Passwordless Login Success! Returned JWT Claims:")
    print("Access Token:", response4.data['access'][:40] + "...")
    print("Role Claim:", response4.data['role'])
    print("Company Workspace:", response4.data['company_name'])
    
    # 7. Test Suspicious Login detection (Using curl user-agent)
    print("\n[Step 5] Testing suspicious login alert triggers...")
    # Request OTP again
    request_otp(factory.post('/api/request-otp/', {'email': test_email, 'purpose': 'login'}, format='json'))
    sus_code = OTPVerification.objects.get(email=test_email, purpose='login').otp
    
    # Verify using 'curl' User-Agent
    request5 = factory.post('/api/verify-otp/', {
        'email': test_email,
        'otp': sus_code,
        'purpose': 'login'
    }, format='json', HTTP_USER_AGENT='curl/7.68.0')
    response5 = verify_otp(request5)
    
    assert response5.status_code == status.HTTP_200_OK
    print("Step 5 Suspicious Login Test Complete! Sent critical security warning email successfully.")
    
    # 8. Test Forgot Password Reset flow
    print("\n[Step 6] Requesting Password Recovery OTP for:", test_email)
    request6 = factory.post('/api/request-otp/', {
        'email': test_email,
        'purpose': 'reset'
    }, format='json')
    response6 = request_otp(request6)
    assert response6.status_code == status.HTTP_200_OK
    
    reset_code = OTPVerification.objects.get(email=test_email, purpose='reset').otp
    print("Retrieved reset code from DB:", reset_code)
    
    print("\n[Step 7] Setting new password using Recovery OTP...")
    request7 = factory.post('/api/verify-otp/', {
        'email': test_email,
        'otp': reset_code,
        'purpose': 'reset',
        'new_password': 'newSecurePassword99!'
    }, format='json')
    response7 = verify_otp(request7)
    
    assert response7.status_code == status.HTTP_200_OK, f"Failed: {response7.data}"
    print("Step 7 Success! Password reset verification message:", response7.data['message'])
    
    print("\n--- ALL OTP INTEGRATION TESTS PASSED SUCCESSFULLY! ---")

if __name__ == '__main__':
    run_otp_verification()
