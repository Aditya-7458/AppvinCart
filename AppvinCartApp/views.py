from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Products,Users

from django.contrib.auth.models import User
from django.contrib import messages


from django.contrib.auth import authenticate, login
from django.http import HttpResponse




from django.core.mail import send_mail
from django.conf import settings
import random





    # Fetch all products from the database
   
def Home(request):
    # Fetch all products from the database
    products = Products.objects.all()
    sort_by = request.GET.get('sort_by')
   

    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'new_arrival':
        products = products.order_by('-id')

    data={

   'products': products,
   'sort_by': sort_by


    }

    return render(request, 'home.html',data)



def Cart(request):
    return render(request,'cart.html')

def Orders(request):
    return render(request,'orders.html')

def Profile(request):
    login=False
    if login==False:
        return render(request,'login.html')



def LogIn(request):
    if request.method == 'POST':
        # Extract username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If authentication is successful, log in the user
            login(request, user)
            # Redirect to a success page or dashboard
            return HttpResponse('loged in')   # Replace 'dashboard' with your desired URL name
        else:
            # If authentication fails, display an error message
            messages.error(request, 'Invalid username or password')
            return redirect('LogIn')  # Redirect back to the login page
    else:
        # If it's a GET request, render the login form
        return render(request, 'login.html')



def SignUp(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('SignUp')

        # Check if user with email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists")
            return redirect('SignUp')

        # Create new user
        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=email, password=password)
        user.save()
        en=Users(first_name=first_name, last_name=last_name, email=email,username=email ,phone=phone,address=address,gender=gender)
        en.save()
        messages.success(request, "Registration successful. You can now login.")
        # Redirect to login page
        return redirect('LogIn')

    return render(request, 'register.html')



def LogOut(request):
    return HttpResponse('Loged out')



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            otp = str(random.randint(1000, 9999))
            request.session['otp'] = otp
            request.session['email'] = email  # Store the email in session
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'An OTP has been sent to your email. Please check your inbox.')
            return redirect('resetPassword')
        else:
            messages.error(request, 'Email does not exist.')
            return redirect('forgotPassword')
    return render(request, 'forgot_password.html')







def resetPassword(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_sent = request.session.get('otp')
        if otp_entered == otp_sent:
            # OTP matched, now update the password
            email = request.session.get('email')
            new_password = request.POST.get('new_password')
            user = User.objects.get(email=email)
            user.set_password(new_password)  # Set the new password
            user.save()
            # Password reset successful
            del request.session['otp']  # Remove OTP from session
            del request.session['email']  # Remove email from session
            messages.success(request, 'Password reset successful. Please login with your new password.')
            return redirect('LogIn')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('resetPassword')
    return render(request, 'reset_password.html')