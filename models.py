from django.db import models
from django.utils.timezone import now


class Lesson(models.Model):
    """
    Model representing a lesson in an online course.
    """
    title = models.CharField(max_length=200, default="Sample Lesson")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Model representing a quiz question.
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=1)

    def is_get_score(self, selected_ids):
        """
        Calculates if the user's selected choices match all correct choices.
        """
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        return all_answers == selected_correct if all_answers > 0 else False

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """
    Model representing an answer choice for a question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    """
    Model representing a student's submission containing chosen choices.
    """
    choices = models.ManyToManyField(Choice)
    submitted_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Submission {self.id} submitted at {self.submitted_at}"
