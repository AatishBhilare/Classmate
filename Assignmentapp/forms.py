from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput, EmailInput, FileInput, PasswordInput

from Assignmentapp.models import User, Department, Student, Subject, Semester, Assignments, Teacher


class AddEditDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name']


class DeleteDepartmentForm(forms.Form):
    dept_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'readonly': True}))


class AddEditSemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['dept', 'sem_no']


class DeleteSemesterForm(forms.Form):
    dept = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'readonly': True}))
    sem_no = forms.IntegerField(widget=TextInput(attrs={'class': 'form-control', 'readonly': True}))


class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['dept', 'semref', 'sub_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'semref' in self.data:
            self.fields['semref'].queryset = Semester.objects.all()


class EditSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['dept', 'semref', 'sub_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semref'].queryset = Semester.objects.none()

        if 'dept' in self.data:
            try:
                dept_id = int(self.data.get('dept'))
                self.fields['semref'].queryset = Semester.objects.filter(dept__id=dept_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            dept_id = self.instance.dept.id
            self.fields['semref'].queryset = Semester.objects.filter(dept__id=dept_id)


class DeleteSubjectForm(forms.Form):
    sub_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'readonly': True}))


class AddTeacherForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField()
    user_image = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'form-control-file'}))
    user_role = forms.ChoiceField(required=False)

    def clean_username(self):
        vusername = self.cleaned_data['username']
        if ' ' in vusername:
            raise forms.ValidationError('Username should not contain any space')
        return vusername

    class Meta:
        model = User
        fields = ['username', 'user_full_name', 'email', 'user_mobile', 'user_image', 'password1',
                  'password2', 'user_address', 'user_gender', 'user_role', 'user_dob']
        widgets = {
            "username": TextInput(
                attrs={
                    "class": "form-control"
                }),

            "user_full_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "type": "email"
                }),
            "user_mobile": TextInput(
                attrs={
                    "class": "form-control"
                }),

        }

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = 'profileimages/user.png'
            return user_image


class AddTeacherDetailsForm(forms.Form):
    dept = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'deptclass'}))
    semref = forms.ModelChoiceField(queryset=Semester.objects.all(), widget=forms.Select(attrs={'class': 'semclass'}))
    subref = forms.ModelChoiceField(queryset=Subject.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'dept' in self.data:
            try:
                dept_id = int(self.data.get('dept'))
                self.fields['semref'].queryset = Semester.objects.filter(dept__id=dept_id)
            except (ValueError, TypeError):
                pass

        if 'semref' in self.data:
            try:
                semref_id = int(self.data.get('semref'))
                self.fields['subref'].queryset = Subject.objects.filter(semref__id=semref_id)
            except (ValueError, TypeError):
                pass


class EditTeacherForm(UserChangeForm):
    password = None
    dept = forms.ModelMultipleChoiceField(label='Departments',
                                          queryset=Department.objects.all(),
                                          widget=forms.CheckboxSelectMultiple
                                          )

    class Meta:
        model = User
        fields = ['user_full_name', 'email', 'user_mobile', 'user_image', 'user_address', 'user_gender', 'user_dob']

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = 'emptyimage'
            return user_image


class DeleteTeacherForm(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'readonly': True}))


class AddStudentForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField()
    user_image = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'form-control-file'}))
    dept = forms.ModelChoiceField(label='Departments',
                                  queryset=Department.objects.all(),
                                  widget=forms.Select()
                                  )
    semref = forms.ModelChoiceField(label='Semester',
                                    queryset=Semester.objects.none(),
                                    widget=forms.Select()
                                    )
    user_role = forms.ChoiceField(required=False)
    stud_roll = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'semref' in self.data:
            self.fields['semref'].queryset = Semester.objects.all()

    def clean_username(self):
        vusername = self.cleaned_data['username']
        if ' ' in vusername:
            raise forms.ValidationError('Username should not contain any space')
        return vusername

    def clean_stud_roll(self):
        vstudroll = self.cleaned_data['stud_roll']
        vstuddept = self.cleaned_data['dept']
        studentObj = Student.objects.filter(stud_roll=vstudroll, dept=vstuddept)
        if studentObj:
            raise forms.ValidationError('Roll No already Exists')
        else:
            return vstudroll

    class Meta:
        model = User
        fields = ['username', 'user_full_name', 'email', 'user_mobile', 'user_image', 'password1',
                  'password2', 'user_address', 'user_gender', 'user_role', 'user_dob']
        widgets = {
            "username": TextInput(
                attrs={
                    "class": "form-control"
                }),

            "user_full_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "type": "email"
                }),
            "user_mobile": TextInput(
                attrs={
                    "class": "form-control"
                }),

        }

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = 'profileimages/user.png'
            return user_image


class EditStudentForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['user_full_name', 'email', 'user_mobile', 'user_image', 'user_address', 'user_gender', 'user_dob']

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = 'emptyimage'
            return user_image


class EditStudentDetailsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('stud_roll', 'dept', 'semref')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semref'].queryset = Semester.objects.none()

        if 'dept' in self.data:
            try:
                dept_id = int(self.data.get('dept'))
                self.fields['semref'].queryset = Semester.objects.filter(dept__id=dept_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            dept_id = self.instance.dept.id
            self.fields['semref'].queryset = Semester.objects.filter(dept__id=dept_id)


class DeleteStudentForm(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'readonly': True}))


class AddAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignments
        fields = ('dept', 'semref', 'subref', 'teacher', 'asg_no', 'asg_title', 'asg_file', 'asg_deadline', 'asg_marks')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user.user_role == '2':
            teacherObj = Teacher.objects.get(user_ref__id=self.user.id)
            self.fields['dept'].queryset = Department.objects.filter(id__in=teacherObj.dept.all())
        self.fields['semref'].queryset = Semester.objects.none()
        self.fields['subref'].queryset = Subject.objects.none()

        if 'dept' in self.data:
            try:
                dept_id = int(self.data.get('dept'))
                self.fields['semref'].queryset = Semester.objects.filter(dept__id=dept_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            dept_id = self.instance.dept.id
            self.fields['semref'].queryset = Semester.objects.filter(dept__id=dept_id)

        if 'semref' in self.data:
            try:
                semref_id = int(self.data.get('semref'))
                self.fields['subref'].queryset = Subject.objects.filter(semref__id=semref_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            semref_id = self.instance.semref.id
            self.fields['subref'].queryset = Subject.objects.filter(semref__id=semref_id)


class EditAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignments
        fields = ('dept', 'semref', 'subref', 'asg_no', 'asg_title', 'asg_file', 'asg_deadline', 'asg_marks')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user.user_role == '2':
            teacherObj = Teacher.objects.get(user_ref__id=self.user.id)
            self.fields['dept'].queryset = Department.objects.filter(id__in=teacherObj.dept.all())
        self.fields['semref'].queryset = Semester.objects.none()
        self.fields['subref'].queryset = Subject.objects.none()

        if 'dept' in self.data:
            try:
                dept_id = int(self.data.get('dept'))
                self.fields['semref'].queryset = Semester.objects.filter(dept__id=dept_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            dept_id = self.instance.dept.id
            self.fields['semref'].queryset = Semester.objects.filter(dept__id=dept_id)

        if 'semref' in self.data:
            try:
                semref_id = int(self.data.get('semref'))
                self.fields['subref'].queryset = Subject.objects.filter(semref__id=semref_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            semref_id = self.instance.semref.id
            self.fields['subref'].queryset = Subject.objects.filter(semref__id=semref_id)

    def clean_asg_file(self):
        asg_file = self.cleaned_data['asg_file']
        if asg_file:
            return asg_file
        else:
            asg_file = 'emptyfile'
            return asg_file


class DeleteAssignmentForm(forms.Form):
    asg_no = forms.IntegerField(widget=TextInput(attrs={'class': 'form-control', 'readonly': True}))
    asg_title = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'readonly': True}))
