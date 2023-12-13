from django.utils.timesince import timesince
from rest_framework import serializers

from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import Room, Message

User = get_user_model()


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
    host_user = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    # topic = serializers.CharField(source="topic.name")
    participant_details = serializers.SerializerMethodField()
    total_participants = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["id", "host", "host_user", "topic",
                  "name", "description", "messages",
                  "participants", "participant_details",
                  "total_participants"]
        read_only_fields = ["host", "host_user", "messages",
                            "participant_details", "total_participants"]

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data['host'] = user
        obj = super().create(validated_data)
        obj.participants.add(user)
        return obj
    
    def get_host_user(self, obj):
        user = obj.host
        return UserSerializer(user).data
    
    def get_messages(self, obj):
        messages = obj.room_messages.all()
        return MessageSerializer(messages, many=True).data

    def get_participant_details(self, obj):
        participants = obj.participants.prefetch_related()
        p_details = [
            {"id": participant.id, "email": participant.email}
            for participant in participants
        ]
        return p_details

    
    def get_total_participants(self, obj):
        return obj.participants.count()
