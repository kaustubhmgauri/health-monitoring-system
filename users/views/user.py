"""
user.py

Provides user-related APIs:
- Register new users
- Login with JWT authentication
- List all users (admin only)
"""

import logging
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import UserRegistrationSerializer, UserSerializer

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing user registration, login, and user retrieval.
    """
    
    def get_permissions(self):
        """
        Override default permissions based on action.

        Steps:
        1. Check the current action (register/login/list_users).
        2. Return AllowAny for public actions.
        3. Return IsAdminUser for list_users.
        4. Default to IsAuthenticated for all other actions.

        Returns:
            list: List of permission classes
        """
        if self.action in ["register", "login"]:
            return [AllowAny()]
        elif self.action == "list_users":
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Register a new user.

        Args:
            request (Request): The incoming HTTP request containing user data.

        Returns:
            Response: JSON response containing the created user data and message.

        Raises:
            serializers.ValidationError: If request data is invalid.
            Exception: If unexpected error occurs during user creation.

        Steps:
            1. Validate request body with UserRegistrationSerializer.
            2. Save user if valid.
            3. Return serialized user data with success message.
        """
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                logger.info(f"User registered successfully: {user.username}")
                return Response(
                    {
                        # "user": UserSerializer(user, context={'request': request}).data,
                        "message": "User registered successfully."
                    },
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            logger.error(f"Error during user registration: {str(e)}")
            return Response(
                {"detail": "Failed to register user.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Authenticate a user and return JWT tokens.

        Args:
            request (Request): The incoming HTTP request containing username and password.

        Returns:
            Response: JSON response containing access & refresh tokens and user data.

        Raises:
            AuthenticationFailed: If credentials are invalid.
            Exception: If unexpected error occurs.

        Steps:
            1. Extract username and password from request body.
            2. Authenticate user using Django's authenticate().
            3. Generate JWT tokens if authentication succeeds.
            4. Return tokens and user data.
        """
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                logger.warning("Login failed: Missing username or password.")
                return Response(
                    {"detail": "Please provide both username and password."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                logger.info(f"User logged in successfully: {user.username}")
                return Response(
                    {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                        "user": UserSerializer(user, context={'request': request}).data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                logger.warning(f"Invalid login attempt for username: {username}")
                return Response(
                    {"detail": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return Response(
                {"detail": "Login failed due to server error.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def list_users(self, request):
        """
        List all registered users (admin only).

        Args:
            request (Request): Incoming HTTP request.

        Returns:
            Response: JSON response containing all users.

        Raises:
            PermissionDenied: If user is not an admin.
            Exception: If query fails.
        """
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            logger.info("Admin retrieved user list successfully.")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving users: {str(e)}")
            return Response(
                {"detail": "Failed to retrieve users.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
