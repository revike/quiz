QuizDTO(
    uuid=1,
    title='Опрос 1',
    questions=[
        QuestionDTO(
            uuid=2,
            text='Вопрос 2 * 1',
            choices=[
                ChoiceDTO(
                    uuid=6,
                    text='Ответ 2 * 2',
                    is_correct=False),
                ChoiceDTO(
                    uuid=5,
                    text='Ответ 1 * 2',
                    is_correct=True),
                ChoiceDTO(
                    uuid=7,
                    text='Ответ 3 * 2',
                    is_correct=False),
                ChoiceDTO(
                    uuid=8,
                    text='Ответ 4 * 2',
                    is_correct=False)]),
        QuestionDTO(
            uuid=1,
            text='Вопрос 1 * 1',
            choices=[
                ChoiceDTO(
                    uuid=1,
                    text='Ответ 1 * 1',
                    is_correct=True),
                ChoiceDTO(
                    uuid=2,
                    text='Ответ 2 * 1',
                    is_correct=False),
                ChoiceDTO(
                    uuid=3,
                    text='Ответ 3 * 1',
                    is_correct=False),
                ChoiceDTO(uuid=4,
                          text='Ответ 4 * 1',
                          is_correct=False)]),
        QuestionDTO(
            uuid=3,
            text='Вопрос 3 * 1',
            choices=[
                ChoiceDTO(
                    uuid=9,
                    text='Ответ 1 * 3',
                    is_correct=True),
                ChoiceDTO(
                    uuid=10,
                    text='Ответ 2 * 3',
                    is_correct=False),
                ChoiceDTO(
                    uuid=11,
                    text='Ответ 3 * 3',
                    is_correct=False),
                ChoiceDTO(
                    uuid=12,
                    text='Ответ 4 * 3',
                    is_correct=False)]),
        QuestionDTO(
            uuid=4,
            text='Вопрос 4 * 1',
            choices=[
                ChoiceDTO(
                    uuid=15,
                    text='Ответ 3 * 4',
                    is_correct=False),
                ChoiceDTO(
                    uuid=16,
                    text='Ответ 4 * 4',
                    is_correct=False),
                ChoiceDTO(
                    uuid=13,
                    text='Ответ 1 * 4',
                    is_correct=True),
                ChoiceDTO(
                    uuid=14,
                    text='Ответ 2 * 4',
                    is_correct=True)]),
        QuestionDTO(
            uuid=5,
            text='Вопрос 5 * 1',
            choices=[
                ChoiceDTO(
                    uuid=17,
                    text='Ответ 1 * 5',
                    is_correct=True),
                ChoiceDTO(
                    uuid=19,
                    text='Ответ 3 * 5',
                    is_correct=False),
                ChoiceDTO(
                    uuid=18,
                    text='Ответ 2 * 5',
                    is_correct=True),
                ChoiceDTO(
                    uuid=20,
                    text='Ответ 4 * 5',
                    is_correct=False)])])

AnswersDTO(
    quiz_uuid=1,
    answers=[
        AnswerDTO(
            question_uuid=2,
            choices=['Ответ 2 * 2', None, None, None]),
        AnswerDTO(
            question_uuid=1,
            choices=[None, 'Ответ 2 * 1', None, None]),
        AnswerDTO(
            question_uuid=3,
            choices=[None, 'Ответ 2 * 3', None, None]),
        AnswerDTO(
            question_uuid=4,
            choices=[None, 'Ответ 4 * 4', None, None]),
        AnswerDTO(
            question_uuid=5,
            choices=[None, None, 'Ответ 2 * 5', None])])
