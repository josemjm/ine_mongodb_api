from django.contrib import admin
from django.urls import path
from ine import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ccaa/list/', views.dict_ccaa_List.as_view()),
    path('ccaa/<str:nombre>/', views.ccaa_Detail.as_view()),
    path('provinces/list/', views.dict_provinces_List.as_view()),
    path('provinces/<str:nombre>/', views.provinces_Detail.as_view()),
    path('municipalities/list/', views.dict_municipalities_List.as_view()),
    path('municipalities/<str:nombre>/', views.municipalities_Detail.as_view()),
    path('suggest_nombre/<str:nombre>/', views.suggest_Nombre.as_view()),
]