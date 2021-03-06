from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import CustomUser
from .serializers import CustomUserSerializer

from projects.models import Pledge, Project, ProjectCategory
from projects.serializers import PledgeSerializer, ProjectSerializer, ProjectCategorySerializer

# Not using IsAdmin in this file. Remove it from the import unless that changes on Wednesday...
from .permissions import IsLoggedInUserOrReadOnly, IsLoggedInUser, IsAdminOrReadOnly


class CustomUserList(APIView):

    # get list of all the users.
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    # create a new user
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CustomUserDetail(APIView):

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    # get profile of a given user
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        # pledges = Pledge.objects.filter(user_id=user.id)
        # pledge_serializer = PledgeSerializer(pledges, many=True)
        # response_data = { 
        #     "user": user_serializer.data, 
        #     "pledges": pledge_serializer.data 
        # }
        # return Response(response_data)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     user = self.get_object(pk)

    #     # if you don't call check_object_permissions here, the view won't check if the user has the right permissions!
    #     self.check_object_permissions(request, user)

    #     # Have to pass in as third agrument partial=True, otherwise the serializer will require a value to be submitted for EVERY property EVERY time.
    #     serializer = CustomUserSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data) # status=200 so no need to include - it's the default.
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     user = self.get_object(pk)

    #     # if you don't call check_object_permissions here, the view won't check if the user has the right permissions!
    #     self.check_object_permissions(request, user)
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class AuthenticatedUserProfile(APIView):

    permission_classes = [IsLoggedInUser]

    def get_object(self):
        try:
            return CustomUser.objects.get(pk=self.request.user.id)
        except CustomUser.DoesNotExist:
            raise Http404

    # get profile of a logged in user
    def get(self, request):
        user = self.get_object()
        # if you don't call check_object_permissions here, the view won't check if the user has the right permissions!
        self.check_object_permissions(request, user)

        user_serializer = CustomUserSerializer(user)
        pledges = Pledge.objects.filter(user_id=user.id)
        pledge_serializer = PledgeSerializer(pledges, many=True)
        projects = Project.objects.filter(user_id=user.id)
        project_serializer = ProjectSerializer(projects, many=True)
        response_data = { 
            "user": user_serializer.data, 
            "projects": project_serializer.data, 
            "pledges": pledge_serializer.data 
        }
        return Response(response_data)

    def put(self, request):
        user = self.get_object()

        # if you don't call check_object_permissions here, the view won't check if the user has the right permissions!
        self.check_object_permissions(request, user)

        user_serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            pledges = Pledge.objects.filter(user_id=user.id)
            pledge_serializer = PledgeSerializer(pledges, many=True)
            projects = Project.objects.filter(user_id=user.id)
            project_serializer = ProjectSerializer(projects, many=True)
            response_data = { 
                "user": user_serializer.data,
                "projects": project_serializer.data, 
                "pledges": pledge_serializer.data 
            }
            return Response(response_data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.get_object()

        # if you don't call check_object_permissions here, the view won't check if the user has the right permissions!
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserAddCategory(APIView):

    permission_classes = [IsLoggedInUser]

    def get_object(self):
        try:
            return CustomUser.objects.get(pk=self.request.user.id)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object()

        # if you don't call check_object_permissions here, the view won't check if the user has the right permissions!
        self.check_object_permissions(request, user)

        cat_to_add = ProjectCategory.objects.get(pk=pk)
        user.favourite_categories.add(cat_to_add)

        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class UserRemoveCategory(APIView):
    permission_classes = [IsLoggedInUser]

    def get_object(self):
        try:
            return CustomUser.objects.get(pk=self.request.user.id)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object()

        # if you don't call check_object_permissions here, the view won't check if the user has the right permissions!
        self.check_object_permissions(request, user)

        cat_to_remove = ProjectCategory.objects.get(pk=pk)
        user.favourite_categories.remove(cat_to_remove)

        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
