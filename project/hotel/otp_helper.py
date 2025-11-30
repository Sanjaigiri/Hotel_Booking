"""
OTP Helper module for sending and verifying OTP using Twilio Verify API.
"""

from twilio.rest import Client
from django.conf import settings
import random


def send_otp(phone):
    """
    Send OTP to the provided phone number using Twilio Verify API.
    
    Args:
        phone (str): Phone number in E.164 format (e.g., +919876543210)
        
    Returns:
        dict: Response dictionary with 'ok' status and optional 'message'
              {'ok': True, 'message': 'OTP sent successfully'}
              {'ok': False, 'message': 'Error description'}
    """
    # DEVELOPMENT MODE: Use mock OTP
    if getattr(settings, 'USE_MOCK_OTP', False):
        return {
            'ok': True,
            'message': f'OTP sent successfully! [DEV MODE: Use {settings.MOCK_OTP_CODE}]',
            'mock': True,
            'mock_code': settings.MOCK_OTP_CODE
        }
    
    # PRODUCTION MODE: Use Twilio Verify API
    try:
        # Initialize Twilio client
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        
        # Send verification code using Twilio Verify
        verification = client.verify \
            .v2 \
            .services(settings.TWILIO_VERIFY_SERVICE_SID) \
            .verifications \
            .create(to=phone, channel='sms')
        
        if verification.status == 'pending':
            return {
                'ok': True,
                'message': 'OTP sent successfully to your phone number.',
                'mock': False
            }
        else:
            return {
                'ok': False,
                'message': 'Failed to send OTP. Please try again.'
            }
            
    except Exception as e:
        error_message = str(e)
        # Log the error for debugging
        print(f"Error sending OTP: {error_message}")
        
        # Handle Twilio trial account limitation (Error 21608)
        if '21608' in error_message or 'unverified' in error_message.lower():
            return {
                'ok': False,
                'message': 'This phone number is not verified. Trial accounts can only send OTP to verified numbers. Please verify your number at twilio.com or contact support.'
            }
        
        # Handle other common Twilio errors
        if '21211' in error_message:
            return {
                'ok': False,
                'message': 'Invalid phone number format. Please enter a valid phone number.'
            }
        
        if '20003' in error_message or 'authenticate' in error_message.lower():
            return {
                'ok': False,
                'message': 'Server configuration error. Please contact support.'
            }
        
        # Generic error message
        return {
            'ok': False,
            'message': 'Unable to send OTP at this time. Please try again later or contact support.'
        }


def verify_otp(phone, code):
    """
    Verify OTP code for the provided phone number using Twilio Verify API.
    
    Args:
        phone (str): Phone number in E.164 format (e.g., +919876543210)
        code (str): 6-digit OTP code entered by the user
        
    Returns:
        dict: Response dictionary with 'ok' status and optional 'message'
              {'ok': True, 'message': 'OTP verified successfully'}
              {'ok': False, 'message': 'Invalid or expired OTP'}
    """
    # DEVELOPMENT MODE: Use mock OTP verification
    if getattr(settings, 'USE_MOCK_OTP', False):
        if code == settings.MOCK_OTP_CODE:
            print(f"[MOCK MODE] OTP verified for {phone}")
            return {
                'ok': True,
                'message': 'OTP verified successfully! [Development Mode]',
                'mock': True
            }
        else:
            return {
                'ok': False,
                'message': f'Invalid OTP. [DEV MODE: Use {settings.MOCK_OTP_CODE}]',
                'mock': True
            }
    
    # PRODUCTION MODE: Use Twilio Verify API
    try:
        # Initialize Twilio client
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        
        # Verify the OTP code
        verification_check = client.verify \
            .v2 \
            .services(settings.TWILIO_VERIFY_SERVICE_SID) \
            .verification_checks \
            .create(to=phone, code=code)
        
        if verification_check.status == 'approved':
            return {
                'ok': True,
                'message': 'OTP verified successfully!',
                'mock': False
            }
        else:
            return {
                'ok': False,
                'message': 'Invalid or expired OTP. Please try again.',
                'mock': False
            }
            
    except Exception as e:
        error_message = str(e)
        # Log the error for debugging
        print(f"Error verifying OTP: {error_message}")
        
        # Handle common verification errors
        if '20404' in error_message:
            return {
                'ok': False,
                'message': 'No OTP verification found. Please request a new OTP.'
            }
        
        if 'expired' in error_message.lower():
            return {
                'ok': False,
                'message': 'OTP has expired. Please request a new one.'
            }
        
        # Generic error
        return {
            'ok': False,
            'message': 'Unable to verify OTP. Please try again or request a new OTP.'
        }
