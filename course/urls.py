from rest_framework.routers import DefaultRouter

from course import views

app_name = 'course'

router = DefaultRouter()
router.register('courses', views.CourseModelViewSet, basename='course')

urlpatterns = router.urls