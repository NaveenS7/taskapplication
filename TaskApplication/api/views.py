from django.shortcuts import render
from api.serializers import UserSerializer,TaskSerializer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from todos.models import Tasks
from rest_framework import authentication,permissions
from rest_framework.response import Response


# Create your views here.



class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    model=User
    queryset=User.objects.all()

class TaskView(ModelViewSet):
    serializer_class=TaskSerializer
    model=Tasks
    queryset=Tasks.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    http_method_names=["get","post"]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def list(self, request, *args, **kwargs):
        qs=Tasks.objects.filter(user=request.user)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)  
        

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user




class TaskdetailsView(GenericViewSet,mixins.DestroyModelMixin):
    serializer_class=TaskSerializer
    queryset=Tasks.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwnerOrReadOnly]

    http_method_names=["delete","put"]

    # def destroy(self, request, *args, **kwargs):
    #     id=kwargs.get("pk")
    #     obj=Tasks.objects.get(id=id)
    #     print(obj.user)
    #     print(request.user)
    #     if obj.user==request.user:
    #         return super().destroy(request,*args,**kwargs)
    #     else:
    #         return Response(data="not able to perform this operation")        
