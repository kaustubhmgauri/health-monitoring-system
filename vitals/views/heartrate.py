"""
heartrate.py
~~~~~~~~~~~~~~~
APIs for recording and retrieving patient heart rate data.
Includes pagination, search, and ordering functionality.
"""

import logging
from django.db import DatabaseError
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from vitals.models import HeartRate
from vitals.serializers import HeartRateSerializer

# Configure module-level logger
logger = logging.getLogger(__name__)


class HeartRateViewSet(viewsets.ModelViewSet):
    """
    API to record and retrieve heart rate data for patients.

    Public Methods
    --------------
    list(request, *args, **kwargs)
        Retrieve paginated heart rate data with search and ordering.

    create(request, *args, **kwargs)
        Record a new heart rate entry for a patient.

    Attributes
    ----------
    queryset : QuerySet
        All heart rate records.
    serializer_class : Serializer
        Serializer used for validation and transformation.
    permission_classes : list
        Permissions required (authenticated users only).
    pagination_class : PageNumberPagination
        Built-in pagination strategy.
    filter_backends : list
        Filters enabled for search and ordering.
    search_fields : list
        Searchable patient fields.
    ordering_fields : list
        Fields that can be ordered.

    Raises
    ------
    DatabaseError
        If database operations fail.
    ValidationError
        If input data is invalid.
    """

    queryset = HeartRate.objects.all()
    serializer_class = HeartRateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["patient__first_name", "patient__last_name"]
    ordering_fields = ["recorded_at", "bpm"]

    def list(self, request, *args, **kwargs):
        """
        Retrieve paginated heart rate records.

        Steps
        -----
        1. Log request for fetching heart rate data.
        2. Query HeartRate objects.
        3. Apply pagination, search, and ordering.
        4. Serialize paginated results.
        5. Return serialized data.
        """
        try:
            logger.info("Fetching heart rate records...")
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger.info("Heart rate records fetched successfully.")
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DatabaseError as db_err:
            logger.error(f"Database error while fetching heart rates: {db_err}")
            return Response(
                {"detail": "Database error while fetching heart rate data."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as ex:
            logger.error(f"Unexpected error in list: {ex}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        """
        Record a new heart rate entry.

        Steps
        -----
        1. Log request for creating a new heart rate record.
        2. Validate input data with serializer.
        3. Save entry with recorded_by set as request.user.
        4. Return created entry in response.

        Arguments
        ---------
        request : Request
            HTTP request containing heart rate data.

        Returns
        -------
        Response
            JSON response with created entry or validation errors.
        """
        try:
            logger.info("Creating a new heart rate record...")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                heart_rate = serializer.save(recorded_by=request.user)
                logger.info(f"Heart rate record created successfully: {heart_rate.id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.warning(f"Validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as db_err:
            logger.error(f"Database error while creating heart rate record: {db_err}")
            return Response(
                {"detail": "Database error while saving heart rate data."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as ex:
            logger.error(f"Unexpected error in create: {ex}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
