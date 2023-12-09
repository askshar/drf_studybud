from django.utils.timesince import timesince
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Room, Message


class MessageSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ("id", "user_detail", "room", "body", "created_at", "updated_at")
        read_only_fields = ("user", "user_detail", "created_at", "updated_at")

    def get_user_detail(self, obj):
        user = obj.user
        return UserSerializer(user).data
    
    def get_created_at(self, obj):
        return timesince(obj.created)
    
    def get_updated_at(self, obj):
        return timesince(obj.updated)



class RoomSerializer(serializers.ModelSerializer):
    host_user = serializers.SerializerMethodField(read_only=True)
    messages = serializers.SerializerMethodField(read_only=True)
    # topic = serializers.CharField(source="topic.name")

    class Meta:
        model = Room
        fields = ["id", "host", "host_user", "topic", "name", "description", "messages"]
        read_only_fields = ["host",]
    
    def get_host_user(self, obj):
        user = obj.host
        return UserSerializer(user).data
    
    def get_messages(self, obj):
        messages = obj.room_messages.all()
        return MessageSerializer(messages, many=True).data
