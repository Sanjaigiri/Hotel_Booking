from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# ----------------------------
# CONTACT MESSAGES
# ----------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact_messages'

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


# ----------------------------
# SIGNUP DETAILS (TEMP USERS)
# ----------------------------
class SignupDetails(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # hashed password
    phone = models.CharField(max_length=20, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'signup_details'

    def __str__(self):
        return self.username


# ----------------------------
# BOOKINGS
# ----------------------------
class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    room_type = models.CharField(max_length=50)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    phone_verified = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} - {self.name} ({self.room_type})"


# ----------------------------
# LOGIN EVENTS
# ----------------------------
class LoginEvents(models.Model):
    email = models.EmailField()
    ip_address = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email




# ----------------------------
# EMAIL OTPs
# ----------------------------
class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    OTP_EXPIRY_MINUTES = 1  # OTP expires after 1 minute

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=self.OTP_EXPIRY_MINUTES)

    @classmethod
    def clean_expired(cls):
        cls.objects.filter(
            created_at__lte=timezone.now() - timedelta(minutes=cls.OTP_EXPIRY_MINUTES)
        ).delete()

    def __str__(self):
        return f"{self.email} - {self.otp}"


# ----------------------------
# USER PROFILE
# ----------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
