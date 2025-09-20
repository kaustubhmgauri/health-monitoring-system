"""
user_serializers.py

Defines serializers for user operations:
- User registration with password validation
- User detail serialization
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import User
import logging

logger = logging.getLogger(__name__)

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with password validation.
    """
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attrs):
        """
        Validate that passwords match.

        Args:
            attrs (dict): The validated attributes.

        Raises:
            serializers.ValidationError: If passwords do not match.

        Returns:
            dict: The validated attributes.
        """
        if attrs['password'] != attrs['password2']:
            logger.warning("Password mismatch during registration.")
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user.

        Args:
            validated_data (dict): Data containing user details.

        Returns:
            User: The created user object.
        """
        try:
            validated_data.pop('password2')
            user = User.objects.create_user(**validated_data)
            logger.info(f"User created successfully in serializer: {user.username}")
            return user
        except Exception as e:
            logger.error(f"Error creating user in serializer: {str(e)}")
            raise serializers.ValidationError({"detail": "User creation failed", "error": str(e)})


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
