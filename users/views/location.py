"""
location.py
~~~~~~~~~~~
This module defines APIs for managing Location objects.
"""

import logging
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import DatabaseError
from users.models import Location
from users.serializers.location_serializer import LocationSerializer

logger = logging.getLogger(__name__)


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Location objects.

    Public Methods
    --------------
    list(request, *args, **kwargs)
        Retrieve a paginated list of locations.

    create(request, *args, **kwargs)
        Create a new location entry.

    Attributes
    ----------
    queryset : QuerySet
        All `Location` objects.
    serializer_class : Serializer
        Serializer used for validation and transformation.
    permission_classes : list
        Permissions required for accessing this API.
    pagination_class : PageNumberPagination
        Built-in pagination strategy.

    Raises
    ------
    DatabaseError
        If database query fails during list or create.
    ValidationError
        If input data is invalid during creation.

    Notes
    -----
    - Only GET (list) and POST (create) methods are allowed.
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    # http_method_names = ["get", "post"]

    def list(self, request, *args, **kwargs):
        """
        Retrieve a paginated list of locations.

        Steps
        -----
        1. Log the request for fetching locations.
        2. Query all Location objects.
        3. Paginate the queryset.
        4. Serialize paginated data.
        5. Return serialized response.

        Returns
        -------
        Response
            Paginated list of locations.
        """
        try:
            logger.info("Fetching list of locations...")
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger.info("Locations fetched successfully with pagination.")
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DatabaseError as db_err:
            logger.error(f"Database error while fetching locations: {db_err}")
            return Response(
                {"detail": "Database error while fetching locations."},
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
        Create a new location entry.

        Steps
        -----
        1. Log the request for creating a new location.
        2. Validate request data with serializer.
        3. Save the location object if valid.
        4. Return success response with created data.

        Arguments
        ---------
        request : Request
            The HTTP request containing location data.

        Returns
        -------
        Response
            JSON response with created location or validation errors.
        """
        try:
            logger.info("Creating a new location...")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                location = serializer.save()
                logger.info(f"Location created successfully: {location.id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.warning(f"Validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as db_err:
            logger.error(f"Database error while creating location: {db_err}")
            return Response(
                {"detail": "Database error while creating location."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as ex:
            logger.error(f"Unexpected error in create: {ex}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
