from django.urls import include, path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index),
    path('categories/<int:cat_id>/', views.categories),
    path('categories/<slug:cat_slug>/', views.categories_by_slug),
    path('archive/<year4:year>/', views.archive),

]