from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Note
from .serializers import UserRegisterSerializer, UserSerializer, NoteSerializer


# PUBLIC_INTERFACE
@swagger_auto_schema(method='get', operation_summary="Health check", operation_description="Returns server status.")
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health(request):
    """Simple health-check endpoint."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='post',
    operation_summary="User registration",
    operation_description="Register a new user with username, email, and password.",
    request_body=UserRegisterSerializer,
    responses={201: UserSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def register(request):
    """
    Register a new user.

    Body:
    - username: string
    - email: string
    - password: string

    Returns created user data (without password).
    """
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='post',
    operation_summary="Login",
    operation_description="Login with username and password using session authentication.",
    manual_parameters=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        }
    ),
    responses={200: openapi.Response(description="Logged in", schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'message': openapi.Schema(type=openapi.TYPE_STRING), 'user': openapi.Schema(type=openapi.TYPE_OBJECT)}
    ))}
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@csrf_exempt
def login_view(request):
    """
    Login a user and create a session cookie.

    Body:
    - username
    - password
    """
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"detail": "username and password required."}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    login(request, user)
    return Response({"message": "Logged in", "user": UserSerializer(user).data})


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='post',
    operation_summary="Logout",
    operation_description="Logout current user (session).",
    responses={200: openapi.Response(description="Logged out")}
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def logout_view(request):
    """Logout the current user by clearing the session."""
    logout(request)
    return Response({"message": "Logged out"})


class IsOwner(permissions.BasePermission):
    """Allow access only to owners of the object."""
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "owner") and obj.owner == request.user


# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """CRUD API for Notes. Only authenticated users can access. Users can only access their own notes."""
    serializer_class = NoteSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by("-updated_at", "-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(operation_summary="List notes", operation_description="List notes for the authenticated user.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create note", operation_description="Create a note for the authenticated user.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve note", operation_description="Retrieve a single note by ID.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update note", operation_description="Update a note by ID.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Partial update note", operation_description="Partially update a note by ID.")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete note", operation_description="Delete a note by ID.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
