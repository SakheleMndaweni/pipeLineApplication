from django.contrib.auth.models import User, auth
from django.shortcuts import render , redirect
from OrderServiceApp.models import *
from OrderServiceApp.utils import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login


@login_required(login_url='login')
def home(request):
        data = orderData(request)
        orderItems = data['orderItems']
        order = data['order']
        items = data['items']
        print(order)
        print(items)

        all_items = Product.objects.all()	
        all_orders = Order.objects.all()
        context ={'order':order,'itemList':items,'orderItems':orderItems,'allitems':all_items,'allorders':all_orders}
        return render(request, "home.html",context)
        
@login_required(login_url='login')
def orderSettings(request):
        data = orderData(request)
        orderItems = data['orderItems']
        order = data['order']
        items = data['items']
        all_items = Product.objects.all()	
        context ={'order':order,'items':items,'orderItems':orderItems,'all_items':all_items}
        return render(request, "settings.html", context)

@login_required(login_url='login')
def updateItem(request,pk):
        item = Product.objects.get(id = pk)
        context ={'item':item}
        return render(request, "update.html", context)


@login_required(login_url='login')
def itemManagement(request):
        data = orderData(request)
        orderItems = data['orderItems']
        order = data['order']
        items = data['items']
        all_items = Product.objects.all()	
        all_orders = Order.objects.all()
        context ={'order':order,'items':items,'orderItems':orderItems,'allitems':all_items,'allorders':all_orders}
        return render(request, "itemManagement.html", context)

@login_required(login_url='login')
def inventoryManagement(request):
        data = orderData(request)
        orderItems = data['orderItems']
        order = data['order']
        items = data['items']
        all_orders = Order.objects.all()
        context ={'order':order,'items':items,'orderItems':orderItems,'allitems':all_items,'allorders':all_orders}
        return render(request, "inventoryManagement", context)

def loginView(request):
        if request.method == 'POST':
            user = None
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user.is_authenticated == True:
                #new
                auth.login(request,user)
    
                return redirect("/")
                    
            else:
                messages.info(request, 'Invalid Credentials, please enter correct email and password')
        return render(request, 'authentication.html')


def login(request):
        if request.method == 'POST':
            user = None
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            print(password)
            user = auth.authenticate(username=username, password=password)
            print(user.username)
            print(user.is_authenticated)
            
            if user.is_authenticated == True:
                #new
                auth.login(request,user)
    
                return redirect("home")
                    
            else:
                messages.info(request, 'Invalid Credentials, please enter correct email and password')

        return redirect("/")

        
        

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')


def createaccount(request):
        success = False
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password1']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('createnewAccount')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('createnewAccount')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    #create a Profile object for the new user
                    user_model = User.objects.get(username= user.username,email =user.email)
                    new_profile = OrderClient.objects.create(user=user_model, name=username, email=email)
                    new_profile.save()
                    contex = {'successful': success}
                    messages.info(request, 'Welcome to Order pipeline, Account created')
                    return render(request, 'register.html',contex)
            else:
                messages.info(request, 'Password Not Matching')
                return redirect('createnewAccount')
            
        else:
            contex = {'successful': success}
            return render(request, 'register.html',contex)