from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from decimal import Decimal
from django.core.mail import send_mail
from .models import Shop, Orders, Bookings

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "homes/index.html", {"username": request.user.username})
    else:
        return render(request, "homes/index.html")

def gallery(request):
    if request.user.is_authenticated:
        return render(request, "homes/gallery.html", {"username": request.user.username})
    else:
        return render(request, "homes/gallery.html")

def contact(request):
    if request.user.is_authenticated:
        return render(request, "homes/contact.html", {"username": request.user.username})
    else:
        return render(request, "homes/contact.html")

def login_view(request):
    if request.user.is_authenticated:
        return render(request, "homes/index.html", {"username": request.user.username})
    else:
        return render(request, "homes/login.html")

def register_view(request):
    if request.user.is_authenticated:
        return render(request, "homes/index.html", {"username": request.user.username})
    else:
        return render(request, "homes/register.html")

def pricing(request):
    if request.user.is_authenticated:
        return render(request, "homes/price.html", {"username": request.user.username})
    else:
        return render(request, "homes/price.html")

def register_user(request):
    if request.user.is_authenticated: 
        return HttpResponse("First log out, then try again!")
    else:
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['mail']
        user = request.POST['username']
        password = request.POST['pass1']
        try:
            User.objects.create_user(first_name=fname, last_name=lname, username=user, email=email, password=password)
        except: 
            return HttpResponse("User already registered!")

        return render(request, "homes/login.html", {"success": "Registered Successfully!"})

def login_user(request):
    if request.user.is_authenticated: 
        return render(request, "homes/index.html", {"username": request.user.username})
    else:
        username = request.POST['user']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "homes/index.html", {"username": username})
        else:
            return render(request, "homes/index.html", {"success": "Invalid Credentials"})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, "homes/login.html", {"success": "Logged out."})
    else:
        return HttpResponse("Need to log in first!")

def shop(request):
    if request.user.is_authenticated:
        return render(request, "homes/shop.html", {"username": request.user.username})
    else:
        return redirect('register_view')

def sendMail(request):
    rec = request.POST['email']
    msg = request.POST['message']
    message = 'Query by - '+rec+' || '+msg
    if msg == '':
        return HttpResponse("Cannot send empty message!")
    else:
        send_mail('Query', 
        message,
        rec,
        ['ayushbofficial@gmail.com', rec],
        fail_silently=False)

        return redirect('index')

def buyItems(request, item_id):
    if request.user.is_authenticated:
        u = request.user
        item = Shop.objects.get(pk=item_id)
        Orders.objects.create(email=u, item=item, status='Payment Pending')
        return redirect('cart')
    else:
        return HttpResponse("Please log in first!")
def delOrder(request, oid):
    if request.user.is_authenticated:
        order = Orders.objects.get(pk=oid)
        order.delete()
        return redirect('cart')
    else:
        return HttpResponse("Please log in first!")

def cart(request):
    if request.user.is_authenticated:
        o = Orders.objects.all()
        bill = []
        completed = []
        cost = 0
        for order in o:
            if order.email == request.user:
                if order.status == 'Payment Pending':
                    bill.append(order)
                    cost = cost+order.item.price
                elif order.status == 'Completed':
                    completed.append(order)
        return render(request, "homes/cart.html", {"username": request.user.username, "bill":bill, "total": cost, "completed": completed})
    else:
        return HttpResponse("Please log in first!")

def payment(request, **kwargs):
    if request.user.is_authenticated:
        t = Decimal(request.POST['total'])
        address = request.POST['address']
        total = t*100
        o = Orders.objects.all()
        for order in o:
            if order.email == request.user:
                if order.status == 'Payment Pending':
                    order.address = address
                    order.save()
        context = {}
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['username'] = request.user.username
        context['total'] = total
        return render(request, "homes/payment.html", context)
    else:
        return HttpResponse("Please log in first!")

def paid(request):
    if request.user.is_authenticated:
        o = Orders.objects.all()
        for order in o:
            if order.email == request.user:
                if order.status == 'Payment Pending':
                    order.status = 'Completed'
                    order.save()

        return redirect('cart')
    else:
        return HttpResponse("Please log in first!")

def visit(request):
    if request.user.is_authenticated:
        return render(request, "homes/visit.html", {"username": request.user.username})
    else:
        return render(request, "homes/login.html", {"success": "Either register or login first!"})

def bookVisit(request):
    if request.user.is_authenticated:
       user = request.user
       address = request.POST['address']
       contact = request.POST['phone']
       b = Bookings.objects.create(user=user, address=address, phone=contact)
       if b:
           return render(request, "homes/success.html", {"message": "We will contact you with in 48 hours!", "username": user.username})
       else:
           return render(request, "homes/success.html", {"message": "Could not book a visit", "username": user.username})
    else:
        return HttpResponse("Please log in first!")