from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from telemedicine.models import Doctor, Appointment, PatientProfile

# 1. HOME & AI SEARCH
def home(request):
    all_doctors = Doctor.objects.all()
    query = request.GET.get('q')
    if query:
        all_doctors = all_doctors.filter(specialization__icontains=query)
    return render(request, 'home.html', {'doctors': all_doctors})

# 2. PATIENT AUTH
def login_page(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('patient_dashboard')
    return render(request, 'login.html')

def register_page(request):
    if request.method == "POST":
        # உங்க ரிஜிஸ்ட்ரேஷன் லாஜிக் இங்கே இருக்கும்
        return redirect('login')
    return render(request, 'register.html')

# 3. PATIENT DASHBOARD
@login_required
def patient_dashboard(request):
    my_appointments = Appointment.objects.filter(user=request.user)
    profile = PatientProfile.objects.filter(user=request.user).first()
    return render(request, 'patient_dashboard.html', {'appointments': my_appointments, 'profile': profile})

@login_required
def update_profile(request):
    profile = get_object_or_404(PatientProfile, user=request.user)
    if request.method == "POST":
        profile.age = request.POST.get('age')
        profile.gender = request.POST.get('gender')
        profile.save()
        return redirect('patient_dashboard')
    return render(request, 'update_profile.html', {'profile': profile})

@login_required
def cancel_appointment(request, appt_id):
    appointment = get_object_or_404(Appointment, id=appt_id, user=request.user)
    appointment.delete()
    return redirect('patient_dashboard')

# 4. DOCTOR MODULES
def doctor_register(request):
    if request.method == "POST":
        return redirect('doctor_login')
    return render(request, 'doctor_register.html')

def doctor_login(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user and Doctor.objects.filter(user=user).exists():
            login(request, user)
            return redirect('doctor_dashboard')
    return render(request, 'doctor_login.html')

@login_required
def doctor_dashboard(request):
    doctor_obj = get_object_or_404(Doctor, user=request.user)
    if request.method == "POST":
        appt_id = request.POST.get('appointment_id')
        action = request.POST.get('action')
        appt = Appointment.objects.get(id=appt_id)
        if action == "accept": appt.status = "Accepted"
        elif action == "reject": appt.status = "Rejected"
        appt.save()
    return render(request, 'doctor_dashboard.html', {
        'appointments': Appointment.objects.filter(doctor=doctor_obj),
        'doctor': doctor_obj
    })

def logout_user(request):
    logout(request)
    return redirect('home')