from rest_framework import routers

from .views import ProjectsViewSet

appname = "projects"

router = routers.DefaultRouter()

router.register("projects", ProjectsViewSet, basename="api-project")

urlpatterns = router.urls