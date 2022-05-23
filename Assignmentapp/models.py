from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    gender = (
        ('1', 'Female'),
        ('2', 'Male'),
    )
    userrole = (
        ('1', 'Admin'),
        ('2', 'Teacher'),
        ('3', 'Student'),
    )
    first_name = None
    last_name = None
    user_full_name = models.CharField(max_length=100, null=True)
    user_mobile = models.IntegerField(null=True)
    user_address = models.TextField(verbose_name='Address', blank=True, null=True)
    user_image = models.ImageField(blank=True, null=True, upload_to='profileimages/', )
    user_gender = models.CharField(verbose_name='Gender', max_length=20, choices=gender, default='1',
                                   blank=True, null=True)
    user_role = models.CharField(verbose_name='User Role', max_length=20, choices=userrole, default='1',
                                 blank=True, null=True)
    user_dob = models.DateField(verbose_name='Date of Birth', blank=True, null=True)
    objects = UserManager()

    class Meta:
        verbose_name_plural = 'Users'

    def _str_(self):
        return self.username


class Department(models.Model):
    dept_name = models.CharField(verbose_name='Department Name', max_length=40)
    teacher_count = models.IntegerField(blank=True, null=True)
    student_count = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.dept_name


class Semester(models.Model):
    dept = models.ForeignKey(Department, models.SET_NULL, verbose_name='Department Name',
                             blank=True, null=True)
    sem_no = models.IntegerField()
    sub_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        dep = str(self.sem_no)
        return dep


class Subject(models.Model):
    dept = models.ForeignKey(Department, models.SET_NULL, verbose_name='Department Name',
                             blank=True, null=True)
    semref = models.ForeignKey(Semester, models.SET_NULL, verbose_name='Semester No',
                               blank=True, null=True)
    sub_name = models.CharField(verbose_name='Subject Name', max_length=40)

    def __str__(self):
        return self.sub_name


class Teacher(models.Model):
    user_ref = models.ForeignKey(User, models.SET_NULL, verbose_name='User Details', related_name='user_reference',
                                 blank=True, null=True)
    dept = models.ManyToManyField(Department, related_name='teacher_dept')
    semref = models.ManyToManyField(Semester, verbose_name='Semester No')
    subref = models.ManyToManyField(Subject, verbose_name='Subject Details')

    def __str__(self):
        return self.user_ref.username


class Student(models.Model):
    user_ref = models.ForeignKey(User, models.SET_NULL, verbose_name='User Details', related_name='user_reference2',
                                 blank=True, null=True)
    stud_roll = models.IntegerField(verbose_name='Student Roll No')
    dept = models.ForeignKey(Department, models.SET_NULL, verbose_name='Student Department',
                             blank=True, null=True)
    semref = models.ForeignKey(Semester, models.SET_NULL, verbose_name='Semester No',
                               blank=True, null=True)


class Assignments(models.Model):
    dept = models.ForeignKey(Department, models.SET_NULL, verbose_name='Department Name',
                             blank=True, null=True)
    semref = models.ForeignKey(Semester, models.SET_NULL, verbose_name='Semester No',
                               blank=True, null=True)
    subref = models.ForeignKey(Subject, models.SET_NULL, verbose_name='Subject Details', blank=True, null=True)
    teacher = models.ForeignKey(Teacher, models.SET_NULL, verbose_name='Teacher Details', blank=True, null=True)
    asg_no = models.IntegerField(verbose_name='Assignment No', blank=True, null=True)
    asg_title = models.CharField(verbose_name='Assignment Title', max_length=255)
    asg_file = models.FileField(upload_to='AssignmentFiles', blank=True, null=True)
    asg_createdtime = models.DateTimeField(auto_now_add=True)
    asg_deadline = models.DateTimeField()
    asg_marks = models.IntegerField(verbose_name='Marks', blank=True, null=True)


class Submission(models.Model):
    asgref = models.ForeignKey(Assignments, models.SET_NULL, verbose_name='Assignment Details',
                               related_name='assignment_ref', blank=True, null=True)
    studref = models.ForeignKey(Student, models.SET_NULL, verbose_name='Student Details', related_name='student_ref',
                                blank=True, null=True)
    submittime = models.DateTimeField(blank=True, null=True)
    submission_file = models.FileField(upload_to='SubmittedFiles', blank=True, null=True)
    submissionstatus = models.BooleanField(default=False)
