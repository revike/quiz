from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView

from main_app.models import Question, Choice, Quiz
from quiz.dto import QuestionDTO, ChoiceDTO, AnswerDTO, QuizDTO, AnswersDTO
from quiz.services import QuizResultService


class IndexView(ListView):
    """Главная страница опросов"""
    template_name = 'main_app/index.html'
    model = Quiz

    def get_context_data(self, *, object_list=None, **kwargs):
        Session.objects.all().delete()
        context = super().get_context_data(**kwargs)
        context['title'] = 'главная'
        return context


class QuizStartView(DetailView):
    """Страница старта"""
    template_name = 'main_app/start.html'
    model = Quiz

    def get_context_data(self, **kwargs):
        Session.objects.all().delete()
        quiz = self.object
        self.request.session['quiz_id'] = quiz.id
        self.request.session['quiz_title'] = quiz.title
        random_quest = Question.objects.filter(
            right_choices=1, quiz_id=quiz.id).order_by('?')[:1].first()
        context = super().get_context_data(**kwargs)
        context['random_quest'] = random_quest
        context['title'] = 'старт'
        return context

    def get(self, request, *args, **kwargs):
        questions = Question.objects.filter(quiz_id=kwargs['pk'])
        if questions.filter(right_choices=1).count() < 3 and questions.filter(
                right_choices=2).count() < 2:
            return HttpResponseRedirect(reverse('main_app:error'))
        i = 0
        k = 0
        for question in questions:
            choice = Choice.objects.filter(question__quiz=kwargs['pk'],
                                           question_id=question.id)
            choice_true_1 = choice.filter(is_correct=True,
                                          question__right_choices=1).count()
            choice_false_3 = choice.filter(is_correct=False,
                                           question__right_choices=1).count()
            if choice_true_1 >= 1 and choice_false_3 >= 3:
                i += 1
            choice_true_2 = choice.filter(is_correct=True,
                                          question__right_choices=2).count()
            choice_false_2 = choice.filter(is_correct=False,
                                           question__right_choices=2).count()
            if choice_true_2 >= 2 and choice_false_2 >= 2:
                k += 1
        if i + k < 5:
            return HttpResponseRedirect(reverse('main_app:error'))
        QuestionView.choice_dto.clear()
        QuestionView.question_dto.clear()
        QuestionView.answer_dto.clear()
        return super().get(self.request)


class QuestionView(DetailView):
    """Вопросы"""
    template_name = 'main_app/question.html'
    model = Question
    choice_dto = []
    question_dto = []
    answer_dto = []

    def get(self, request, *args, **kwargs):
        start = request.META.get('HTTP_REFERER')
        if start is None:
            self.choice_dto.clear()
            self.question_dto.clear()
            self.answer_dto.clear()
            return HttpResponseRedirect(reverse('main_app:index'))
        return super().get(self.request)

    def get_context_data(self, **kwargs):
        finish = 0
        len_question_dto = len(self.question_dto)
        question = self.object
        choice_data = Choice.objects.filter(question_id=question)
        right_choices = 1

        choices = []

        def add_dto():
            for choice in choices:
                self.choice_dto.append(
                    ChoiceDTO(choice.id, choice.text, choice.is_correct))
            self.question_dto.append(
                QuestionDTO(question.id, question.text, self.choice_dto[-4:]))

        if len_question_dto > 2:
            right_choices = 2

        choices_right = choice_data.filter(
            is_correct=True)[:4 - right_choices]
        choices_not_right = choice_data.filter(
            is_correct=False)[:4 - right_choices]
        choices += choices_not_right

        if len_question_dto == 0:
            choices.insert(1, choices_right[0])
        elif len_question_dto == 1 or len_question_dto == 2:
            choices.insert(0, choices_right[0])
        elif len_question_dto == 3:
            choices += choices_right
        elif len_question_dto == 4:
            choices.insert(0, choices_right[0])
            choices.insert(2, choices_right[1])

        add_dto()
        if len_question_dto > 1:
            right_choices = 2

        quest_uuid = [i.uuid for i in self.question_dto]

        next_quest = Question.objects.filter(
            right_choices=right_choices).exclude(id__in=quest_uuid).order_by(
            '?')[:1].first()

        if len_question_dto < 4:
            self.request.session['next_quest'] = next_quest.id
            finish = 1
            self.request.session['finish'] = False
        else:
            self.request.session['finish'] = True
        try:
            choice_data = {
                'A': choices[0],
                'B': choices[1],
                'C': choices[2],
                'D': choices[3]
            }
        except IndexError:
            choice_data = 0
        context = super().get_context_data(**kwargs)
        context['finish'] = finish
        context['next_quest'] = next_quest
        context['choices'] = choice_data
        context['title'] = 'quiz'
        return context

    def post(self, request, *args, **kwargs):
        question_id = kwargs['pk']
        choices = []
        next_quest = self.request.session['next_quest']
        choices.append(self.request.POST.get('A'))
        choices.append(self.request.POST.get('B'))
        choices.append(self.request.POST.get('C'))
        choices.append(self.request.POST.get('D'))
        self.answer_dto.append(AnswerDTO(question_id, choices))
        try:
            if self.question_dto[-1].uuid != self.answer_dto[-1].question_uuid:
                self.question_dto.pop(-1)
                self.answer_dto.pop(-2)
            if len(self.question_dto) != len(self.answer_dto):
                self.question_dto.pop(-1)
        except IndexError:
            HttpResponseRedirect(reverse('main_app:index'))

        if self.request.session.get('finish'):
            quiz = self.request.session
            quizzes = QuizDTO(quiz['quiz_id'], quiz['quiz_title'],
                              self.question_dto)
            answers = AnswersDTO(quiz['quiz_id'], self.answer_dto)
            result = QuizResultService(quizzes, answers).get_result()
            self.request.session['result'] = result
            self.request.session['answers'] = answers
            return HttpResponseRedirect(reverse('main_app:result'))
        return HttpResponseRedirect(
            reverse('main_app:question', args=[next_quest]))


class ResultView(TemplateView):
    """Результат"""
    template_name = 'main_app/result.html'

    def get_context_data(self, **kwargs):
        result = self.request.session['result']
        # print(self.request.session['answers'])
        context = super().get_context_data(**kwargs)
        context['result'] = float(result * 100)
        context['title'] = 'результат'
        return context

    def get(self, request, *args, **kwargs):
        start = request.META.get('HTTP_REFERER')
        if start is None:
            return HttpResponseRedirect(reverse('main_app:index'))
        return super().get(self.request, **kwargs)


class ErrorView(TemplateView):
    """Неготовый Опрос"""
    template_name = 'main_app/error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'не готов'
        return context
