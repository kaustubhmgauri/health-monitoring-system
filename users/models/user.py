"""
user.py

This module contains the custom User model for the system. 
It extends Django's AbstractUser to add custom fields and constraints.

Created On: 18 Sept 2025
Created By: Kaustubh
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Attributes:
        email: Unique email address of the user.
        first_name: First name of the user.
        last_name: Last name of the user.
        is_active: Indicates whether the user account is active.
        is_staff: Indicates whether the user has admin/staff privileges.
        created_at: Timestamp when the user was created.
        updated_at: Timestamp when the user was last updated.
    """

    email: str = models.EmailField(
        unique=True,
        help_text="Unique email address of the user."
    )
    first_name: str = models.CharField(
        max_length=50,
        help_text="First name of the user."
    )
    last_name: str = models.CharField(
        max_length=50,
        help_text="Last name of the user."
    )
    is_active: bool = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active."
    )
    is_staff: bool = models.BooleanField(
        default=False,
        help_text="Designates whether the user can access the admin site."
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the user record was created."
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the user record was last updated."
    )

    USERNAME_FIELD: str = 'username'
    REQUIRED_FIELDS: list = ['email', 'first_name', 'last_name']

    class Meta:
        """
        Meta options for the User model.

        Attributes:
            verbose_name (str): Human-readable singular name for the model.
            verbose_name_plural (str): Human-readable plural name for the model.
        """
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        """
        Returns the string representation of the User.

        Returns:
            str: Username of the user.
        """
        return self.username
