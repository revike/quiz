from django.db import models


class Quiz(models.Model):
    """Модель опроса"""
    class Meta:
        verbose_name_plural = 'опросы'
        verbose_name = 'опросы'

    title = models.CharField(max_length=128, verbose_name='опрос')

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    """Модель вопросов"""

    class Meta:
        verbose_name_plural = 'вопросы'
        verbose_name = 'вопросы'

    CHOICES = (
        (1, 'Один правильный вариант ответа'),
        (2, 'Два правильных варианта ответа'),
    )
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE, null=False,
                             verbose_name='опрос')
    text = models.CharField(max_length=512, unique=True,
                            verbose_name='текст вопроса')
    right_choices = models.SmallIntegerField(
        null=False, default=1, choices=CHOICES,
        verbose_name='количество верных ответов')

    def __str__(self):
        return f'{self.text}'


class Choice(models.Model):
    """Модель вариантов ответов"""

    class Meta:
        verbose_name_plural = 'ответы'
        verbose_name = 'ответы'

    question = models.ForeignKey(to=Question, on_delete=models.CASCADE,
                                 verbose_name='вопрос')
    text = models.CharField(max_length=128, verbose_name='текст ответа')
    is_correct = models.BooleanField(verbose_name='верный ответ')

    def __str__(self):
        return f'{self.text}'
