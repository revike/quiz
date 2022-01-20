from django.urls import path
from main_app import views as main_app

app_name = 'main_app'

urlpatterns = [
    path('', main_app.IndexView.as_view(), name='index'),
    path('start/<int:pk>/', main_app.QuizStartView.as_view(), name='start'),
    path('question/<int:pk>/', main_app.QuestionView.as_view(),
         name='question'),
    path('result/', main_app.ResultView.as_view(), name='result'),
    path('error/', main_app.ErrorView.as_view(), name='error'),
]
