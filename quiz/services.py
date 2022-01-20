from .dto import QuizDTO, AnswersDTO


class QuizResultService:
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        if self.quiz_dto.uuid == self.answers_dto.quiz_uuid:
            quantity_quest = len(self.quiz_dto.questions)
            point = len(self.answers_dto.answers)
            for answer in self.answers_dto[1]:
                i = 0
                while answer.question_uuid != self.quiz_dto[2][i].uuid:
                    i += 1
                if answer.question_uuid == self.quiz_dto[2][i].uuid:
                    quiz_choices = self.quiz_dto[2][i].choices
                    answer_choices = answer.choices
                    for i in range(len(answer_choices)):
                        if (quiz_choices[i].is_correct and answer_choices[i]
                            is None) or (not quiz_choices[i].is_correct and
                                         answer_choices[i] is not None):
                            point -= 1
                            break
            result = point / quantity_quest
            return result
