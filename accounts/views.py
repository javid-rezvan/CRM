from django.shortcuts import render,redirect
from . models import Product,Order,Tag,Customer
from . forms import OrderForm
from django.forms import inlineformset_factory
from . filters import OrderFilter
from . forms import CreateUserForm,CustomerForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'accounts/products.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    myFilter=OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs
    context={'customer':customer,'orders':orders,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer=Customer.objects.get(id=pk)
    # form=OrderForm(initial={'customer':customer})
    formset=OrderFormSet(instance=customer)
    if request.method == 'POST':
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order=Order.objects.get(id=pk) 
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context={'item':order }
    return render(request,'accounts/delete.html',context)

@unauthenticated_user
def registerPage(request):
    
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user
            )
            messages.success(request,'user was created for: ',user.username)
            return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
  
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(username=username)
        
            Authuser=authenticate(request,username=username,password=password)
            if Authuser is not None:
               login(request,Authuser)
               return redirect('home')
            else:
                messages.error(request,'password is not correct')
        except:
            messages.error(request,'user dose not exists')    
            
   
    return render(request,'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    deliverd=orders.filter(status='Deliverd').count()
    pending=orders.filter(status='pending').count()
    context={'orders':orders,'total_orders':total_orders,'deliverd':deliverd,'pending':pending}
    return render(request,'accounts/user.html',context)

def accountSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method == 'POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'accounts/account_settings.html',context)