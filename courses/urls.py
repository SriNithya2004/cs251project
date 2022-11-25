from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.coursesinfo, name = 'coursehomepage'),
    path('create/',views.create, name = 'CourseCreate'),
    path('join/',views.join,name = 'CourseJoin'),
    path('<int:course_id>/',views.course,name = 'coursepage'),
    path('<int:course_id>/create',views.assign_create,name ='assign_create'),
    path('<int:course_id>/assign/<int:assign_id>',views.assign,name ='assign_page'),
    path('<int:course_id>/assign/<int:assign_id>/submissions',views.submissions,name ='submissions'),
    path('<int:course_id>/assign/<int:assign_id>/feedback/<int:sub_id>',views.feedback,name ='feedback'),
    path('<int:course_id>/participants',views.participants,name ='participants'),
    path('remove/<int:course_id>/<int:user_id>',views.remove,name = 'remove'),
]