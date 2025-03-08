from django.db import models

class Conversation(models.Model):
    sender = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.recipient} at {self.timestamp}"
