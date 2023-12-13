from django.shortcuts import get_object_or_404

from rest_framework import viewsets, decorators, status, response
from rest_framework import permissions as dj_permissions

from . import models, serializers, permissions, filters


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsHostOrReadOnly]
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    filterset_class = filters.RoomFilter

    
    @decorators.action(detail=True, methods=["post"],
                       permission_classes=[dj_permissions.IsAuthenticated])
    def join_room(self, request, pk=None):
        obj = get_object_or_404(models.Room, pk=pk)
        user = request.user
        message = ""
        if not obj.participants.filter(id=user.id).exists():
            obj.participants.add(user)
            message = "Room joined."
        else:
            if user == obj.host:
                return response.Response({"host": "Room host can not leave room."},
                                status=status.HTTP_400_BAD_REQUEST)
            obj.participants.remove(user)
            message = "Room left."
        return response.Response({"success": message}, status=status.HTTP_200_OK)
    

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
    