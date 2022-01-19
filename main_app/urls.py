from django.urls import path
from main_app import views as main_app

app_name = 'main_app'

urlpatterns = [
    path('', main_app.Index.as_view(), name='index'),
    path('question/<int:pk>/', main_app.QuestionView.as_view(),
         name='question'),
]
