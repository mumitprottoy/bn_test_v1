from django.db import models


class Questionnaire(models.Model):
    question = models.TextField()
    description = models.TextField()
    serial = models.IntegerField(default=-1)

    @property
    def details(self) -> dict:
        return dict(
                ques_id=self.id,
                serial=self.serial,
                question=self.question,
                description=self.description
            )

    @classmethod
    def all_questions(cls: 'Questionnaire') -> list[dict]:
        s: list[dict] = [q.details for q in cls.objects.all()]
        for i, q in enumerate(s):
            s[i], s[q['serial']] = s[q['serial']], s[i]
        return s


    def __str__(self) -> str:
        return self.question
    
    def save(self, *args, **kwargs) -> None:
        if self._state.adding and self.serial == -1:
            self.serial = self.__class__.objects.count() + 1
            super().save(*args, **kwargs)
