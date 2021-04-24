from rest_framework import serializers
from .models import Survey, Questions, UserAnswer
from django.contrib.auth.models import User


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class SurveySerializer(serializers.ModelSerializer):
    startDate = serializers.ReadOnlyField(source='survey.startDate')

    class Meta:
        model = Survey
        fields = ['id', 'name', 'startDate', 'endDate', 'description', 'status']


class SurveyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'name', 'startDate', 'endDate', 'description']


class QuestionsSerializer(serializers.ModelSerializer):
    survey = serializers.ReadOnlyField(source='survey.name')

    class Meta:
        model = Questions
        fields = ['id', 'survey', 'text', 'answerType', 'changeAnswer']


class UserAnswerCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='UserAnswer.user')
    survey = serializers.ReadOnlyField(source='UserAnswer.survey')
    question = serializers.ReadOnlyField(source='UserAnswer.question')

    class Meta:
        model = UserAnswer
        fields = ['id', 'user', 'survey', 'question', 'answer']


class UserAnswerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='UserAnswer.user')

    class Meta:
        model = UserAnswer
        fields = ['id', 'user', 'survey', 'question', 'answer']
