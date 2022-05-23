from django.contrib import admin

# Register your models here.
from Assignmentapp.models import Submission, Assignments, Student, Teacher, Subject, Department, User, Semester

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Assignments)
admin.site.register(Submission)
