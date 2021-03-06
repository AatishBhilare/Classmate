# Generated by Django 3.2.5 on 2021-07-29 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Assignmentapp', '0006_alter_department_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name_plural': 'Departments'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='user',
            name='user_dob',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Birth'),
        ),
    ]
