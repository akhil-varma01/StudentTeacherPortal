from rest_framework import serializers
from .models import Student, Todo, Task, Admin

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': False}  # ✅ make password optional
        }


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Task
        fields = "__all__"



class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = "__all__"
