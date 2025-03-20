from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import json
import uuid
from .models import Profile


def signin(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if already verified
                if user.profile.is_verified:
                    login(request, user)
                    return JsonResponse({'status': 'success', 'redirect': '/'})

                # Generate a verification token
                token = str(uuid.uuid4())
                user.profile.verification_token = token
                user.profile.save()

                # Send verification email
                send_mail(
                    'Verify Your Email',
                    f'Click this link to verify: http://127.0.0.1:8000/verify/?token={token}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                # Log the user in (pending verification)
                login(request, user)
                return JsonResponse({'status': 'success', 'redirect': '/verify/'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return render(request, 'sign_in.html')


def sign_up(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            password_confirm = data.get('password_confirm')

            if password != password_confirm:
                return JsonResponse({'status': 'error', 'message': 'Passwords do not match'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already taken'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already registered'}, status=400)

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = True  # Active but unverified
            user.save()

            # Generate verification token
            token = str(uuid.uuid4())
            user.profile.verification_token = token
            user.profile.save()

            # Send verification email
            send_mail(
                'Verify Your Email',
                f'Click this link to verify: http://127.0.0.1:8000/verify/?token={token}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return JsonResponse({'status': 'success', 'message': 'Check your email to verify your account'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return render(request, 'sign_up.html')


def verify(request):
    token = request.GET.get('token')
    if token:
        try:
            profile = Profile.objects.get(verification_token=token)
            profile.is_verified = True
            profile.verification_token = ''  # Clear token after use
            profile.save()
            login(request, profile.user)
            return redirect('home')
        except Profile.DoesNotExist:
            return render(request, 'verify.html', {'error': 'Invalid or expired token'})
    return render(request, 'verify.html')


def home(request):
    return render(request, 'home.html')