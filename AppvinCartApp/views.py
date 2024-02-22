from django.urls import reverse
from decimal import Decimal
from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpResponse
from .models import CartItem,Cart, OrderItem, Products,Users,Orders


from django.contrib.auth.models import User
from django.contrib import messages


from django.contrib.auth import authenticate, login
from django.http import HttpResponse


from django.contrib.auth import logout

from django.core.mail import send_mail
from django.conf import settings
import random
import stripe




from django.contrib.auth.decorators import login_required




from django.utils import timezone




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


@login_required
def view_Cart(request):
    # Get the current user's cart
    cart = Cart.objects.get(user=request.user)
    
    # Get all items in the cart
    cart_items = cart.items.all()

    total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    
    # Pass messages in the context
    messages_to_render = messages.get_messages(request)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'messages': messages_to_render, 'total_price': total_price})
@login_required
def update_cart(request, cart_item_id):
    if request.method == 'POST':
        # Get the cart item object
        cart_item = get_object_or_404(CartItem, id=cart_item_id)

        # Get the new quantity from the form submission
        new_quantity = int(request.POST.get('quantity'))

        if new_quantity > 0:
            # Update the quantity of the cart item
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Quantity updated successfully.")
        else:
            # If the quantity is 0 or negative, remove the item from the cart
            cart_item.delete()
            messages.success(request, "Item removed from cart.")




    return redirect('Cart')


@login_required
def viewOrders(request):
    # Filter orders by the currently logged-in user
    user = request.user
    orders = Orders.objects.filter(customer__email=user.email).order_by('-order_date')

    context = {'orders': orders}
    if not orders:
        context['no_orders'] = True
    return render(request, 'Orders.html', context)


    


def Profile(request):
    # Check if the user is logged in
    if request.user.is_authenticated:
        # Get the user object
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        
    
        # Pass the user data to the template
        return render(request, 'profile.html', {'user': user,'first_name': first_name, 'last_name': last_name})
    else:
        # If the user is not logged in, redirect to the login page
        return redirect('LogIn')






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
            return redirect('Profile')   # Replace 'dashboard' with your desired URL name
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
    
    logout(request)
    # Redirect to a specific URL after logout, or to a default one if not specified
    return redirect('Home') 
   



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




@login_required
def buyNow(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        product_image_url = request.POST.get('product_image_url')
        product_price = request.POST.get('product_price')
        data={
            'product_id': product_id,
            'product_name': product_name,
            'product_image_url': product_image_url,
            'product_price': product_price
        } 
       
        return render(request, 'order.html',data)
    else:
        return HttpResponse("Invalid request method")




    

def generate_order_number():
    # Check if any orders exist in the database
    if Orders.objects.exists():
        # Get the latest order from the database
        latest_order = Orders.objects.latest('order_date')
        order_number = latest_order.order_number
        order_id = int(order_number.split('-')[-1])
        new_order_id = order_id + 1
        new_order_number = f"{timezone.now().strftime('%Y%m%d')}-{new_order_id:04d}"
    else:
        # If no orders exist, start with 1
        new_order_number = f"{timezone.now().strftime('%Y%m%d')}-0001"
    return new_order_number


@login_required
def addToCart(request, productId):
    if request.method == 'POST':
        # Get product details
        product = get_object_or_404(Products, id=productId)


        product_data = {
            'product_name': product.name,
            'product_id': product.id,
            'product_price': float(product.price),
        }
        
        # Get the currently logged-in user
        user = request.user
        
        try:
            # Try to retrieve the user's cart
            user_cart = user.cart
        except Cart.DoesNotExist:
            # If the user doesn't have a cart, create one
            user_cart = Cart.objects.create(user=user)
        
        # Add the product to the cart
        cart_item, added = CartItem.objects.get_or_create(cart=user_cart, product=product)
        
        if added:
            messages.success(request, "Product added to cart successfully.")
            
        else:
            messages.info(request, "Product already exists in the cart.")
        product_data_list = request.session.get('product_data_list', [])
        product_data_list.append(product_data)
        request.session['product_data_list'] = product_data_list
        
        return redirect('Cart')
    else:
        return HttpResponse("Invalid request method")


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def placeOrder(request):
    if request.method == 'POST':
        # Extract form data
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        total_price = request.POST.get('total_price')

        # Get the currently logged-in user
        user = request.user

        # Get the related Users instance
        users_instance = Users.objects.get(username=user.username)
        

        # Create a new order instance
        order = Orders.objects.create(
            order_number=generate_order_number(),
            total_amount=product_price,
            customer=users_instance,
            order_date=timezone.now()
        )

        # Add order item
        order_item = OrderItem.objects.create(
            order=order,
            product_id=product_id,
            product_name=product_name,
            price=product_price,
            quantity=1  # You may need to adjust this based on your requirements
        )

        unit_amount_cents = int(float(product_price) * 100)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': product_name,
                    },
                    'unit_amount': unit_amount_cents,  # Stripe expects price in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url = request.build_absolute_uri(reverse('success_url')),
            cancel_url = request.build_absolute_uri(reverse('cancel_url'))
        )

        # Add a success message
        messages.success(request, 'Order placed successfully!')

        # Redirect to the Orders page after placing the order
        return redirect(checkout_session.url)
    else:
        return HttpResponse("Invalid request method")
    



def success_view(request):
    return HttpResponse("Your payment was successful. Thank you for your order!")

def cancel_view(request):
    return HttpResponse("Your payment was canceled.")