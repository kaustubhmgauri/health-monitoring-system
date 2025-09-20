"""
patient_serializers.py
~~~~~~~~~~~~~~~~~~~~~~~
Serializer for Patient model, handling validation and transformations.
"""

import logging
from django.db import DatabaseError
from rest_framework import serializers
from patients.models import Patient

logger = logging.getLogger(__name__)


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.

    Validates and serializes patient data.
    """

    class Meta:
        model = Patient
        fields = [
            "id", "first_name", "last_name", "date_of_birth", "gender",
            "place", "email", "contact_number", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_email(self, value):
        """Ensure email format is valid."""
        if value and "@" not in value:
            logger.warning("Invalid email format provided.")
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_contact_number(self, value):
        """Ensure contact number has 10–15 digits."""
        if value and (len(value) < 10 or len(value) > 15):
            logger.warning("Invalid contact number length provided.")
            raise serializers.ValidationError("Contact number must be 10–15 digits.")
        return value

    def create(self, validated_data):
        """
        Attach logged-in user automatically when creating.

        Returns
        -------
        Patient : Patient instance
        """
        try:
            validated_data["user"] = self.context["request"].user
            patient = super().create(validated_data)
            logger.info(f"Patient created successfully with ID {patient.id}")
            return patient
        except DatabaseError as db_err:
            logger.error(f"Database error while creating patient: {db_err}")
            raise serializers.ValidationError("Failed to save patient due to a database error.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating patient: {ex}")
            raise serializers.ValidationError("An unexpected error occurred while saving patient.")
