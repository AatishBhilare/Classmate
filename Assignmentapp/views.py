from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.forms import formset_factory
from django.forms.models import model_to_dict

from django.shortcuts import render, redirect

from Assignmentapp.decorators import adminteacher_authentication, student_authentication
from Assignmentapp.forms import AddTeacherForm, AddStudentForm, EditTeacherForm, EditStudentForm, DeleteTeacherForm, \
    DeleteStudentForm, DeleteSubjectForm, AddEditDepartmentForm, DeleteDepartmentForm, \
    AddEditSemesterForm, DeleteSemesterForm, EditStudentDetailsForm, EditSubjectForm, AddSubjectForm, AddAssignmentForm, \
    EditAssignmentForm, DeleteAssignmentForm, AddTeacherDetailsForm
from Assignmentapp.models import Teacher, Student, Department, User, Subject, Semester, Assignments, Submission


@login_required(login_url='login')
@student_authentication
def index(request):
    teacher_count = Teacher.objects.all().count()
    student_count = Student.objects.all().count()
    dept_count = Department.objects.all().count()
    sub_count = Subject.objects.all().count()
    context = {'teacher_count': teacher_count, 'student_count': student_count, 'dept_count': dept_count,
               'sub_count': sub_count}
    return render(request, 'index.html', context)


def loginuser(request):
    if request.user.is_authenticated:
        if request.user.user_role == '3':
            return redirect('studentindex')
        else:
            return redirect('index')
    else:
        if request.method == 'POST':
            loginusername = request.POST.get('loginUsername')
            loginpassword = request.POST.get('loginPassword')

            user = authenticate(request, username=loginusername, password=loginpassword)

            if user is not None:
                login(request, user)
                if request.user.user_role == '3':
                    return redirect('studentindex')
                else:
                    return redirect('index')
            else:
                messages.info(request, 'username or password is incorrect')

        return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@adminteacher_authentication
def department(request):
    departments = Department.objects.all()
    for dp in departments:
        st_cnt = Student.objects.filter(dept__dept_name=dp.dept_name).count()
        tc_cnt = Teacher.objects.filter(dept__dept_name=dp.dept_name).count()
        dp.student_count = st_cnt
        dp.teacher_count = tc_cnt
    context = {'departments': departments}
    return render(request, 'department/department.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def adddepartment(request):
    form = AddEditDepartmentForm()
    if request.method == 'POST':
        form = AddEditDepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('department')
    context = {'form': form}
    return render(request, 'department/adddepartment.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def editdepartment(request, deptid):
    departmentObj = Department.objects.get(id=deptid)
    form = AddEditDepartmentForm(instance=departmentObj)

    if request.method == 'POST':
        form = AddEditDepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            departmentObj.dept_name = newform.dept_name
            departmentObj.save()
            return redirect('department')

    context = {'form': form}
    return render(request, 'department/editdepartment.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def deletedepartment(request, deptid):
    departmentObj = Department.objects.get(id=deptid)
    form = DeleteDepartmentForm(initial={'dept_name': departmentObj.dept_name})

    if request.method == 'POST':
        form = DeleteDepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            dept_name = form.cleaned_data.get('dept_name')
            if departmentObj.dept_name == dept_name:
                departmentObj.delete()
                return redirect('department')

    context = {'form': form}
    return render(request, 'department/deletedepartment.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def semester(request):
    semesters = Semester.objects.all()
    for sm in semesters:
        sb_cnt = Subject.objects.filter(semref__dept__dept_name=sm.dept.dept_name,
                                        semref__sem_no=sm.sem_no).count()
        sm.sub_count = sb_cnt

    context = {'semesters': semesters}
    return render(request, 'semester/semester.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def addsemester(request):
    form = AddEditSemesterForm()
    if request.method == 'POST':
        form = AddEditSemesterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('semester')
    context = {'form': form}
    return render(request, 'semester/addsemester.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def editsemester(request, semid):
    semObj = Semester.objects.get(id=semid)
    form = AddEditSemesterForm(instance=semObj)

    if request.method == 'POST':
        form = AddEditSemesterForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            semObj.dept = newform.dept
            semObj.sem_no = newform.sem_no
            semObj.save()
            return redirect('semester')

    context = {'form': form}
    return render(request, 'semester/editsemester.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def deletesemester(request, semid):
    semObj = Semester.objects.get(id=semid)
    form = DeleteSemesterForm(initial={'sem_no': semObj.sem_no, 'dept': semObj.dept})

    if request.method == 'POST':
        form = DeleteSemesterForm(request.POST, request.FILES)
        if form.is_valid():
            sem_no = form.cleaned_data.get('sem_no')
            dept = form.cleaned_data.get('dept')
            if semObj.sem_no == sem_no and semObj.dept.dept_name == dept:
                semObj.delete()
                return redirect('semester')

    context = {'form': form}
    return render(request, 'semester/deletesemester.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def teacher(request):
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teacher/teacher.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def addteacher(request):
    form2 = AddTeacherForm()
    AddTeacherFormSet = formset_factory(AddTeacherDetailsForm)
    formset = AddTeacherFormSet()
    if request.method == 'POST':
        formset = AddTeacherFormSet(request.POST)
        form2 = AddTeacherForm(request.POST, request.FILES)
        if form2.is_valid() and formset.is_valid():
            form2.instance.user_role = '2'
            newform = form2.save()

            teacherObj = Teacher.objects.create(user_ref=newform)

            for i in range(0, formset.total_form_count()):
                tform = formset.forms[i]
                try:
                    dept = tform.cleaned_data['dept']
                except:
                    dept = None
                try:
                    semref = tform.cleaned_data['semref']
                except:
                    semref = None
                try:
                    subref = tform.cleaned_data['subref']
                except:
                    subref = None

                if dept and semref and subref:
                    if dept not in teacherObj.dept.all():
                        teacherObj.dept.add(dept)
                    if semref not in teacherObj.semref.all():
                        teacherObj.semref.add(semref)
                    if subref not in teacherObj.subref.all():
                        teacherObj.subref.add(subref)
            teacherObj.save()
            '''deptv = form2.cleaned_data.get('dept')
            teacherObj = Teacher.objects.create(user_ref=newform)
            for x in deptv:
                teacherObj.dept.add(x)
            teacherObj.save()'''

            return redirect('teacher')
    context = {'form2': form2, 'formset': formset}
    return render(request, 'teacher/addteacher.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def editteacher(request, tid):
    teacherObj = Teacher.objects.get(id=tid)
    tobject = teacherObj.user_ref
    tobject = model_to_dict(tobject)
    # tobject.update(tobject.dept)

    teachDeptList = []
    for d in teacherObj.dept.all():
        teachDeptList.append(d.id)
    tobject['dept'] = teachDeptList

    form = EditTeacherForm(initial=tobject)
    user_teacherObj = User.objects.get(id=teacherObj.user_ref.id)

    if request.method == 'POST':
        form = EditTeacherForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            user_teacherObj.user_full_name = newform.user_full_name
            user_teacherObj.email = newform.email
            user_teacherObj.user_mobile = newform.user_mobile
            user_teacherObj.user_address = newform.user_address
            user_teacherObj.user_gender = newform.user_gender
            user_teacherObj.user_dob = newform.user_dob
            if not newform.user_image == 'emptyimage':
                user_teacherObj.user_image = newform.user_image

            user_teacherObj.save()

            deptv = form.cleaned_data.get('dept')
            teacherObj.dept.clear()
            for d in deptv:
                teacherObj.dept.add(d)

            teacherObj.save()
            return redirect('teacher')

    context = {'form': form}
    return render(request, 'teacher/editteacher.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def deleteteacher(request, tid):
    teacherObj = Teacher.objects.get(id=tid)
    form = DeleteTeacherForm(initial={'username': teacherObj.user_ref.username})

    if request.method == 'POST':
        form = DeleteTeacherForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if teacherObj.user_ref.username == username:
                user_teacherObj = User.objects.get(id=teacherObj.user_ref.id)
                teacherObj.delete()
                user_teacherObj.delete()
                return redirect('teacher')

    context = {'form': form}
    return render(request, 'teacher/deleteteacher.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def student(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'student/student.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def load_sem(request):
    dept_id = request.GET.get('dept')
    sem = Semester.objects.filter(dept__id=dept_id)
    return render(request, 'student/sem_options.html', {'semesters': sem})


@login_required(login_url='login')
@adminteacher_authentication
def load_sub(request):
    semref_id = request.GET.get('semref')
    sub = Subject.objects.filter(semref__id=semref_id)
    return render(request, 'assignment/sub_options.html', {'subjects': sub})


@login_required(login_url='login')
@adminteacher_authentication
def addstudent(request):
    form = AddStudentForm()
    if request.method == 'POST':
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user_role = '3'
            newform = form.save()
            deptv = form.cleaned_data.get('dept')
            sem = form.cleaned_data.get('semref')
            roll = form.cleaned_data.get('stud_roll')
            studentObj = Student.objects.create(user_ref=newform, dept=deptv, semref=sem, stud_roll=roll)
            studentObj.save()
            return redirect('student')
    context = {'form': form}
    return render(request, 'student/addstudent.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def editstudent(request, stid):
    studentObj = Student.objects.get(id=stid)
    stobject = studentObj.user_ref
    user_studentObj = User.objects.get(id=studentObj.user_ref.id)

    form = EditStudentForm(instance=stobject)
    form2 = EditStudentDetailsForm(instance=studentObj)

    if request.method == 'POST':
        form = EditStudentForm(request.POST, request.FILES)
        form2 = EditStudentDetailsForm(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
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

            newform2 = form2.save(commit=False)

            studentObj.dept = newform2.dept
            studentObj.semref = newform2.semref
            studentObj.stud_roll = newform2.stud_roll
            studentObj.save()

            return redirect('student')
    context = {'form': form, 'form2': form2}
    return render(request, 'student/editstudent.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def deletestudent(request, stid):
    studentObj = Student.objects.get(id=stid)
    form = DeleteStudentForm(initial={'username': studentObj.user_ref.username})

    if request.method == 'POST':
        form = DeleteStudentForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if studentObj.user_ref.username == username:
                user_studentObj = User.objects.get(id=studentObj.user_ref.id)
                studentObj.delete()
                user_studentObj.delete()
                return redirect('student')

    context = {'form': form}
    return render(request, 'student/deletestudent.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def subject(request):
    subjectObj = Subject.objects.all()
    context = {'subjectObj': subjectObj}
    return render(request, 'subjects/subject.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def addsubject(request):
    form = AddSubjectForm()
    if request.method == 'POST':
        form = AddSubjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subject')
    context = {'form': form}
    return render(request, 'subjects/addsubject.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def editsubject(request, subid):
    subjectObj = Subject.objects.get(id=subid)
    form = EditSubjectForm(instance=subjectObj)

    if request.method == 'POST':
        form = EditSubjectForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            subjectObj.sub_name = newform.sub_name
            subjectObj.semref = newform.semref
            subjectObj.dept = newform.dept
            subjectObj.save()
            return redirect('subject')

    context = {'form': form}

    return render(request, 'subjects/editsubject.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def deletesubject(request, subid):
    subjectObj = Subject.objects.get(id=subid)
    form = DeleteSubjectForm(initial={'semref': subjectObj.semref.sem_no, 'sub_name': subjectObj.sub_name})

    if request.method == 'POST':
        form = DeleteSubjectForm(request.POST, request.FILES)
        if form.is_valid():
            sub_name = form.cleaned_data.get('sub_name')
            if subjectObj.sub_name == sub_name:
                subjectObj.delete()
                return redirect('subject')

    context = {'form': form}
    return render(request, 'subjects/deletesubject.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def assignment(request):
    if request.user.user_role == '2':
        teacherObj = Teacher.objects.get(user_ref__id=request.user.id)
        assignment = Assignments.objects.filter(dept__id__in=teacherObj.dept.all())
    else:
        assignment = Assignments.objects.all()
    context = {'assignments': assignment}
    return render(request, 'assignment/assignment.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def addassignment(request):
    form = AddAssignmentForm(user=request.user)

    if request.method == 'POST':
        form = AddAssignmentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            teacher = Teacher.objects.get(user_ref=request.user)
            form.instance.teacher = teacher
            newform = form.save()

            studentObj = Student.objects.filter(dept=newform.dept, semref=newform.semref)
            for student in studentObj:
                submissionObj = Submission.objects.create(studref=student, asgref=newform)
                submissionObj.save()
            return redirect('assignment')

    context = {'form': form}
    return render(request, 'assignment/addassignment.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def editassignment(request, asgid):
    assignmentObj = Assignments.objects.get(id=asgid)
    form = EditAssignmentForm(instance=assignmentObj, user=request.user)

    if request.method == 'POST':
        form = EditAssignmentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            newform = form.save(commit=False)
            assignmentObj.dept = newform.dept
            assignmentObj.semref = newform.semref
            assignmentObj.subref = newform.subref
            assignmentObj.asg_no = newform.asg_no
            assignmentObj.asg_title = newform.asg_title
            assignmentObj.asg_deadline = newform.asg_deadline
            assignmentObj.asg_marks = newform.asg_marks

            if not newform.asg_file == 'emptyfile':
                assignmentObj.asg_file = newform.asg_file

            assignmentObj.save()

            return redirect('assignment')

    context = {'form': form}
    return render(request, 'assignment/editassignment.html', context)


@login_required(login_url='login')
@adminteacher_authentication
def deleteassignment(request, asgid):
    assignmentObj = Assignments.objects.get(id=asgid)
    form = DeleteAssignmentForm(initial={'asg_no': assignmentObj.asg_no, 'asg_title': assignmentObj.asg_title})

    if request.method == 'POST':
        form = DeleteAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            asg_no = form.cleaned_data.get('asg_no')
            asg_title = form.cleaned_data.get('asg_title')
            if assignmentObj.asg_no == asg_no and assignmentObj.asg_title == asg_title:
                assignmentObj.delete()
                return redirect('assignment')

    context = {'form': form}
    return render(request, 'assignment/deleteassignment.html', context)
