from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
#from .models import User
from django.contrib.auth.models import User
import jwt, datetime



# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        #print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(1)

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        #print(username,password)
        user = User.objects.filter(username=username).first()
        #print(user)
        if user is None:
            response = Response()
            response.data = {
                'error':'Please enter a correct username and password. Note that both fields may be case-sensitive.',
                'login':0   
                }
            return response

            #raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            response = Response()
            response.data = {
                'error':'Please enter a correct username and password. Note that both fields may be case-sensitive.' ,
                'login':0
                }
            return response
            #raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')#.decode('utf-8')
        #print(type(token))
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'login':1        
            }
        return response

class UserView(APIView):
    def get(self, request):

        
        try :
            token = request.data['jwt']
        except:
            token = request.COOKIES.get('jwt')
        

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)
        #print(serializer.data)
        return Response(serializer.data)

class LogoutView(APIView):
    def get(self, request):
        
        response = Response()
        response.delete_cookie('jwt')
        response.delete_cookie('sessionid')
        response.data = {
            'message': 'success'
        }
        #print('logout')
        #print(response)
        return response
