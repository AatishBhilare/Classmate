# Generated by Django 3.2.5 on 2021-07-31 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Assignmentapp', '0010_alter_student_stud_roll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='dept_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_ref3', to='Assignmentapp.department', verbose_name='Department Name'),
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem_no', models.IntegerField()),
                ('dept_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_ref', to='Assignmentapp.department', verbose_name='Department Name')),
            ],
        ),
    ]