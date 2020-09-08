from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as auth_token_view
from contact.views import AddContactView,HelloView,LogoutView,FetchCompany
#from contact.router import router

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('add_contact/',AddContactView.as_view(), name='add_contact'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #path('api/', include(router.urls)), 
	#path('api-token-auth/', auth_token_view.obtain_auth_token, name='api-tokn-auth'),
	path('hello/', HelloView.as_view(), name='hello'),
	path('logout/', LogoutView.as_view()),
    path('fetch_company/',FetchCompany.as_view(), name='hello'),
]