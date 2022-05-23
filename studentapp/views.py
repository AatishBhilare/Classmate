from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Assignmentapp.decorators import student_profile_authentication, student_editprofile_authentication
from Assignmentapp.models import Student, User, Assignments, Submission
from studentapp.forns import EditStudentForm, SubmitAssignmentForm


@login_required(login_url='login')
def studentindex(request):
    return render(request, 'studentpanel/studentindex.html')


@login_required(login_url='login')
@student_profile_authentication
def studentprofile(request, stid):
    studentObj = Student.objects.get(user_ref__id=stid)
    context = {'studentObj': studentObj}
    return render(request, 'studentpanel/profile/studentprofile.html', context)


@login_required(login_url='login')
@student_editprofile_authentication
def editstudentprofile(request, estid):
    studentObj = Student.objects.get(user_ref__id=estid)
    stobject = studentObj.user_ref
    user_studentObj = User.objects.get(id=studentObj.user_ref.id)

    form = EditStudentForm(instance=stobject)

    if request.method == 'POST':
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            user_studentObj.user_full_name = newform.user_full_name
            user_studentObj.email = newform.email
            user_studentObj.user_mobile = newform.user_mobile
            user_studentObj.user_address = newform.user_address
            user_studentObj.user_gender = newform.user_gender
            user_studentObj.user_dob = newform.user_dob

            if not newform.user_image == 'emptyimage':
                user_studentObj.user_image = newform.user_image

            user_studentObj.save()

            return redirect('studentprofile', estid)
    context = {'form': form}
    return render(request, 'studentpanel/profile/editstudentprofile.html', context)


def assignment(request):
    studentObj = Student.objects.get(user_ref__id=request.user.id)
    submissionObj = Submission.objects.filter(studref=studentObj)
    context = {'submissionObj': submissionObj}
    return render(request, 'studentpanel/assignment/assignment.html', context)


def submitassignment(request, submid):
    submissionObj = Submission.objects.get(id=submid)
    form = SubmitAssignmentForm(instance=submissionObj)

    if request.method == 'POST':
        form = SubmitAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            clearBtn = request.POST.get('submission_file-clear')
            newform = form.save(commit=False)
            submissionObj.submittime = datetime.now()

            if clearBtn:
                submissionObj.submission_file = None
                submissionObj.submissionstatus = False
            else:
                if not newform.submission_file == 'EmptyFile':
                    submissionObj.submission_file = newform.submission_file
                    submissionObj.submissionstatus = True

            submissionObj.save()
            return redirect('studentassignment')

    context = {'form': form, 'submissionObj': submissionObj}
    return render(request, 'studentpanel/assignment/submitassignment.html', context)
