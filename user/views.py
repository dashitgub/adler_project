from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserLoginSerializer

class UserRegisterView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_register.html')

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Регистрация успешна!'}, status=201)
        return JsonResponse({'errors': serializer.errors}, status=400)

class UserLoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return render(request, 'notes_list.html', {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return render(request, 'user_login.html', {
            'error': 'Неверные учетные данные. Попробуйте снова.',
        })