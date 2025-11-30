from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import json
import random

from hotel.models import ContactMessage, Booking, LoginEvents, EmailOTP, Profile


# ----------------------------
# INDEX / ABOUT / CONTACT
# ----------------------------
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message)
        return render(request, 'contact.html', {'success': True, 'name': name})
    return render(request, 'contact.html')


# ----------------------------
# SIGNUP (STEP 1 - SEND OTP)
# ----------------------------
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").lower().strip()
        phone = request.POST.get("phone").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match!"})

        # Check if a user with the same email + phone already exists
        if User.objects.filter(email=email, profile__phone=phone).exists():
            return render(request, "signup.html", {"error": "An account with this email & phone already exists!"})

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Save OTP
        EmailOTP.objects.update_or_create(
            email=email,
            defaults={"otp": otp, "created_at": timezone.now()}
        )

        # Send OTP via email
        send_mail(
            subject="DreamStay Email OTP Verification",
            message=f"Your OTP is {otp}. Valid for 1 minute.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        # Save temp user info in session
        request.session["temp_user"] = {"username": username, "email": email, "phone": phone, "password": password}
        return redirect("signup_verify")

    return render(request, "signup.html")


# ----------------------------
# SIGNUP VERIFY OTP (STEP 2)
# ----------------------------
def signup_verify(request):
    if request.user.is_authenticated:
        return redirect("index")

    temp_user = request.session.get("temp_user")
    if not temp_user:
        return redirect("signup")

    email = temp_user["email"]
    otp_record = EmailOTP.objects.filter(email=email).first()

    if request.method == "POST":
        user_otp = request.POST.get("otp")

        if not otp_record:
            return render(request, "signup_verify.html", {"error": "OTP not found!"})

        if otp_record.is_expired():
            otp_record.delete()
            return render(request, "signup_verify.html", {"error": "OTP expired! Please try again."})

        if user_otp != otp_record.otp:
            return render(request, "signup_verify.html", {"error": "Incorrect OTP!"})

        # Create user
        user = User.objects.create_user(
            username=temp_user["username"],
            email=email,
            password=temp_user["password"]
        )
        Profile.objects.create(user=user, phone=temp_user["phone"])

        # Login user
        auth_login(request, user)

        # Clear session & OTP
        otp_record.delete()
        del request.session["temp_user"]

        return redirect("index")

    return render(request, "signup_verify.html", {"email": email})



# ----------------------------
# FORGOT PASSWORD (SEND OTP)
# ----------------------------
def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email").lower().strip()

        if not User.objects.filter(email=email).exists():
            return render(request, "forgot_password.html", {"error": "Email not registered!"})

        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.update_or_create(email=email, defaults={"otp": otp, "created_at": timezone.now()})

        send_mail(
            subject="DreamStay Password Reset OTP",
            message=f"Your OTP is {otp}. Valid for 1 minute.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        request.session["reset_email"] = email
        return redirect("verify_forgot_otp")

    return render(request, "forgot_password.html")


# ----------------------------
# FORGOT PASSWORD VERIFY OTP
# ----------------------------
def verify_forgot_otp(request):
    email = request.session.get("reset_email")
    if not email:
        return redirect("forgot_password")

    otp_record = EmailOTP.objects.filter(email=email).first()

    if request.method == "POST":
        user_otp = request.POST.get("otp")

        if not otp_record:
            return render(request, "verify_forgot_otp.html", {"error": "OTP not found!"})

        if otp_record.is_expired():
            otp_record.delete()
            return render(request, "verify_forgot_otp.html", {"error": "OTP expired! Please try again."})

        if user_otp != otp_record.otp:
            return render(request, "verify_forgot_otp.html", {"error": "Incorrect OTP!"})

        otp_record.delete()
        return redirect("reset_password")

    return render(request, "verify_forgot_otp.html", {"email": email})


# ----------------------------
# RESET PASSWORD
# ----------------------------
def reset_password(request):
    email = request.session.get("reset_email")
    if not email:
        return redirect("forgot_password")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "reset_password.html", {"error": "Passwords do not match!"})

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        del request.session["reset_email"]
        return redirect("login")

    return render(request, "reset_password.html")


# ----------------------------
# BOOKING OTP (AJAX)
# ----------------------------
@require_http_methods(["POST"])
def request_otp_view(request):
    data = json.loads(request.body)
    phone = data.get("phone", "").strip()
    if not phone:
        return JsonResponse({"ok": False, "message": "Phone number is required."})

    if not phone.startswith("+"):
        phone = "+91" + phone

    # Implement your OTP sending logic here
    return JsonResponse({"ok": True, "message": f"OTP sent to {phone}"})


@require_http_methods(["POST"])
def verify_otp_view(request):
    data = json.loads(request.body)
    phone = data.get("phone")
    otp = data.get("otp")
    if not phone or not otp:
        return JsonResponse({"ok": False, "message": "Phone and OTP required"})

    if not phone.startswith("+"):
        phone = "+91" + phone

    # Implement your OTP verification logic here
    request.session["phone_verified"] = True
    request.session["verified_phone"] = phone
    return JsonResponse({"ok": True, "message": "Phone verified"})


# ----------------------------
# BOOKING / PAYMENT VIEWS
# ----------------------------
def booking(request):
    return render(request, "booking.html")

def payment_view(request):
    return render(request, "payment.html")




# ----------------------------
# LOGIN
# ----------------------------
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").lower().strip()
        password = request.POST.get("password", "")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid email or password!"})

        # Authenticate using username
        auth_user = authenticate(request, username=user.username, password=password)

        if auth_user is None:
            return render(request, "login.html", {"error": "Invalid email or password!"})

        # Login user
        login(request, auth_user)

        # Log IP
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        LoginEvents.objects.create(email=email, ip_address=ip or "")

        return redirect("index")

    return render(request, "login.html")

# It should exist exactly like this
def user_logout(request):
    auth_logout(request)
    return redirect("login")
