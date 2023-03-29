from rest_framework import serializers

from course.models import Course, Student, Teacher

from authentication.serializers import UserInfoSerializer



class CourseSerializer(serializers.ModelSerializer):
    created_by = UserInfoSerializer(read_only=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'code',
            'description',
            'preview_pic',
            'section',
            'subject',
            'room',
            'created_by',
            'created_at',
            'modified_at',
        ]


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'section',
            'subject',
            'room',
        ]
    
    def create(self, validated_data):
        user = self.context['user']
        course = Course.objects.create(**validated_data, created_by=user)
        course.save()
        return course
        
