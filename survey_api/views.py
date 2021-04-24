from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Survey, Questions, UserAnswer
from .serializers import SurveySerializer, SurveyUserSerializer, QuestionsSerializer, UserAnswerCreateSerializer, \
    UserAnswerSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

import datetime


def survey_update():
    Survey.objects.filter(endDate__lt=datetime.date.today()).update(status=False)
    Survey.objects.filter(startDate__lt=datetime.date.today()).update(status=True)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'That username has already been taken. Please choose another name.'},
                                status=400)
    else:
        return JsonResponse({'error': 'Need the method POST'}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            JsonResponse({'error': 'Cold not login. Please check username and password'},
                         status=400)
        else:
            try:
                token = Token.objects.get(user=user)
            except ValueError:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
    else:
        return JsonResponse({'error': 'Need the method POST'}, status=400)


class SurveyView(generics.ListCreateAPIView):
    serializer_class = SurveySerializer

    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        survey_update()
        return Survey.objects.all()


class SurveyUserView(generics.ListAPIView):
    serializer_class = SurveyUserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        survey_update()
        return Survey.objects.filter(status=True)


class SurveyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SurveySerializer

    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        survey_update()
        return Survey.objects.all()

    def perform_destroy(self, instance):
        if instance.status:
            raise ValidationError('You can not delete an active survey!')
        return instance.delete()


class QuestionsView(generics.ListCreateAPIView):
    serializer_class = QuestionsSerializer

    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        survey_update()
        survey = Survey.objects.get(pk=self.kwargs['survey'])
        return Questions.objects.filter(survey=survey)

    def perform_create(self, serializer):
        survey = Survey.objects.get(pk=self.kwargs['survey'])
        serializer.save(survey=survey)


class QuestionsUserView(generics.ListAPIView):
    serializer_class = QuestionsSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        survey_update()
        survey = Survey.objects.get(pk=self.kwargs['survey'])
        return Questions.objects.filter(survey=survey)


class QuestionsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionsSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        survey_update()
        return Questions.objects.all()

    def perform_destroy(self, instance):
        data = Survey.objects.filter(name=instance.survey).values('status')[0]
        if data['status']:
            raise ValidationError('You can not delete a question of active survey!')
        instance.delete()


class UserAnswerCreateView(generics.CreateAPIView):
    serializer_class = UserAnswerCreateSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        survey_update()
        survey = Survey.objects.get(pk=self.kwargs['survey'])
        question = Questions.objects.get(pk=self.kwargs['question'])
        return UserAnswer.objects.filter(survey=survey, question=question)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have answered this question yet!')

        user = self.request.user
        survey = Survey.objects.get(pk=self.kwargs['survey'])
        question = Questions.objects.get(pk=self.kwargs['question'])
        serializer.save(user=user, survey=survey, question=question)


class UserAnswerView(generics.ListAPIView):
    serializer_class = UserAnswerSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        survey_update()
        user = self.request.user
        return UserAnswer.objects.filter(user=user)
