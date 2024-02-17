from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer

# Create your views here.
class ProjectsViewSet(GenericViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    template_name = 'projects_list.htm'
    renderer_classes = [TemplateHTMLRenderer]

    @action(methods=['get'], detail=False, url_path="get-all")
    def get_all(self, request):
        return Response({"projects": self.queryset})
        #serializer = self.get_serializer(self.queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path="get-done")
    def get_done(self, request):
        queryset = self.queryset.filter(status="Done")
        #serializer = self.get_serializer(queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"projects": queryset})
