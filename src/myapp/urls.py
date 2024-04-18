

from django.urls import path, include

from . import views

urlpatterns = [
    path('pass-image/', views.ImageOCRView.as_view())
]
