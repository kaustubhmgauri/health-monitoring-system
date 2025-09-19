"""
heartrate.py

This module contains the HeartRate model which stores heart rate measurements 
for patients, including metadata about who recorded the measurement and when.

Created On: 18 Sept 2025
Created By: Kaustubh
"""

from django.db import models
from patients.models import Patient
from users.models import User

class HeartRate(models.Model):
    """
    Represents a heart rate measurement for a patient.

    Attributes:
        patient: The patient whose heart rate is recorded.
        recorded_by: User who recorded the measurement. Can be null.
        bpm: Beats per minute recorded for the patient.
        recorded_at: Timestamp when the heart rate was recorded.
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    patient: Patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='heart_rates',
        help_text="The patient whose heart rate is recorded."
    )
    recorded_by: User = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_heart_rates',
        help_text="User who recorded the heart rate. Can be null."
    )
    bpm: int = models.PositiveIntegerField(
        help_text="Beats per minute recorded for the patient."
    )
    recorded_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the heart rate was recorded."
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the record was created."
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated."
    )

    class Meta:
        """
        Meta options for the HeartRate model.

        Attributes:
            ordering: Default ordering of records (newest first based on recorded_at).
        """
        ordering = ['-recorded_at']
        verbose_name = "Heart Rate"
        verbose_name_plural = "Heart Rates"

    def __str__(self) -> str:
        """
        Returns the string representation of the HeartRate record.

        Returns:
            str: Formatted string showing patient name, BPM, and recorded timestamp.
        """
        return f"{self.patient} - {self.bpm} BPM at {self.recorded_at}"
