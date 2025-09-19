"""
location.py

This module contains the Location model which represents physical locations 
associated with users or patients in the system.

Created On: 18 Sept 2025
Created By: Kaustubh
"""

from django.db import models

class Location(models.Model):
    """
    Represents a physical location in the system.

    Attributes:
        name (CharField): Name of the location.
        address_line (TextField): Optional detailed address.
        city (CharField): Optional city of the location.
        state (CharField): Optional state of the location.
        zip_code (CharField): Optional postal code of the location.
        country (CharField): Optional country of the location.
        created_at (DateTimeField): Timestamp when the location was created.
        updated_at (DateTimeField): Timestamp when the location was last updated.
    """

    name = models.CharField(
        max_length=100,
        help_text="Name of the location."
    )
    address_line = models.TextField(
        blank=True, 
        null=True,
        help_text="Optional detailed address of the location."
    )
    city = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Optional city of the location."
    )
    state = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Optional state of the location."
    )
    zip_code = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Optional postal code of the location."
    )
    country = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Optional country of the location."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the location record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the location record was last updated."
    )

    class Meta:
        """
        Meta options for the Location model.

        Attributes:
            verbose_name (str): Human-readable singular name for the model.
            verbose_name_plural (str): Human-readable plural name for the model.
        """
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        """
        Returns the string representation of the Location.

        Returns:
            str: Name of the location.
        """
        return self.name
