from dataclasses import fields

from rest_framework import serializers
from .models.language import Language
from .models.mood import Mood

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class MoodSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(source='mood_fk_language')

    class Meta:
        model = Mood
        fields = ['mood_id', 'mood_name', 'language']