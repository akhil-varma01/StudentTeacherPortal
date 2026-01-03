from django.contrib import admin

# Register your models here.
from .models import Student, Todo, Task, Admin
admin .site.register(Student)
admin.site.register(Todo)
admin.site.register(Task)
admin.site.register(Admin)