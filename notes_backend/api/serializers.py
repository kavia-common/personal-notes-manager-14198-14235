from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note


# PUBLIC_INTERFACE
class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration input and creation."""
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        # Create user with proper password hashing
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )


# PUBLIC_INTERFACE
class UserSerializer(serializers.ModelSerializer):
    """Serializer for returning simple user info."""
    class Meta:
        model = User
        fields = ("id", "username", "email")


# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model, owner is read-only username."""
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Note
        fields = ("id", "title", "content", "created_at", "updated_at", "owner")
        read_only_fields = ("id", "created_at", "updated_at", "owner")
