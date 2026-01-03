from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Todo, Task, Admin
from .serializers import StudentSerializer, TodoSerializer, TaskSerializer, AdminSerializer


# CREATE student
class StudentCreateAPIView(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET all students
class StudentListAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# GET single student by ID
class StudentRetrieveAPIView(APIView):
    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)


# UPDATE student by ID
class StudentUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE student by ID
class StudentDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        student.delete()
        return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# STUDENT LOGIN    
class StudentLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # ✅ Check for spaces in username
        if " " in username:
            return Response({"error": "Username should not contain spaces"}, status=status.HTTP_400_BAD_REQUEST)


        # Check if username and password are provided
        if not username or not password:
            return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(username=username)
        except Student.DoesNotExist:
            return Response({"error": "Invalid username"}, status=status.HTTP_404_NOT_FOUND)

        # Basic password check (you can later hash passwords using make_password)
        if student.password != password:
            return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Success response
        return Response({
            "message": "Login successful",
            "student": {
                "id": student.id,
                "username": student.username,
                "name": student.name,
                "email": student.email,
                "department": student.department,
                "age": student.age,
                "phone": student.phone,
                "address": student.address,
            }
        }, status=status.HTTP_200_OK)


class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        phone = request.data.get('phone')
        email = request.data.get('email')
        age = request.data.get('age')
        department = request.data.get('department')
        address = request.data.get('address')

        # ✅ Username must not contain spaces
        if " " in username:
            return Response({"error": "Username should not contain spaces"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username or email already exists
        if Student.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if Student.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create new student
        student = Student.objects.create(
            username=username,
            password=password,
            name=name,
            phone=phone,
            email=email,
            age=age,
            department=department,
            address=address
        )

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ✅ To-Do APIs
class TodoListCreateAPIView(APIView):
    def get(self, request, student_id):
        """Get all todos for a specific student"""
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        todos = Todo.objects.filter(student=student)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, student_id):
        """Create a new todo for a specific student"""
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data =request.data.copy()
        data['student'] = student_id
        serializer = TodoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# UPDATE a To-Do by ID
class TodoUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# DELETE a To-Do by ID
class TodoDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
        
        todo.delete()
        return Response({"message": "Todo Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
# GET single todo by ID
class TodoRetrieveAPIView(APIView):
    def get(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo)
        return Response(serializer.data)

class TodoToggleCompleteAPIView(APIView):
    def patch(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=404)

        todo.completed = not todo.completed   # toggle value
        todo.save()

        serializer = TodoSerializer(todo)
        return Response(serializer.data)


# Admin Login API (Class Based)
class AdminLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            admin = Admin.objects.get(username=username, password=password)
            serializer = AdminSerializer(admin)
            return Response({"admin": serializer.data}, status=status.HTTP_200_OK)
        except Admin.DoesNotExist:
            return Response({"error": "Invalid admin credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    
# Create Task (Admin)
class TaskCreateAPIView(APIView):
    def post(self, request):
        data = request.data.copy()

        # If frontend sends 'assigned_to' as empty string or 'all', treat as None
        assigned_to = data.get("assigned_to", None)
        if assigned_to in ("", "all", None):
            data["assigned_to"] = None
        else:
            # validate student exists
            try:
                student = Student.objects.get(pk=int(assigned_to))
                data["assigned_to"] = student.id
            except (Student.DoesNotExist, ValueError, TypeError):
                return Response({"error": "Invalid student id for assigned_to."},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Get All Tasks (Admin)
class TaskListAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all().order_by('-created_at')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Update Task by ID
class TaskUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Task by ID
class TaskDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, 
                            status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response({"message": "Task deleted successfully"}, 
                        status=status.HTTP_200_OK)


# Get Tasks for a specific User (ALL tasks visible to everyone)
from django.db.models import Q

class UserTaskListAPIView(APIView):
    def get(self, request, user_id):
        tasks = Task.objects.filter(
            Q(assigned_to__id=user_id) | Q(assigned_to__isnull=True)
        ).order_by('-created_at')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


