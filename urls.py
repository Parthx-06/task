from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Course details page
    path('<int:course_id>/', views.course_details, name='course_details'),
    
    # Path for submitting exam/quiz choices
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Path for displaying exam results
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
    path('course/<int:course_id>/submission/<int:submission_id>/show_exam_result/', views.show_exam_result, name='show_exam_result'),
]
