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
    def sync_serial(cls: 'Questionnaire', serial: int) -> None:
        ques_id_list = list()
        q = cls.objects.filter(serial=serial + 1).first()
        while q is not None:
            ques_id_list.append(q.id)
            serial += 1
            q = cls.objects.filter(serial=serial + 1).first()
        for ques_id in ques_id_list:
            q = Questionnaire.objects.get(id=ques_id)
            q.serial = q.serial - 1
            q.save()


    @classmethod
    def all_questions(cls: 'Questionnaire') -> list[dict]:
        id_serial_map = {q.serial: q.id for q in cls.objects.all()}
        return [cls.objects.get(
            id=id_serial_map[i]).details for i in sorted(id_serial_map)]

    def __str__(self) -> str:
        return self.question
    
    def save(self, *args, **kwargs) -> None:
        if self._state.adding and self.serial == -1:
            self.serial = self.__class__.objects.count() + 1
            super().save(*args, **kwargs)
