from django.shortcuts import render
from . models import Product,Order,Tag,Customer

def home(request):
    return render(request,'accounts/dashboard.html')

def products(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'accounts/products.html',context)


def customer(request):
  return render(request,'accounts/customer.html')


