from rest_framework import viewsets
from users.serializers import ModuleSerializer
from users.models import Module

"""
ReadOnlyModelViewSet is used when dealing with catalogs and no write operations are required
"""
class ModuleCatalogView(viewsets.ReadOnlyModelViewSet):
    
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    