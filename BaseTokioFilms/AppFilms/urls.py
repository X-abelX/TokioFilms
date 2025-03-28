from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('update-order/', views.update_order, name='update_order'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('update-category-name/<int:category_id>/', views.update_category_name, name='update_category_name'),
    path('add-film/', views.add_film, name='add_film'),
    path('lista_items/', views.lista_items, name='lista_items'),
    path('film/<int:film_id>/', views.film_detail, name='film_detail'),
    path('films/', views.films, name='films'),
    path('series/', views.series, name='series'),
    path('film/<int:film_id>/like/', views.like_film, name='like_film'),
]

