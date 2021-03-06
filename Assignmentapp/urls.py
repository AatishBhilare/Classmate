from django.urls import path

from Assignmentapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('department', views.department, name='department'),
    path('department/add', views.adddepartment, name='adddepartment'),
    path('department/<int:deptid>/edit', views.editdepartment, name='editdepartment'),
    path('department/<int:deptid>/delete', views.deletedepartment, name='deletedepartment'),
    path('semester', views.semester, name='semester'),
    path('semester/add', views.addsemester, name='addsemester'),
    path('semester/<int:semid>/edit', views.editsemester, name='editsemester'),
    path('semester/<int:semid>/delete', views.deletesemester, name='deletesemester'),
    path('ajax/load-sem/', views.load_sem, name='ajax_load_sem'),
    path('ajax/load-sub/', views.load_sub, name='ajax_load_sub'),
    path('teacher', views.teacher, name='teacher'),
    path('teacher/add', views.addteacher, name='addteacher'),
    path('teacher/<int:tid>/edit', views.editteacher, name='editteacher'),
    path('teacher/<int:tid>/delete', views.deleteteacher, name='deleteteacher'),
    path('student', views.student, name='student'),
    path('student/add', views.addstudent, name='addstudent'),
    path('student/<int:stid>edit', views.editstudent, name='editstudent'),
    path('student/<int:stid>/delete', views.deletestudent, name='deletestudent'),
    path('subject', views.subject, name='subject'),
    path('subject/add', views.addsubject, name='addsubject'),
    path('subject/<int:subid>/edit', views.editsubject, name='editsubject'),
    path('subject/<int:subid>/delete', views.deletesubject, name='deletesubject'),
    path('assignment', views.assignment, name='assignment'),
    path('assignment/add', views.addassignment, name='addassignment'),
    path('assignment/<int:asgid>/edit', views.editassignment, name='editassignment'),
    path('assignment/<int:asgid>/delete', views.deleteassignment, name='deleteassignment'),
]
