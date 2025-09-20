"""
location_serializer.py
~~~~~~~~~~~~~~~~~~~~~~
Serializer for Location model, handling validation and transformation.
"""

from rest_framework import serializers
from users.models import Location


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location model.

    Fields
    ------
    id : int
        Primary key of the location.
    name : str
        Name of the location.
    address_line : str
        Address line of the location.
    city : str
        City name.
    state : str
        State name.
    zip_code : str
        Postal code.
    country : str
        Country name.
    created_at : datetime
        Timestamp when location was created.
    updated_at : datetime
        Timestamp when location was last updated.

    Notes
    -----
    - `id`, `created_at`, and `updated_at` are read-only.
    """

    class Meta:
        model = Location
        fields = [
            "id", "name", "address_line", "city", "state",
            "zip_code", "country", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        """Ensure the location name is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Location name cannot be empty.")
        return value
