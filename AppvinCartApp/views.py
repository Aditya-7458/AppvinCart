from django.shortcuts import render
from django.http import HttpResponse
from .models import Products




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
    return render(request,'profile.html')

def LogIn(request):
    return HttpResponse("Loged In")


def SignUp(request):
    return HttpResponse('Signed up')

def LogOut(request):
    return HttpResponse('Loged out')
