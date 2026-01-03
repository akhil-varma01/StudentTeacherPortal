from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    department = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    

class Todo(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="todos"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.student.username}"
    

# models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # NEW: assign to a specific student (nullable = assigned to ALL when null)
    assigned_to = models.ForeignKey(
        "Student",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.assigned_to:
            return f"{self.title} -> {self.assigned_to.username}"
        return f"{self.title} -> All users"



class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username
