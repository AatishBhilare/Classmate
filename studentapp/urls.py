from django.urls import path

from studentapp import views

urlpatterns = [
    path('', views.studentindex, name='studentindex'),
    path('profile/<int:stid>', views.studentprofile, name='studentprofile'),
    path('profile/edit/<int:estid>', views.editstudentprofile, name='editstudentprofile'),
    path('assignment', views.assignment, name='studentassignment'),
    path('assignment/<int:submid>/submit', views.submitassignment, name='submitassignment'),

]
