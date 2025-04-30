from rest_framework import serializers
from .models import User, Post


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_id', 'created_at', 'updated_at']
        read_only_fields = ['author_id', 'created_at', 'updated_at']

