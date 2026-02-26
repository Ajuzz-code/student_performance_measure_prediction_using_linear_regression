from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Course, Prediction, StudentProfile
import pickle,os
from django.conf import settings


#MODEL_PATH = os.path.join(settings.BASE_DIR, 'model.pkl')
#model = pickle.load(open(MODEL_PATH, 'rb'))
model = pickle.load(open(os.path.join(settings.BASE_DIR, 'model.pkl'), 'rb'))


def home(request):
    return render(request, 'home.html')



def register(request):
    courses = Course.objects.all()
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        course = Course.objects.get(id=request.POST['course'])
        user.studentprofile = user.studentprofile = None
        user.save()

        from .models import StudentProfile
        StudentProfile.objects.create(
            user=user,
            roll_no=request.POST['roll_no'],
            course=course,
            year=request.POST['year'],
            contact=request.POST['contact'],
            address=request.POST['address']
        )
        return redirect('login')
    return render(request, 'register.html', {'courses': courses})


def student_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Invalid credentials")
    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')
@login_required
def profile(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {
        'profile': student_profile
    })

@login_required
def predict(request):
    if request.method == "POST":
        attendance = float(request.POST['attendance'])
        previous_marks = float(request.POST['previous_marks'])
        assignments = float(request.POST['assignments'])
        absences = float(request.POST['absences'])

        predicted_marks = model.predict(
            [[attendance, previous_marks, assignments, absences]]
        )[0]

        predicted_marks = round(predicted_marks, 2)
        if predicted_marks < 40:
            result = "Fail"
        elif predicted_marks < 60:
            result = "Pass"
        elif predicted_marks < 75:
            result = "First Class"
        else:
            result = "Distinction"

        Prediction.objects.create(
            student=request.user,
            attendance=attendance,
            previous_marks=previous_marks,
            assignments=assignments,
            absences=absences,
            predicted_marks=predicted_marks
        )
        return render(request, 'result.html', {
            'outcome': predicted_marks,
            'result': result,
            #'confidence': 95   # static confidence (or calculate later)
        })

    return redirect('dashboard')

@login_required
def history(request):
    predictions = Prediction.objects.filter(
        student=request.user
    ).order_by('date')

    dates = [p.date.strftime("%Y-%m-%d %H:%M") for p in predictions]
    probabilities = [p.probability() * 100 for p in predictions]

    return render(request, 'history.html', {
        'predictions': predictions,
        'dates': dates,
        'probabilities': probabilities
    })


def student_logout(request):
    logout(request)
    return redirect('/')

