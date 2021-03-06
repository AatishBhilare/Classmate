# Generated by Django 3.2.5 on 2021-08-11 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Assignmentapp', '0023_submission_submissionstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='semref',
            field=models.ManyToManyField(to='Assignmentapp.Semester', verbose_name='Semester No'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='subref',
            field=models.ManyToManyField(to='Assignmentapp.Subject', verbose_name='Subject Details'),
        ),
    ]
