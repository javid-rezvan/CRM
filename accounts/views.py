from django.shortcuts import render,redirect
from . models import Product,Order,Tag,Customer
from . forms import OrderForm

def home(request):
    customers=Customer.objects.all()
    total_customers=customers.count()
    
    orders=Order.objects.all()
    total_orders=orders.count()
    deliverd=orders.filter(status='Deliverd').count()
    pending=orders.filter(status='pending').count()
    
    context={'customers':customers,'orders':orders,
              'deliverd':deliverd,'pending':pending,
              'total_customers':total_customers,
              'total_orders':total_orders
              }
    
    return render(request,'accounts/dashboard.html',context)

def products(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'accounts/products.html',context)


def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    context={'customer':customer,'orders':orders}
    return render(request,'accounts/customer.html',context)


def createOrder(request):
    form=OrderForm()
    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

def updateOrder(request,pk):
    
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    
    if request.method == 'POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    order=Order.objects.get(id=pk) 
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context={'item':order }
    return render(request,'accounts/delete.html',context)


