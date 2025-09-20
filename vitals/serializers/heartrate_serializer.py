"""
heartrate_serializers.py
~~~~~~~~~~~~~~~~~~~~~~~~~
Serializer for HeartRate model, handling validation and transformations.
"""

from rest_framework import serializers
from vitals.models import HeartRate


class HeartRateSerializer(serializers.ModelSerializer):
    """
    Serializer for HeartRate model.

    Fields
    ------
    id : int
        Primary key of the record.
    patient : FK
        Related patient object.
    patient_name : str
        Read-only string representation of patient.
    recorded_by : FK
        User who recorded this entry.
    recorded_by_name : str
        Username of the recorder.
    bpm : int
        Heartbeats per minute.
    recorded_at : datetime
        Timestamp when record was taken.
    created_at : datetime
        Timestamp when entry was created.
    updated_at : datetime
        Timestamp when entry was updated.
    """

    patient_name = serializers.CharField(source="patient.__str__", read_only=True)
    recorded_by_name = serializers.CharField(source="recorded_by.username", read_only=True)

    class Meta:
        model = HeartRate
        fields = [
            "id", "patient", "patient_name", "recorded_by", "recorded_by_name",
            "bpm", "recorded_at", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "recorded_at", "created_at", "updated_at", "recorded_by"]

    def validate_bpm(self, value):
        """Ensure bpm value is realistic (between 30 and 250)."""
        if value < 30 or value > 250:
            raise serializers.ValidationError("BPM must be between 30 and 250.")
        return value
