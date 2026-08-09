from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MaritimeCourse(TimeStampedModel):
    """Maritime Academy Course model"""
    
    TRACK_CHOICES = (
        ('deck', 'Deck Officer'),
        ('engine', 'Engine Officer'),
        ('rating', 'Rating'),
        ('general', 'General Maritime'),
    )
    
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    credits = models.PositiveIntegerField(default=3)
    duration_weeks = models.PositiveIntegerField(default=12)
    summary = models.TextField(blank=True)
    outcomes = models.JSONField(default=list, blank=True)  # List of learning outcomes
    track = models.CharField(max_length=20, choices=TRACK_CHOICES, default='general')
    order = models.PositiveIntegerField(default=0)  # For ordering within a track
    
    class Meta:
        ordering = ['track', 'order', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.title}"


class MaritimeEnrollment(TimeStampedModel):
    """Maritime Academy Enrollment model"""
    
    STATUS_CHOICES = (
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maritime_enrollments')
    course = models.ForeignKey(MaritimeCourse, on_delete=models.CASCADE, related_name='enrollments')
    track = models.CharField(max_length=20, choices=MaritimeCourse.TRACK_CHOICES, default='general')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.code} ({self.status})"
