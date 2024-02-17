# Generated by Django 4.0.6 on 2024-01-30 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('status', models.CharField(choices=[('done', 'Done'), ('postponed', 'Postponed'), ('progess', 'In progess'), ('canceled', 'Canceled')], max_length=15, verbose_name='Status')),
                ('link', models.CharField(max_length=255, verbose_name='Link')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
    ]
