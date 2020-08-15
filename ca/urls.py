from django.urls import path

from . import views

app_name = 'ca'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.CertificatesOfCAView.as_view(), name='certs_of_ca')
]

