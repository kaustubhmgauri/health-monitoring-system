"""
patient.py
~~~~~~~~~~
API endpoints for managing patient records.
Supports CRUD operations with pagination, filtering, and search.
"""

import logging
from django.db import DatabaseError
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from patients.models import Patient
from patients.serializers import PatientSerializer

# Configure module-level logger
logger = logging.getLogger(__name__)


class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage patients (create, retrieve, list, update, delete).

    Public Methods
    --------------
    list(request, *args, **kwargs)
        Retrieve paginated patient records with search and ordering.

    create(request, *args, **kwargs)
        Add a new patient record linked to the logged-in user.

    perform_create(serializer)
        Assign the logged-in user as the owner of the patient record.

    Attributes
    ----------
    queryset : QuerySet
        All patient records.
    serializer_class : Serializer
        Serializer for patient validation and transformation.
    permission_classes : list
        Permissions required (authenticated users only).
    pagination_class : PageNumberPagination
        Built-in pagination strategy.
    filter_backends : list
        Filters enabled for search and ordering.
    search_fields : list
        Fields that support searching.
    ordering_fields : list
        Fields that support ordering.

    Raises
    ------
    DatabaseError
        If database operations fail.
    ValidationError
        If input data is invalid.
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["created_at", "first_name"]

    def list(self, request, *args, **kwargs):
        """
        Retrieve paginated patient records.

        Steps
        -----
        1. Log request for fetching patients.
        2. Apply filters, search, and ordering.
        3. Paginate the queryset.
        4. Serialize results.
        5. Return paginated response.
        """
        try:
            logger.info("Fetching patient records...")
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger.info("Patients retrieved successfully.")
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DatabaseError as db_err:
            logger.error(f"Database error while fetching patients: {db_err}")
            return Response(
                {"detail": "Database error while fetching patient data."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as ex:
            logger.error(f"Unexpected error in patient list: {ex}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        """
        Add a new patient record.

        Steps
        -----
        1. Log request for creating a patient.
        2. Validate input data with serializer.
        3. Save patient record linked to logged-in user.
        4. Return created patient data.
        """
        try:
            logger.info("Creating new patient...")
            serializer = self.get_serializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                patient = serializer.save(user=request.user)
                logger.info(f"Patient created successfully with ID {patient.id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.warning(f"Validation failed for patient creation: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as db_err:
            logger.error(f"Database error while creating patient: {db_err}")
            return Response(
                {"detail": "Database error while saving patient."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as ex:
            logger.error(f"Unexpected error in patient creation: {ex}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def perform_create(self, serializer):
        """
        Assign the logged-in user to the patient record.

        Steps
        -----
        1. Attach the request.user to serializer.
        2. Save serializer safely with try/except.
        """
        try:
            serializer.save(user=self.request.user)
            logger.info(f"Patient created for user {self.request.user.username}")
        except DatabaseError as db_err:
            logger.error(f"Database error in perform_create: {db_err}")
            raise
        except Exception as ex:
            logger.error(f"Unexpected error in perform_create: {ex}")
            raise

