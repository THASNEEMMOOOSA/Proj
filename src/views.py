from django.shortcuts import render,redirect
from django.http import HttpResponse,request
from django.template import loader,context
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import razorpay
from .models import Bookpack,Order

# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt,csrf_protect,requires_csrf_token
# Create your views here.
# views.py

# @requires_csrf_token

def landingpage(request):
    template=loader.get_template('landingpage.html')
    # bookp=Bookpack.objects.all()
    # context={
    #     'bookp':bookp,
    # }
    return HttpResponse(template.render())


def signup(request):
     if request.user.is_authenticated:
            return redirect('home')

     if request.method=='POST':
        uname=request.POST['uname']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password!=password2:
            return HttpResponse("Passwords do not Match!!!")
        else:
         user=User.objects.create_user(uname,email,password)
         print(user)
         user.save()
         return redirect('login')
        
       

     return render(request,'signup.html')


def login(request):
    if request.user.is_authenticated:
            return redirect('home')


    if request.method=='POST':
        uname=request.POST['uname']
        password=request.POST['password']
        user=authenticate(request,username=uname,password=password)
        if user is not None:
            auth_login(request,user)
            bookp=Bookpack.objects.all()

            return redirect('home')
           
            return render(request,'index.html', {'user':user,'bookp':bookp})
        else:
            return HttpResponse('Username or Password doesnt match or User doesnt exists!!')
    return render(request,'login.html')

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        return redirect('index')
    return redirect('login')

@login_required(login_url='login')
def logouth(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    return redirect('login')




@login_required(login_url='login')

def index(request):
    template=loader.get_template('index.html')
    bookp=Bookpack.objects.all()
    context={
        'bookp':bookp,
    }
    return HttpResponse(template.render(context,request))

@login_required(login_url='login')
def bookpage(request,id):
    template=loader.get_template('bookpage.html')
    bookpack=Bookpack.objects.get(id=id)
    context={
        "bookpack":bookpack,
        "total":21+bookpack.price,
    }
   
    return HttpResponse(template.render(context,request))

@login_required(login_url='login')
def savepage(request,id):
    bookpack=Bookpack.objects.get(id=id)
    productid=bookpack.productid


    if request.method == 'POST':
      firstname=request.POST['firstName']
      lastname=request.POST['lastName']
      email=request.POST['email']
      address1=request.POST['address1']
      address2=request.POST['address2']
      state=request.POST['state']
      pin=request.POST['pin']
      amount = int(bookpack.price+21)*100  # Amount in paisa
      name=firstname+' '+lastname
      client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
      response_payment = client.order.create(dict(amount= amount, currency= 'INR'))
      print(response_payment)   
      order_id = response_payment['id']
      order_status = response_payment['status']
      if order_status=='created':
         order=Order(name=name,amount=(amount/100),email=email,address1=address1,address2=address2,state=state,pin=pin,productid=productid,order_id=order_id)
         order.save()
      response_payment['name']=name
      Order.objects.get(order_id=order_id)    
  
    #   orderdetail = Order.objects.get(productid=productid)
    #   template=loader.get_template('booksavepage.html')
    
    #   context={
    #     "bookpack":bookpack,
    #     "order":new_order,
    #     "total":21+bookpack.price,
    # }
    return render(request, 'sumpage.html',{
        "bookpack":bookpack,
        "order": Order.objects.get(order_id=order_id),
        "total":21+bookpack.price,
        'payment':response_payment
    })
  
@csrf_exempt
def payment_status(request):
    response=request.POST
    print(response)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    try:
        status=client.utility.verify_payment_signature({
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature':  response['razorpay_signature']
        })
        order=Order.objects.get(order_id=response['razorpay_order_id'])
        order.razorpay_payment_id=response['razorpay_payment_id']
        order.paid=True
        order.save()
        return render(request,'payment_status.html',{'status':True})
    except:
        return render(request,'payment_status.html',{'status':False})

   
    #   return HttpResponse(template.render(context,request))        
    
# def sumpage(request,id):
#     template=loader.get_template('sumpage.html')
#     bookpack=Bookpack.objects.get(id=id)
#     order_productid=bookpack.productid
#     orderdetail = Order.objects.get(order_productid=order_productid)
#     order_amount=(bookpack.price+21)*100
#     order_productid=bookpack.productid
#     client = razorpay.Client(auth=("rzp_test_bYBHeH757vrngg", "FRpY7h49QKRBOXRK1UVGWAMC"))
  

    

#     # if request.method == 'POST':
#     DATA = {
#     "amount": order_amount,
#     "currency": "INR",
#     "receipt": "receipt#1",
#     "notes": {
#         "key1": "value3",
#         "key2": "value2"
#     }
# }
#     payment=client.order.create(data=DATA)
#     order_idd=payment['id']

#     context={
#         "bookpack":bookpack,
#         "order":orderdetail,
#         "payment":order_idd,
#         "total":21+bookpack.price,

#     }

#     print(payment)
#     return HttpResponse(template.render(context,request))

# def payment_process(request):
#     if request.method == 'POST':
#         amount = 50000  # Amount in paisa
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
#         order_id = payment['id']

#         # Render the payment form with Razorpay details
#         return render(request, 'payment/payment_form.html', {'razorpay_key': settings.RAZORPAY_KEY_ID, 'order_id': order_id})
    
#     # Handle all other request methods with a "Method not allowed" response
#     return HttpResponse("Method not allowed", status=405)

# def success(request):
#     response=request.POST
#     print(response)

#     template=loader.get_template('success.html')



 
   
#     return HttpResponse(template.render())
