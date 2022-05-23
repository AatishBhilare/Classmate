from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import TextInput, EmailInput, FileInput, PasswordInput

from Assignmentapp.models import User, Submission


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


class SubmitAssignmentForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_file']

    def clean_submission_file(self):
        submission_file = self.cleaned_data['submission_file']
        if submission_file:
            return submission_file
        else:
            submission_file = 'EmptyFile'
            return submission_file
