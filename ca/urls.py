from django.urls import path

from . import views

app_name = 'ca'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.CertificatesOfCAView.as_view(), name='certs_of_ca'),
    path('<int:ca_id>/fillin_p10', views.fillin_p10, name='fillin_p10'),
    path('<int:ca_id>/certify_p10', views.certify_p10, name='certify_p10'),
]

