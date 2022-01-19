from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from main_app.models import Question, Choice
from quiz.dto import QuestionDTO, ChoiceDTO


class Index(TemplateView):
    """Главная страница"""
    template_name = 'main_app/index.html'
    model = Question

    def get_context_data(self, **kwargs):
        random_quest = Question.objects.filter(
            right_choices=1).order_by('?')[:1].first()
        context = super().get_context_data(**kwargs)
        context['random_quest'] = random_quest
        context['title'] = 'главная'
        next_url = self.request.META.get('HTTP_REFERER')
        print(next_url)
        return context


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
            return HttpResponseRedirect(reverse('main_app:index'))
        return super(QuestionView, self).get(self.request)

    def get_context_data(self, **kwargs):
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
            is_correct=True)[:right_choices]
        choices_not_right = choice_data.filter(
            is_correct=False)[:(4 - right_choices)]
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
        print(len_question_dto)
        if len_question_dto > 1:
            right_choices = 2

        next_quest = Question.objects.filter(
            right_choices=right_choices).order_by('?')[:1].first()

        self.request.session['next_quest'] = next_quest.id
        context = super().get_context_data(**kwargs)
        context['next_quest'] = next_quest
        context['choices'] = choices
        context['title'] = 'quiz'
        return context

    def post(self, request, *args, **kwargs):
        next_quest = self.request.session['next_quest']
        choices = self.question_dto
        print(choices)
        # print('=' * 25, self.request.POST)

        return HttpResponseRedirect(
            reverse('main_app:question', args=[next_quest]))
