import logging
from django.conf import settings
import requests

from django.shortcuts import render
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth import login as rest_login, logout as rest_logout
from rest_framework.authentication import TokenAuthentication

from contact.serializers import AddContactSerializer
from rest_framework.permissions import IsAuthenticated 
from contact.models import Contact




# Create your views here.
logger = logging.getLogger(settings.LOGGER_NAME)

logger.info("Logger Work")

class AddContactView(APIView):
	def post(self, request):
		serializer = AddContactSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status= status.HTTP_200_OK)
		return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class HelloView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		content = {'message': 'Hello, World!'}
		return Response(content)

class LogoutView(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		rest_logout(request)
		return Response(status=204)


class FetchCompany(APIView):
	#permission_classes = (IsAuthenticated,)
	def get(self, request):
		# params = {'username': 'testuser'}
		# params['access_token'] = 'c3NhbmthMDJjsd'
		# params['region'] = 'test'
		# params['role'] = 'guide'
		# params['ipaddr'] = '192.168.0.37'
		# params['name'] = 'test-testhost-001'
		# params['check'] = 'enable' 
		# url = 'http://10.0.0.1:8000/monitor/'
		# r = requests.post(url, data=params)
		# r.json()
		url = 'http://localhost:5000/companies'
		r = requests.get(url)
		print(r)
		print(type(r))
		return Response(r, status= status.HTTP_200_OK)