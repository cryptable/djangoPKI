from django.contrib import admin
from django import forms
from .models import PrivateKey, Certificate, CA


class CertficateModelForm(forms.ModelForm):
    certificate_text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Certificate
        fields = '__all__'


class PrivateKeyModelForm(forms.ModelForm):
    private_key_text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PrivateKey
        fields = '__all__'


class CertificateAdmin(admin.ModelAdmin):
    form = CertficateModelForm


class PrivateKeyAdmin(admin.ModelAdmin):
    form = PrivateKeyModelForm


admin.site.register(Certificate, CertificateAdmin)
admin.site.register(PrivateKey, PrivateKeyAdmin)
admin.site.register(CA)
