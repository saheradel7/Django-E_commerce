from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.TextChoices):
    ELECTRONICS = 'Electronics'
    LAPTOPS =     'Laptops'
    ARTS =        'Arts'
    FOOD =        'Food'
    HOME =        'Home'
    KITCHEN =     'Kitchen'


    
class Product(models.Model):
    name = models.CharField(max_length= 200 , blank= True ,default="")
    description=models.TextField(max_length= 200 , blank= True ,default="")
    price= models.DecimalField(max_digits=7, decimal_places=2 ,default=0)
    prand =models.CharField(max_length= 200 , blank= True ,default="") 
    category =models.CharField(max_length= 200 ,choices= Category.choices)
    ratings = models.DecimalField(max_digits=3 ,decimal_places=2,default=0)
    stock = models.IntegerField(default=0)
    user =models.ForeignKey(User , on_delete=models.SET_NULL ,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.name
    


class Reviw(models.Model):
    product = models.ForeignKey(Product , on_delete= models.CASCADE , null = True, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True)
    rating= models.IntegerField(default= 0 )
    comment = models.TextField(max_length=500 , default="" , blank=False)
    createdAt=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reating +" | " +self.comment