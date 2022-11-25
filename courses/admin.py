from django.contrib import admin
from courses.models import Course, Assignment, FileSubmission

# Register your models here.

admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(FileSubmission)