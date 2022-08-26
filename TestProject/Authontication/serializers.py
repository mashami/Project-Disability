from xml.dom import ValidationErr
from .models import User
from rest_framework import serializers
from rest_framework.response import Response
from phonenumber_field.modelfields import PhoneNumberField

class UserSiliarizer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True,write_only=True)
    # User_name=serializers.CharField()
    class Meta:
        model=User
        fields=['SignUp_as','first_Name','Last_Name','User_name','create_on','Disability','phone_Number','is_active','password','confirm_password']
  
        extra_kwargs = {
            'password': {'write_only':True},
            'confirm_password':{'write_only':True},
            'is_active':{'read_only':True},
         }
    
    
   
    
    # def validate(self, data):
    #     email = data.get('email', None)
    #     if email:
    #         data['Username'] = email
    #     return data
        
    # def validate_email(self,email):
    #     existing_email=User.objects.filter(email=email).first()
    #     if existing_email:
    #         raise serializers.ValidationError("this Email is already exist!!")
    #     return email
    
    
    
    def validate(self, attrs):
        phoneNumber_exits=User.objects.filter(User_name=attrs['phone_Number']).exists()
        if phoneNumber_exits:
            raise ValidationErr(details="phone_Number name is already exists")
        
        password= attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        if password !=confirm_password:
            raise serializers.ValidationError(
                "password and confirm_password does not match"
            )
        return attrs
        
    def create(self, validated_data):
        password= validated_data.pop('password',None)
        confirm_password= validated_data.pop('confirm_password',None)
        instance=User.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)  
        instance.save()
        return instance
            
        
class UserSerializerLogIn(serializers.ModelSerializer):
     class Meta:
        model=User
        fields=['id','User_name','password']
        extra_kwargs = {
            'password': {'write_only':True},
         }
        
