# Generated by Django 3.2.5 on 2021-07-29 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Assignmentapp', '0002_auto_20210729_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='dept',
            field=models.ManyToManyField(related_name='teacher_dept', to='Assignmentapp.Department'),
        ),
    ]
