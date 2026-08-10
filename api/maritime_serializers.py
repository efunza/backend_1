from rest_framework import serializers
from api.maritime_models import MaritimeCourse, MaritimeMaterial, MaritimeSession, MaritimeEnrollment


class MaritimeMaterialSerializer(serializers.ModelSerializer):
    uploaded_by_display = serializers.StringRelatedField(source='uploaded_by', read_only=True)

    class Meta:
        model = MaritimeMaterial
        fields = [
            'id', 'course', 'title', 'description', 'file', 'file_type', 'uploaded_by', 'uploaded_by_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'created_at', 'updated_at']


class MaritimeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritimeSession
        fields = [
            'id', 'course', 'title', 'description', 'start_time', 'end_time', 'join_url', 'recording_url', 'is_recurring', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MaritimeCourseSerializer(serializers.ModelSerializer):
    materials = MaritimeMaterialSerializer(many=True, read_only=True)
    sessions = MaritimeSessionSerializer(many=True, read_only=True)

    class Meta:
        model = MaritimeCourse
        fields = [
            'id', 'code', 'title', 'slug', 'credits', 'duration_weeks', 'summary', 'description', 'text_content',
            'outcomes', 'track', 'order', 'cover_image', 'is_published', 'materials', 'sessions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class MaritimeEnrollmentSerializer(serializers.ModelSerializer):
    user_display = serializers.StringRelatedField(source='user', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = MaritimeEnrollment
        fields = [
            'id', 'user', 'user_display', 'course', 'course_title', 'track', 'status', 'enrolled_at', 'completed_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'enrolled_at', 'updated_at']

    def create(self, validated_data):
        # Ensure user is set from context
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
