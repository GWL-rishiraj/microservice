from rest_framework import serializers

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *

class AddContactSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta():
        model = User
        fields =['email','role','status','company','password', 'password2']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def save(self):
        user = User(
            email = self.validated_data['email'],
            #status = self.validated_data['status'],
            user_type = self.validated_data['role'],
            #profile_image = self.validated_data['profile_image'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Password must match.'})

        user.set_password(password)
        user.save()
        return user

