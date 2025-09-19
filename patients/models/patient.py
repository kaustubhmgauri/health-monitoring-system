"""
patient.py

This module contains the Patient model which represents a patient 
associated with a user in the system. It includes personal details,
contact information, and the location (place) associated with the patient.

Created On: 18 Sept 2025
Created By: Kaustubh
"""

from django.db import models
from users.models import User, Location

class Patient(models.Model):
    """
    Represents a patient in the system.

    Attributes:
        user (ForeignKey): The user (doctor, admin, or caregiver) who manages this patient.
        first_name (CharField): Patient's first name.
        last_name (CharField): Patient's last name.
        date_of_birth (DateField): Patient's date of birth.
        gender (CharField): Patient's gender. Choices: Male, Female, Other.
        place (ForeignKey): Optional location associated with the patient.
        email (EmailField): Optional email address of the patient.
        contact_number (CharField): Optional contact number of the patient.
        created_at (DateTimeField): Timestamp when the patient was created.
        updated_at (DateTimeField): Timestamp when the patient was last updated.
    """

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='patients',
        help_text="The user responsible for this patient."
    )
    first_name = models.CharField(
        max_length=50,
        help_text="Patient's first name."
    )
    last_name = models.CharField(
        max_length=50,
        help_text="Patient's last name."
    )
    date_of_birth = models.DateField(
        help_text="Patient's date of birth."
    )
    gender = models.CharField(
        max_length=10, 
        choices=[('Male','Male'),('Female','Female'),('Other','Other')],
        help_text="Patient's gender."
    )
    place = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='patients',
        help_text="Optional location associated with the patient."
    )
    email = models.EmailField(
        blank=True, 
        null=True, 
        unique=False,
        help_text="Optional email address of the patient."
    )
    contact_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Optional contact number of the patient."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the patient record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the patient record was last updated."
    )

    class Meta:
        """
        Meta options for the Patient model.

        Attributes:
            unique_together (tuple): Ensures a patient with the same first name, 
                                     last name, and date of birth cannot be duplicated
                                     for the same user.
        """
        unique_together = ('user', 'first_name', 'last_name', 'date_of_birth')
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        """
        Returns the string representation of the Patient.

        Returns:
            str: Full name of the patient.
        """
        return f"{self.first_name} {self.last_name}"
