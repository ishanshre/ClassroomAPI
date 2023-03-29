from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from course.models import Course, Student, Teacher
from course.serializers import (
    CourseSerializer,
    CourseCreateSerializer,
)
# Create your views here.


class CourseModelViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    http_method_names = ['get','post','put','delete','options','head']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CourseCreateSerializer
        return CourseSerializer
    
    def get_queryset(self):
        return Course.objects.filter(created_by=self.request.user)

    def get_serializer_context(self):
        return {"user":self.request.user}