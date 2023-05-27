from django.db import models

# Create your models here.
class Add_Profile(models.Model):
    profile_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    profile_name = models.CharField(max_length=45, default='Pharma')
    in_file_path = models.TextField()
    out_file_path = models.TextField()
    archieve_path = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=50, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(null=True,max_length=50)

class audit_log(models.Model):
    cpv_audit_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    in_file_name= models.CharField( max_length=250)
    out_file_name = models.CharField( max_length=250)
    converted_datetime =models.CharField(max_length=60)
    user_name = models.CharField(max_length=50, null=True)
    status =models.CharField(max_length=25, null=True)
    cpv_System_Name = models.CharField(max_length=45, default='CPV')
    profile_name = models.CharField(max_length=45, default='Pharma')