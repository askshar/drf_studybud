from rest_framework import viewsets

from . import models, serializers, permissions, filters


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsHostOrReadOnly]
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    filterset_class = filters.RoomFilter

    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data["host"] = user
        return super().perform_create(serializer)
    

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.MessagePermissions]
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        room_id = self.request.query_params.get('room')
        queryset = queryset.filter(room__id=room_id) if room_id else queryset
        return queryset
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data["user"] = user
        return super().perform_create(serializer)
    