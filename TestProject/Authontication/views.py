from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .serializers import *
from rest_framework import generics, mixins,status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed 
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser 
import jwt,datetime
# Create your views here.


class UserIPAView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class=UserSiliarizer
    queryset=User.objects.all()
    def post(self, request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        return self.list(request)
    
class Login(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class=UserSerializerLogIn
    def post (self,request):  
        User_name=request.data['User_name']
        password=request.data['password']
        
        user=User.objects.filter(User_name=User_name).first()
        if user is None:
            raise AuthenticationFailed('user is not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('password is incorrect')
        
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow()  
        }
        
        token=jwt.encode(payload,'secret', algorithm='HS256')
        response=Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data={
                'jwt':token
            }
        
        return response



class UserView(APIView):
    # permission_classes=[IsAuthenticated,IsAdminUser]
    def get(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthentacated')
        
        
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSiliarizer(user)
        return Response(serializer.data)

    
class LogOut(APIView):
    def post(self,request):
        response=Response(status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('jwt')
        
        response.data={
            'message':'user has been logout successful!!' 
        }
        
        return response