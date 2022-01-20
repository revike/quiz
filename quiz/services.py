from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO
from typing import List


class QuizResultService():
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        if self.quiz_dto.uuid == self.answers_dto.quiz_uuid:
            quantity_list = self.quiz_dto.questions
            answers_list = self.answers_dto.answers
            for question in self.quiz_dto.questions:
                ...
        return 0
