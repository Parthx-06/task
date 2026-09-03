from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Course details route
    path('<int:course_id>/', views.course_details, name='course_details'),
    
    # Required submit view route: <int:course_id>/submit/
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Required show_exam_result view route: course/<int:course_id>/submission/<int:submission_id>/result/
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
    path('course/<int:course_id>/submission/<int:submission_id>/show_exam_result/', views.show_exam_result, name='show_exam_result'),
]
