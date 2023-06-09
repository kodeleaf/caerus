# Generated by Django 3.2.19 on 2023-05-16 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convertpvs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='audit_log',
            fields=[
                ('cpv_audit_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('in_file_name', models.CharField(max_length=250)),
                ('out_file_name', models.CharField(max_length=250)),
                ('converted_datetime', models.CharField(max_length=60)),
                ('user_name', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=25, null=True)),
                ('cpv_System_Name', models.CharField(default='CPV', max_length=45)),
                ('profile_name', models.CharField(default='Pharma', max_length=45)),
            ],
        ),
    ]
