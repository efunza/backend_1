from rest_framework import serializers
from api.maritime_models import MaritimeCourse, MaritimeEnrollment


class MaritimeCourseSerializer(serializers.ModelSerializer):
    """Serializer for Maritime Academy courses."""
    
    class Meta:
        model = MaritimeCourse
        fields = [
            'id',
            'code',
            'title',
            'credits',
            'duration_weeks',
            'summary',
            'outcomes',
            'track',
            'order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MaritimeEnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Maritime Academy enrollments."""
    
    user_display = serializers.StringRelatedField(source='user', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = MaritimeEnrollment
        fields = [
            'id',
            'user',
            'user_display',
            'track',
            'course',
            'course_title',
            'status',
            'enrolled_at',
            'updated_at',
            'completed_at',
        ]
        read_only_fields = ['id', 'user', 'enrolled_at', 'updated_at']
    
    def create(self, validated_data):
        """Automatically set user from request context."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
