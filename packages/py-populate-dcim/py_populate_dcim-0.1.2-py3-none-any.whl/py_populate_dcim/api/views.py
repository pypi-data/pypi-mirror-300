# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication

from py_populate_dcim.api.models import RefreshRequest
from .serializers import RefreshRequestSerializer


class RefreshRequestViewSet(ModelViewSet):
    """API viewset for triggering refresh of Etherflow's Python Populate DCIM program."""

    authentication_classes=[BasicAuthentication]
    queryset = RefreshRequest.objects.all()
    serializer_class = RefreshRequestSerializer
    parser_classes = [FormParser]
    
    # def post(self, request, format=None):
    #     return Response({'received data': request.data})
