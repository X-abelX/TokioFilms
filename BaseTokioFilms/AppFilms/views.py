from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import categoryFilms, film
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

# Create your views here.
def index(request):
    return render(request, 'AppFilms/index.html')

def prueba(request):
    return render(request, 'AppFilms/prueba.html')

@login_required
def home(request):
    return render(request, 'AppFilms/home.html')

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    categories = categoryFilms.objects.all().order_by('position')
    return render(request, 'AppFilms/dashboard.html', {'categories': categories})                                                                                                                                                                                       

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'AppFilms/login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'AppFilms/register.html', {'form': form})

@csrf_exempt
def update_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order = data.get("order", [])
        edited_categories = data.get("editedCategories", {})

        for item in order:
            category = categoryFilms.objects.get(id=item["id"])
            category.position = item["position"]
            category.save()

        for id, new_name in edited_categories.items():
            category = categoryFilms.objects.get(id=id)
            category.name = new_name
            category.save()

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)

@require_POST
@csrf_exempt
def add_category(request):
    data = json.loads(request.body)
    category_name = data.get("name")
    if category_name:
        new_category = categoryFilms(name=category_name)
        new_category.save()
        return JsonResponse({"status": "success", "id": new_category.id, "name": new_category.name})
    return JsonResponse({"status": "failed"}, status=400)

from django.views.decorators.http import require_http_methods

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_category(request, category_id):
    try:
        category = categoryFilms.objects.get(id=category_id)
        category.delete()
        return JsonResponse({"status": "success"})
    except categoryFilms.DoesNotExist:
        return JsonResponse({"status": "failed", "message": "Category not found"}, status=404)

@require_POST
@csrf_exempt
def update_category_name(request, category_id):
    data = json.loads(request.body)
    new_name = data.get("name")
    if new_name:
        try:
            category = categoryFilms.objects.get(id=category_id)
            category.name = new_name
            category.save()
            return JsonResponse({"status": "success"})
        except categoryFilms.DoesNotExist:
            return JsonResponse({"status": "failed", "message": "Category not found"}, status=404)
    return JsonResponse({"status": "failed"}, status=400)