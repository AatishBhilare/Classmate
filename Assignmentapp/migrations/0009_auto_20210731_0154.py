# Generated by Django 3.2.5 on 2021-07-30 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Assignmentapp', '0008_auto_20210731_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dept_reference', to='Assignmentapp.department', verbose_name='Student Department'),
        ),
        migrations.AlterField(
            model_name='student',
            name='user_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_reference2', to=settings.AUTH_USER_MODEL, verbose_name='User Details'),
        ),
    ]