from django import forms
from .models import Task
class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=["title","description","priority","due_date","completed"]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter task title"}),
            "description":forms.Textarea(attrs={"class":"form-control","rows":4,"placeholder":"Add task details"}),
            "priority":forms.Select(attrs={"class":"form-control"}),
            "due_date":forms.DateInput(attrs={"class":"form-control","type":"date"}),
            "completed":forms.CheckboxInput(attrs={"class":"checkbox"}),
        }
