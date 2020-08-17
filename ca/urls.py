from django.urls import path

from . import views

app_name = 'ca'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.CertificatesOfCAView.as_view(), name='certs_of_ca'),
    path('<int:ca_id>/fillin_p10', views.fillin_p10, name='fillin_p10'),
    path('<int:ca_id>/certify_p10', views.certify_p10, name='certify_p10'),
    path('<int:ca_id>/create_cert', views.create_cert, name='create_cert'),
    path('cert/<int:pk>/', views.DetailCertificateView.as_view(), name='detail_cert'),
    path('cert/<int:cert_id>/download', views.download_cert, name='download_cert'),
    path('cert/<int:cert_id>/downloadp12', views.download_p12, name='download_p12'),
    path('cert/<int:cert_id>/downloadp12b64', views.download_p12_base64, name='download_p12_base64'),
]

