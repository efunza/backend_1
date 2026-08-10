from django.db import models
from django.conf import settings
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MaritimeCourse(TimeStampedModel):
    """Maritime Academy Course model

    Extended with slug, cover image, published flag and optional
    text_content field that can be used by AI endpoints.
    """

    TRACK_CHOICES = (
        ('deck', 'Deck Officer'),
        ('engine', 'Engine Officer'),
        ('rating', 'Rating'),
        ('general', 'General Maritime'),
    )

    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    credits = models.PositiveIntegerField(default=3)
    duration_weeks = models.PositiveIntegerField(default=12)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    text_content = models.TextField(blank=True, help_text='Optional extracted/plain text used by AI features')
    outcomes = models.JSONField(default=list, blank=True)  # List of learning outcomes
    track = models.CharField(max_length=20, choices=TRACK_CHOICES, default='general')
    order = models.PositiveIntegerField(default=0)  # For ordering within a track
    cover_image = models.ImageField(upload_to='maritime/covers/', null=True, blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['track', 'order', 'code']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:50]
            slug = base
            counter = 1
            while MaritimeCourse.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.title}"


class MaritimeMaterial(TimeStampedModel):
    """Files and supporting materials for a course."""

    FILE_TYPE_CHOICES = (
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('archive', 'Archive'),
        ('other', 'Other'),
    )

    course = models.ForeignKey(MaritimeCourse, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='maritime/materials/')
    file_type = models.CharField(max_length=32, choices=FILE_TYPE_CHOICES, default='other')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class MaritimeSession(TimeStampedModel):
    """Scheduled live session for a course (join_url can be Jitsi/Zoom link)."""

    course = models.ForeignKey(MaritimeCourse, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    join_url = models.URLField(blank=True)
    recording_url = models.URLField(blank=True)
    is_recurring = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.course.code} - {self.title} @ {self.start_time}"