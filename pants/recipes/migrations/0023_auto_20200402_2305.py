# Generated by Django 3.0.4 on 2020-04-02 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0022_auto_20200319_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='introduction',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]