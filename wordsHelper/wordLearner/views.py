from rest_framework import viewsets
from .models import Language
from .models import Mood
from .serializers import LanguageSerializer
from .serializers import MoodSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class MoodViewSet(viewsets.ModelViewSet):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer