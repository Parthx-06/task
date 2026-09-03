from django.db import models
from django.utils.timezone import now
from django.conf import settings


class Instructor(models.Model):
    """
    Model representing an instructor in the online course platform.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200, default="")
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name or f"Instructor {self.id}"


class Learner(models.Model):
    """
    Model representing a learner/student in the online course platform.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    occupation = models.CharField(max_length=100, default="Student")
    social_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"Learner {self.id}"


class Course(models.Model):
    """
    Model representing an online course.
    """
    name = models.CharField(max_length=200, default="")
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    description = models.TextField(blank=True)
    pub_date = models.DateField(null=True, blank=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Model representing a lesson within a course.
    """
    title = models.CharField(max_length=200, default="Sample Lesson")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    """
    Model representing course enrollment for a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, default='audit')
    rating = models.FloatField(default=5.0)


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
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True)
    choices = models.ManyToManyField(Choice)
    submitted_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Submission {self.id} submitted at {self.submitted_at}"
