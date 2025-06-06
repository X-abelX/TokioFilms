# Importamos los modelos de Django mas algunas funcionalidades.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, UserProfileForm, UserPasswordChangeForm
from .models import categoryFilms, film, UserLike , userlistadd
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from datetime import datetime
from django.contrib import messages

# Cramos nuestra vista principal. 
def index(request):
    return render(request, 'AppFilms/index.html')

# Creamos la vista de login.
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
    return render(request, 'AppFilms/auth/login.html', {'form': form})

# Creamos la vista de registro.
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
    return render(request, 'AppFilms/auth/register.html', {'form': form})

# Creamos la vista Home en donde el usuario ira una vez logueado.
@login_required
def home(request):
    # Fetch top 10 films based on likes
    top_films = film.objects.filter(type='pelicula', likes__gt=0).order_by('-likes')[:10]
    top_series = film.objects.filter(type='serie', likes__gt=0).order_by('-likes')[:10]

    # Fetch latest films and series
    latest_films = film.objects.filter(type='pelicula', releaseDate__isnull=False).order_by('-releaseDate')[:10]
    latest_series = film.objects.filter(type='serie', releaseDate__isnull=False).order_by('-releaseDate')[:10]

    # Fetch recommendations based on user's liked categories
    user_likes = UserLike.objects.filter(user=request.user)
    liked_categories = user_likes.values_list('film__categoryFilms', flat=True)
    recommended_films = film.objects.filter(categoryFilms__in=liked_categories).order_by('?')[:10]

    return render(request, 'AppFilms/home/home.html', {
        'top_films': top_films,
        'top_series': top_series,
        'latest_films': latest_films,
        'latest_series': latest_series,
        'recommended_films': recommended_films,
    })

# Creamos una vista que nos proporcione todas las peliculas 
@login_required
def films(request):
    categories = categoryFilms.objects.all().order_by('position').prefetch_related('film_set')
    films = film.objects.all()
    return render(request, 'AppFilms/films/films.html', {'categories': categories, 'films': films})

# Creamos una vista que nos proporcione todas las series.
@login_required
def series(request):
    categories_with_series = []
    for category in categoryFilms.objects.all():
        series_count = category.film_set.filter(type='serie').count()
        if series_count > 0:
            categories_with_series.append({
                'category': category,
                'series_count': series_count
            })
    
    return render(request, 'AppFilms/series/series.html', {'categories': categories_with_series})

# Creamos una vista que nos proporcione las peliculas de nuestra lista
@login_required
def mylist(request):
    # Retrieve films from the user's list
    my_list_films = film.objects.filter(userlistadd__user=request.user).distinct()
    
    # Retrieve films that the user has liked
    liked_films = film.objects.filter(userlike__user=request.user).distinct()

    return render(request, 'AppFilms/mylist/mylist.html', {
        'my_list': my_list_films,
        'liked_films': liked_films,
    })

# Creamos una vista en la que podremos buscar peliculas y series.
@login_required
def search(request):
    films = film.objects.all()
    return render(request, 'AppFilms/search/search.html', {'films': films})

#creamos una vista en la que podremos hacer cambios en nuestro perfil.
@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        user = request.user

        # Update username and email
        user.username = username
        user.email = email

        # Check if new password is provided and matches
        if new_password and new_password == confirm_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # Keep the user logged in
            else:
                messages.error(request, 'Current password is incorrect.')
                return redirect('profile')

        user.save()
        messages.success(request, 'Your profile was successfully updated!')
        return redirect('profile')

    return render(request, 'AppFilms/profile/profile.html')


# Creamos una vista para ver los detalles de una pelicula o serie.
@login_required
def category_detail(request, category_id, type):
    category = get_object_or_404(categoryFilms, id=category_id)
    films = category.film_set.filter(type=type)  # Filter films by the specified type ('pelicula' or 'serie')

    return render(request, 'AppFilms/category/category.html', {
        'category': category,
        'films': films,
    })


# Creamos una vista de administracion en donde podremos crear, editar y eliminar peliculas y series. Solo se podra acceder a esta vista si eres un usuario administrador.
@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    categories = categoryFilms.objects.all().order_by('position').prefetch_related('film_set')
    films = film.objects.all()
    return render(request, 'AppFilms/dashboard/dashboard.html', {'categories': categories, 'films': films})                                                                                                                                                                                      

# Creamos una funcionalidad en la que podamos actualizar el orden de las categorias y editar el nombre de las mismas.
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


# Creamos una funcionalidad en la que podamos añadir categorias nuevas.
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


#Creamos una funcionalidad en la que podamos eliminar categorias.
@require_http_methods(["DELETE"])
@csrf_exempt
def delete_category(request, category_id):
    try:
        category = categoryFilms.objects.get(id=category_id)
        category.delete()
        return JsonResponse({"status": "success"})
    except categoryFilms.DoesNotExist:
        return JsonResponse({"status": "failed", "message": "Category not found"}, status=404)


#Creamos una funcionalidad en la que podamos editar el nombre de las categorias.
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


#Creamos una funcionalidad en la que podamos añadir peliculas nuevas.
@login_required
def add_film(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        age = request.POST.get("age")
        duration = request.POST.get("duration") if request.POST.get("type") == "pelicula" else None
        releaseDate = request.POST.get("releaseDate")
        image = request.FILES.get("image")
        videoQuality = request.POST.get("videoQuality")
        cast = request.POST.get("cast")
        category_id = request.POST.get("category")
        film_type = request.POST.get("type")

        if category_id == "null":
            return redirect("dashboard")

        category = categoryFilms.objects.get(id=category_id)

        # Convertir la fecha al formato YYYY-MM-DD
        try:
            releaseDate = datetime.strptime(releaseDate, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return redirect("dashboard")

        # Handle series-specific fields
        seasons = request.POST.get("seasons") if film_type == "serie" else None
        episodes = request.POST.get("episodes") if film_type == "serie" else None

        # Create a new film object
        new_film = film(
            title=title,
            description=description,
            age=age,
            duration=duration,
            releaseDate=releaseDate,
            image=image,
            videoQuality=videoQuality,
            cast=cast,
            categoryFilms=category,
            type=film_type,  # Set the type (movie or series)
            seasons=seasons,
            episodes=episodes,
        )

        new_film.save()

        return redirect("dashboard")

    return redirect("dashboard")

#creamos una funcionalidad para poder ver las categorias
def lista_items(request):
    categories = categoryFilms.objects.all().order_by('position') # Obtener los datos actualizados
    return render(request, 'AppFilms/components/list.html', {'categories': categories})

#creamos una funcionalidad para poder ver los likes y listas
@login_required
def film_detail(request, film_id):
    film_instance = get_object_or_404(film, id=film_id)
    user_like_exists = UserLike.objects.filter(user=request.user, film=film_instance).exists()
    user_list_exists = userlistadd.objects.filter(user=request.user, film=film_instance).exists()
    category = film_instance.categoryFilms # Fetch categories related to the film

    return render(request, 'AppFilms/components/film_detail.html', {
        'film': film_instance,
        'user_like_exists': user_like_exists,
        'user_list_exists': user_list_exists,
        'category': category,  # Pass categories to the template
    })

# creamos una funcionalidad para dar likes a las peliculas y series.
@login_required
def like_film(request, film_id):
    film_instance = get_object_or_404(film, id=film_id)
    user_like = UserLike.objects.filter(user=request.user, film=film_instance).first()
    
    if user_like:
        # If the user has already liked the film, remove the like
        user_like.delete()
        if film_instance.likes > 0:
            film_instance.likes -= 1
    else:
        # If the user has not liked the film, add a like
        UserLike.objects.create(user=request.user, film=film_instance)
        film_instance.likes += 1
    
    film_instance.save()
    return redirect('film_detail', film_id=film_id)


# creamos una funcionalidad para añadir peliculas y series a nuestra lista.  
@login_required
def add_to_list(request, film_id):
    film_instance = get_object_or_404(film, id=film_id)
    user_list_item = userlistadd.objects.filter(user=request.user, film=film_instance).first()

    if user_list_item:
        # If the film is already in the list, remove it
        user_list_item.delete()
    else:
        # If the film is not in the list, add it
        userlistadd.objects.create(user=request.user, film=film_instance)

    return redirect('film_detail', film_id=film_id)