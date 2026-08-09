from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from api.maritime_models import MaritimeCourse, MaritimeEnrollment
from api.maritime_serializers import MaritimeCourseSerializer, MaritimeEnrollmentSerializer


class MaritimeCourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for Maritime Academy courses.
    Supports filtering by track.
    """
    
    queryset = MaritimeCourse.objects.all()
    serializer_class = MaritimeCourseSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['track']
    ordering_fields = ['order', 'created_at', 'title']
    ordering = ['track', 'order']
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_track(self, request):
        """Get courses filtered by track."""
        track = request.query_params.get('track')
        if not track:
            return Response({'error': 'track parameter required'}, status=400)
        
        courses = self.queryset.filter(track=track)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)


class MaritimeEnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Maritime Academy enrollments.
    Users can only view/edit their own enrollments.
    """
    
    serializer_class = MaritimeEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['enrolled_at', 'status']
    ordering = ['-enrolled_at']
    
    def get_queryset(self):
        """Users can only see their own enrollments (admins see all)."""
        user = self.request.user
        if user.is_staff:
            return MaritimeEnrollment.objects.all()
        return MaritimeEnrollment.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Automatically set user from request."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_enrollments(self, request):
        """Get current user's enrollments."""
        enrollments = self.get_queryset()
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark an enrollment as completed."""
        enrollment = self.get_object()
        if enrollment.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Cannot complete other users enrollments'},
                status=403
            )
        enrollment.status = 'completed'
        enrollment.save()
        return Response(self.get_serializer(enrollment).data)
