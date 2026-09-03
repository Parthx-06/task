from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment


def course_details(request, course_id):
    """
    View function to display course details and its lessons.
    """
    course = get_object_or_404(Course, pk=course_id)
    context = {'course': course}
    return render(request, 'course_details_bootstrap.html', context)


def submit(request, course_id):
    """
    View function to handle exam form submissions for a course.
    Extracts selected choice IDs, creates a Submission object, and redirects to show_exam_result.
    """
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        # Retrieve all selected choice IDs from POST request
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                try:
                    selected_choice_ids.append(int(value))
                except ValueError:
                    pass
            elif key == 'choice':
                for val in request.POST.getlist('choice'):
                    try:
                        selected_choice_ids.append(int(val))
                    except ValueError:
                        pass
        
        # Create submission instance
        submission = Submission.objects.create()
        
        # Associate selected choices
        if selected_choice_ids:
            choices = Choice.objects.filter(id__in=selected_choice_ids)
            submission.choices.set(choices)
            submission.save()
            
        return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)
    
    return redirect('course_details', course_id=course.id)


def show_exam_result(request, course_id, submission_id=None):
    """
    View function to display score and detailed results of an exam submission.
    """
    course = get_object_or_404(Course, pk=course_id)
    
    if submission_id:
        submission = get_object_or_404(Submission, pk=submission_id)
    else:
        submission = Submission.objects.filter().last()
        if not submission:
            raise Http404("No submission found.")
            
    selected_choice_ids = list(submission.choices.values_list('id', flat=True))
    total_score = 0
    total_possible = 0
    
    # Calculate score based on correct questions
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_possible += question.grade
            if question.is_get_score(selected_choice_ids):
                total_score += question.grade

    percentage = (total_score / total_possible * 100) if total_possible > 0 else 0

    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'total_possible': total_possible,
        'percentage': round(percentage, 2),
        'selected_choice_ids': selected_choice_ids,
    }
    return render(request, 'exam_result.html', context)
