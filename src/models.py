from django.db import models

# Create your models here.
class Bookpack(models.Model):
    title = models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    productid=models.CharField(max_length=100)

class Order(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length = 254)
    address1=models.CharField(max_length=300)
    address2=models.CharField(max_length=300)
    state=models.CharField(max_length=300)
    pin=models.IntegerField(null=True)
    productid=models.CharField(max_length=100,blank=True)

    # order_lastname=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    order_id=models.CharField(max_length=100,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False)

   












