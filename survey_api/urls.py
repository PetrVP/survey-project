from django.urls import path, include
from .views import SurveyView, SurveyUserView, QuestionsView, QuestionsUserView, UserAnswerCreateView, UserAnswerView, \
    SurveyRetrieveUpdateDestroy, QuestionsRetrieveUpdateDestroy, signup, login

urlpatterns = [
    path('survey/', SurveyView.as_view()),
    path('survey/<int:pk>/', SurveyRetrieveUpdateDestroy.as_view()),
    path('survey/<int:survey>/questions/', QuestionsView.as_view()),
    path('survey/<int:survey>/questions/<int:pk>/', QuestionsRetrieveUpdateDestroy.as_view()),
    path('user/', UserAnswerView.as_view()),
    path('user/survey/', SurveyUserView.as_view()),
    path('user/survey/<int:survey>/', QuestionsUserView.as_view()),
    path('user/survey/<int:survey>/<int:question>/', UserAnswerCreateView.as_view()),
    path('signup/', signup),
    path('login/', login),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
