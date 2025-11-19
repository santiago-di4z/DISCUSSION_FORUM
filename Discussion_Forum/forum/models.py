from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# - - - - - - BOARD  - - - - - - #
class Board(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.short_name}) - {self.id}"

# - - - - - - THREAD  - - - - - - #
class Thread(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="threads")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads")
    title = models.CharField(max_length=225)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.board.short_name}) - {self.id}"
    
    class Meta:
        ordering = ['-created_at'] # Default: newest first

# - - - - - - COMMENT  - - - - - - #
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment ({self.id}) by {self.user} on Thread {self.thread.id}"

    class Meta:
        ordering = ['created_at']
