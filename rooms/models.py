from django.db import models

from users.models import User


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Topic(TimeStampModel):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"



class Room(TimeStampModel):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rooms")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name="topic_rooms")
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ['-id',]
    
    

class Message(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_messages")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_messages")
    body = models.TextField()

    def __str__(self) -> str:
        return self.body[:25]

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-id',]
