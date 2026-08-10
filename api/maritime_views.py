from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.conf import settings

from api.maritime_models import MaritimeCourse, MaritimeEnrollment, MaritimeMaterial, MaritimeSession
from api.maritime_serializers import (
    MaritimeCourseSerializer, MaritimeEnrollmentSerializer,
    MaritimeMaterialSerializer, MaritimeSessionSerializer
)

from api.views import AIChatView  # reuse internal AI view logic via dispatch


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class MaritimeCourseViewSet(viewsets.ModelViewSet):
    """Full CRUD for Maritime courses (create/update/delete restricted to staff)."""

    queryset = MaritimeCourse.objects.all()
    serializer_class = MaritimeCourseSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['track', 'is_published']
    ordering_fields = ['order', 'created_at', 'title']
    ordering = ['track', 'order']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related(
            Prefetch('materials', queryset=MaritimeMaterial.objects.all()),
            Prefetch('sessions', queryset=MaritimeSession.objects.all()),
        )

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_track(self, request):
        track = request.query_params.get('track')
        if not track:
            return Response({'error': 'track parameter required'}, status=400)
        courses = self.get_queryset().filter(track=track, is_published=True)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ai_summary(self, request, pk=None):
        """Generate an AI summary for the course using the internal AI endpoint."""
        course = self.get_object()
        # Assemble text context: course.description + text_content + small sample from materials if text
        text = (course.description or '') + '\n\n' + (course.text_content or '')
        # For safety, truncate to a reasonable length
        text = text[:12000]
        payload = {
            'mode': 'readathon',
            'task': 'summarize',
            'book_title': course.title,
            'text': text,
        }
        # Use AIChatView.post logic by instantiating and calling
        ai_view = AIChatView()
        ai_request = request
        ai_request.data._mutable = True
        ai_request.data.update(payload)
        ai_request.data._mutable = False
        ai_resp = ai_view.post(ai_request)
        return ai_resp

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ai_quiz(self, request, pk=None):
        course = self.get_object()
        text = (course.description or '') + '\n\n' + (course.text_content or '')
        text = text[:12000]
        payload = {
            'mode': 'readathon',
            'task': 'generate_quiz',
            'book_title': course.title,
            'text': text,
        }
        ai_view = AIChatView()
        ai_request = request
        ai_request.data._mutable = True
        ai_request.data.update(payload)
        ai_request.data._mutable = False
        ai_resp = ai_view.post(ai_request)
        return ai_resp

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ai_ask(self, request, pk=None):
        question = request.data.get('question', '')
        course = self.get_object()
        context_text = (course.description or '') + '\n\n' + (course.text_content or '')
        payload = {
            'mode': 'readathon',
            'task': 'ask_ai',
            'question': question,
            'text': context_text[:12000],
        }
        ai_view = AIChatView()
        ai_request = request
        ai_request.data._mutable = True
        ai_request.data.update(payload)
        ai_request.data._mutable = False
        ai_resp = ai_view.post(ai_request)
        return ai_resp


class MaritimeMaterialViewSet(viewsets.ModelViewSet):
    """Upload and manage materials. Uploads are multipart/form-data."""

    queryset = MaritimeMaterial.objects.all()
    serializer_class = MaritimeMaterialSerializer
    permission_classes = [IsStaffOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Validate file size
        max_size = int(getattr(settings, 'MAX_UPLOAD_SIZE', 104_857_600))  # 100MB
        f = self.request.FILES.get('file')
        if f and f.size > max_size:
            raise serializers.ValidationError({'file': 'File too large'})
        serializer.save(uploaded_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get('course')
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs.select_related('uploaded_by', 'course')


class MaritimeSessionViewSet(viewsets.ModelViewSet):
    queryset = MaritimeSession.objects.all()
    serializer_class = MaritimeSessionSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get('course')
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs.select_related('course')


class MaritimeEnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = MaritimeEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MaritimeEnrollment.objects.all()
        return MaritimeEnrollment.objects.filter(user=user)

    def perform_create(self, serializer):
        # Prevent duplicate enrollments
        course = serializer.validated_data.get('course')
        if MaritimeEnrollment.objects.filter(user=self.request.user, course=course).exists():
            raise serializers.ValidationError({'detail': 'Already enrolled in this course'})
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_enrollments(self, request):
        enrollments = self.get_queryset()
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)
