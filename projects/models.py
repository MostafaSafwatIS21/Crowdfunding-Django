from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    details = models.TextField()
    total_target = models.DecimalField(max_digits=12, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError({
                    'end_time': 'End date and time must be after the start date and time.'
                })

    def __str__(self):
        return self.title

class Fund(models.Model):
    backer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='funds')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='funds')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    funded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.backer.first_name} funded {self.amount} to {self.project.title}"
