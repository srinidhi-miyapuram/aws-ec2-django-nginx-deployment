from django.contrib.auth.models import User
from django.db import models
class Task(models.Model):
    class Priority(models.TextChoices):
        LOW="LOW","Low"
        MEDIUM="MEDIUM","Medium"
        HIGH="HIGH","High"
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="tasks")
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    priority=models.CharField(max_length=10,choices=Priority.choices,default=Priority.MEDIUM)
    due_date=models.DateField(null=True,blank=True)
    completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=["completed","-created_at"]
    def __str__(self): return self.title
