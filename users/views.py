from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from users.models import User
from users.serializers import UserSerializer
from rest_framework.decorators import api_view

from scripts.helloWorld import getStr

@api_view(['GET', 'POST', 'DELETE'])
def user_list(request):
    # GET list of users, POST a new user, DELETE all users
    if request.method == 'GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False) # safe=False for objects serialization
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = User.objects.all().delete()
        return JsonResponse({ 'message': '{} users have been deleted'.format(count[0]) }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    # Find user my pk (primary key)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({ 'message': 'User does not exist' }, status=status.HTTP_404_NOT_FOUND)

    # GET / PUT / DELETE user
    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({ 'message': 'User has been deleted' })

@api_view(['GET'])
def user_list_email(request):
    # GET all user emails
    users = list(User.objects.values('id', 'email')) # .values() returns QuerySet which are not JSON serializable, hence the list() wrapping

    if request.method == 'GET':
        return JsonResponse(users, safe=False)


@api_view(['GET'])
def ml_ai(request):
    # GET ML/AI evaluation
    evaluation = getStr()

    if request.method == 'GET':
        return JsonResponse(evaluation, safe=False)
