# Generated by Django 4.0.2 on 2022-04-05 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportstaff',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
