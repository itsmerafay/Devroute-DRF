from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from profiles.models import UserProfile
from profiles.serializers import UserProfileSerializer, UserProfileCreateUpdateSerializer
from profiles.permissions import IsAdminOrSelf
from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)

class UserProfileListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSelf]
    
    def get(self, request):
        logger.info("Attempting to retrieve user profiles.")
        if 'my_key' in cache:
            logger.info("Cache hit: Retrieving user profiles from Redis.")
            profile_data = cache.get('my_key')
            source = "Redis Cache"
        else:
            logger.info("Cache miss: Retrieving user profiles from the database.")
            profiles = UserProfile.objects.all()
            profile_data = UserProfileSerializer(profiles, many=True).data
            cache.set('my_key', profile_data, timeout=10)  # Cache the data for future requests
            source = "Database"
        
        return Response({
            "source": source,
            "data": profile_data
        }, status=status.HTTP_200_OK)
    

class UserProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Authenticated user: {request.user}")
        logger.info(f"Request data: {request.data}")
        serializer = UserProfileCreateUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_object(self, pk):
        try:
            profile = UserProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except UserProfile.DoesNotExist:
            return Http404
        
    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = UserProfileCreateUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    
