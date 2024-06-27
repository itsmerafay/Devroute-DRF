from rest_framework import serializers
from authentication.models import User
from .models import UserProfile
from rest_framework.validators import ValidationError

# FOr listing Only

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)                             # to make it in a string 

    class Meta:
        model = UserProfile
        fields = ['user','city','cnic','address']

class UserProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['city', 'cnic', 'address']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the authenticated user
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        instance.city = validated_data.get('city', instance.city)
        instance.cnic = validated_data.get('cnic', instance.cnic)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance