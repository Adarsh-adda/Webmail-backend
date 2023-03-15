from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import User,Mail
from rest_framework.exceptions import AuthenticationFailed
import datetime, jwt

# Create your views here.

 
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,MyCustomPagination,MailSerializer

# create register view
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            raise AuthenticationFailed('User already exists, please login instead')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# create login view
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id': user.id, # type: ignore
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response  = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
       
        return response
    

# CREATE USER VIEW
class UserView(APIView):

    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#  logout view
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
# create mail view
# class MailViewApi(APIView):
#     def get(self, request):
#         paginator = PageNumberPagination()
#         paginator.page_size = 10
#         paginator.get_page_size(request)
#         mail = Mail.objects.all()
#         result_page = paginator.paginate_queryset(mail, request)
#         serializer = MailSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

class MailViewApi(ListAPIView):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    pagination_class = MyCustomPagination

# UPDATE MAIL VIEW
class MailUpdateView(APIView):
    def put(self, request, pk, format=None):
        mail = Mail.objects.get(id=pk)
        serializer = MailSerializer(instance=mail, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
class StarredView(APIView):
    def get(self, request):
        mail = Mail.objects.filter(starred=True)
        serializer = MailSerializer(mail, many=True)
        return Response(serializer.data)

