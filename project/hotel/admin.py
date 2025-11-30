from django.contrib import admin
from .models import SignupDetails, LoginEvents, Booking, ContactMessage, EmailOTP, Profile


# ----------------------------
# SIGNUP DETAILS
# ----------------------------
@admin.register(SignupDetails)
class SignupDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'phone_verified', 'created_at')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('phone_verified', 'created_at')


# ----------------------------
# LOGIN EVENTS
# ----------------------------
@admin.register(LoginEvents)
class LoginEventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'ip_address', 'timestamp')
    search_fields = ('email', 'ip_address')
    list_filter = ('timestamp',)


# ----------------------------
# BOOKINGS
# ----------------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'email', 'phone',
        'room_type', 'check_in', 'check_out',
        'guests', 'payment_status', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'email', 'phone', 'room_type')
    list_filter = ('room_type', 'payment_status', 'check_in', 'check_out')


# ----------------------------
# CONTACT MESSAGES
# ----------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)


# ----------------------------
# EMAIL OTPS
# ----------------------------
@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'otp', 'created_at')
    search_fields = ('email', 'otp')
    list_filter = ('created_at',)


# ----------------------------
# USER PROFILE
# ----------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')
    search_fields = ('user__username', 'user__email', 'phone')
