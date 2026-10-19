from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    available_time = models.CharField(max_length=100)
    doctor_image = models.ImageField(upload_to='doctors/', default='doctors/default_doc.png', blank=True)

    def __str__(self):
        return f"Dr. {self.user.username} ({self.specialization})"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_image = models.ImageField(upload_to='patients/', default='patients/default_pat.png', blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} to {self.doctor.user.username} - {self.status}"