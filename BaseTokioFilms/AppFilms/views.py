from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'AppFilms/index.html')

def login(request):
    return render(request, 'AppFilms/login.html')