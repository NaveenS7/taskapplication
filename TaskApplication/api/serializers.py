from rest_framework import serializers
from todos.models import Tasks
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password"]


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class TaskSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)

    class Meta:
        model=Tasks
        fields=["id","task_name","user","date","status"]   