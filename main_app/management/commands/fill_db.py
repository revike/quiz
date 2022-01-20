import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from main_app.models import Quiz, Question, Choice

JSON_PATH = os.path.join(settings.BASE_DIR, 'main_app/json')


def load_json_data(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'),
              encoding='utf-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        quizzes = load_json_data('quizzes')
        Quiz.objects.all().delete()
        for quiz in quizzes:
            Quiz.objects.create(**quiz)

        questions = load_json_data('questions')
        Question.objects.all().delete()
        for question in questions:
            quiz = question['quiz']
            _quiz = Quiz.objects.get(title=quiz)
            question['quiz'] = _quiz
            print('*' * 10)
            print(question)
            Question.objects.create(**question)

        choices = load_json_data('choices')
        Choice.objects.all().delete()
        for choice in choices:
            question = choice['question']
            _question = Question.objects.get(text=question)
            choice['question'] = _question
            Choice.objects.create(**choice)

        User.objects.filter(is_staff=True, is_superuser=True).delete()
        User.objects.create_superuser(
            'admin', 'admin@admin.local', 'admin')
