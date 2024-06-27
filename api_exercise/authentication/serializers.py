from rest_framework import serializers
from authentication.models import User

from rest_framework import serializers
from authentication.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'first_name', 'last_name', 'password', 'password2', 'tc')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2', None)  # Use pop with default None

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)  # Remove password2 if present

        # Extract first_name and last_name from validated_data
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        # Create user with UserManager
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            password=password,
            **validated_data
        )

        return user



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']