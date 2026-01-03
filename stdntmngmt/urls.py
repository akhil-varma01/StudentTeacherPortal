from django.urls import path
from .views import *


urlpatterns = [
# ✅ Student Management Endpoints
    path('register/', RegisterAPIView.as_view(), name='student-register'),
    path('login/', StudentLoginAPIView.as_view(), name='student-login'),
    path('student-create/', StudentCreateAPIView.as_view(), name='student-create'),
    path('students/', StudentListAPIView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentRetrieveAPIView.as_view(), name='student-retrieve'),
    path('students/update/<int:pk>/', StudentUpdateAPIView.as_view(), name='student-update'),
    path('students/delete/<int:pk>/', StudentDeleteAPIView.as_view(), name='student-delete'),

# ✅ To-Do Endpoints
    path('todos/<int:student_id>/', TodoListCreateAPIView.as_view(), name='todo-list-create'),
    path('todos/update/<int:pk>/', TodoUpdateAPIView.as_view(), name='todo-update'),
    path('todos/delete/<int:pk>/', TodoDeleteAPIView.as_view(), name='todo-delete'),
    path('todos/get/<int:pk>/', TodoRetrieveAPIView.as_view(), name="todo-get"),
    path('todos/toggle-complete/<int:pk>/', TodoToggleCompleteAPIView.as_view(), name="todo-toggle"),

# ✅ Task Endpoints
    path("api/admin/login/", AdminLoginAPIView.as_view(), name="api-admin-login"),
    path("api/admin/tasks/", TaskListAPIView.as_view()),
    path("api/admin/tasks/create/", TaskCreateAPIView.as_view()),
    path("api/admin/tasks/update/<int:pk>/", TaskUpdateAPIView.as_view()),
    path("api/admin/tasks/delete/<int:pk>/", TaskDeleteAPIView.as_view()),

    # user tasks
    path("tasks/<int:user_id>/", UserTaskListAPIView.as_view()),
]
