from django.views import generic

from .models import CA, Certificate


class IndexView(generic.ListView):
    template_name = 'ca/index.html'
    context_object_name = 'ca_list'

    def get_queryset(self):
        return Certificate.objects.filter(ca__isnull=False)


class CertificatesOfCAView(generic.ListView):
    model = Certificate
    context_object_name = 'certificate_list'
    template_name = 'ca/certs_of_ca.html'

    def get_context_data(self, **kwargs):
        subject = self.object_list[0].subject_text
        context = Certificate.objects\
            .filter(issuer_text__exact=subject)\
            .exclude(subject_text__exact=subject)
        return {
            'ca_name': subject,
            'certificate_list': context,
        }