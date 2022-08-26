from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
# Create your models here.

class UserCustomerManager(BaseUserManager):
    def create_user(self,User_name,password,**extra_fields):
        new_user=self.model(User_name=User_name,**extra_fields)
        new_user.set_password(password)
        new_user.save()
        return new_user
    
    def create_superuser(self,User_name,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('The superuser should be a staff'))
        
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('The superuser should be a active'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('This is for superuser only '))
        
        return self.create_user(User_name,password,**extra_fields)
    
    
class User(AbstractUser):
    
    Options=[
        ('person without disability','person without disiability'),
        ('person with disability','person with disability')
    ]
  
    
    disabilityQuategory=[
        ('deaf','deaf'),
        ('blind','blind'),
        ('handicap','handicap'),
        ('mental','mental'),
        ('speech impair','speech impair')
        
    ]
    # creator=models.ForeignKey(NewUser, on_delete=models.Set_DEFAULT)
    SignUp_as=models.CharField(choices=Options, max_length=100)
    first_Name=models.CharField(max_length=100)
    Last_Name=models.CharField(max_length=100)
    User_name=models.CharField(max_length=100, blank=True, null=False, unique=True)
    is_active=models.BooleanField(default=True)
    password=models.CharField(max_length=100)
    create_on=models.DateField(auto_now_add=True)
    Disability=models.CharField(choices=disabilityQuategory,max_length=100)
    phone_Number =PhoneNumberField(null=False,unique=True)
    
    USERNAME_FIELD='User_name'
    REQUIRED_FIELDS= []
    
    objects=UserCustomerManager()
    
    def __str__(self):
        return f"<User {self.User_name}"
    @property  
    def username(self):
        return self.User_name
    @property
    def first_name(self):
        return self.first_Name
   
    @property
    def last_name(self):
        return self.last_name
class partnershipsInsitutions(models.Model):
    Institutions=[
        ('THT', 'Troupe des persones Handicapees Twuzuzanye Rwanda'),
        ('NUDOR','NUDOR'),
        ('NGO','NGO'),
    ]
    InstitutionName=models.CharField(choices=Institutions, max_length=100,null=True, blank=True) 
    is_active=models.BooleanField(default=True)
    password=models.CharField(max_length=50,null=True)
    is_staff=models.BooleanField(default=True)
    
    def __str__(self):
        return self.InstitutionName
    @property
    def is_staff(self):
        return self.is_staff
    