from django.contrib import admin

from .models import PrivateKey, Certificate, CA


admin.site.register(Certificate)
admin.site.register(PrivateKey)
admin.site.register(CA)
