from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse

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
        ca_cert = self.object_list[0]
        context = Certificate.objects\
            .filter(issuer_text__exact=ca_cert.subject_text)\
            .exclude(subject_text__exact=ca_cert.subject_text)
        return {
            'ca': ca_cert,
            'certificate_list': context,
        }


def fillin_p10(request, ca_id):
    ca_cert = get_object_or_404(Certificate, pk=ca_id)
    return render(request, 'ca/fillin_p10.html', {
        'ca':ca_cert })


def certify_p10(request, ca_id):
    ca_cert = get_object_or_404(Certificate, pk=ca_id)
    p10 = request.POST['p10']
    return HttpResponseRedirect(reverse('ca:certs_of_ca', args=(ca_id,)))