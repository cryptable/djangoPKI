import datetime
import os
from binascii import b2a_base64
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.forms import ModelForm

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, pkcs12
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography import x509

from .models import Certificate, PrivateKey


class DetailCertificateView(generic.DetailView):
    model = Certificate
    template_name = 'ca/detail_cert.html'


class IndexView(generic.ListView):
    template_name = 'ca/index.html'
    context_object_name = 'ca_list'

    def get_queryset(self):
        return Certificate.objects.filter(ca__isnull=False)


# TODO refactor the ListView
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
    return render(request, 'ca/fillin_p10.html', {'ca': ca_cert})


def certify_p10(request, ca_id):
    ca_cert = get_object_or_404(Certificate, pk=ca_id)

    # Load CA certificate and private key
    passwd = ca_cert.private_key.password_text
    rsakey = ca_cert.private_key.private_key_text
    key = load_pem_private_key(rsakey.encode('ascii'), passwd.encode('ascii'), default_backend())
    cacert = x509.load_pem_x509_certificate(ca_cert.certificate_text.encode('ascii'), default_backend())

    # Load Request
    p10 = request.POST['p10']
    x509req = x509.load_pem_x509_csr(p10.encode('ascii'), default_backend())

    # Create certificate for it
    sernum = x509.random_serial_number()
    cert = x509.CertificateBuilder()\
        .issuer_name(cacert.subject)\
        .subject_name(x509req.subject)\
        .public_key(x509req.public_key())\
        .serial_number(sernum)\
        .not_valid_before(timezone.now())\
        .not_valid_after(timezone.now() + datetime.timedelta(days=366))\
        .add_extension(x509.KeyUsage(digital_signature=True,
                                     content_commitment=True,
                                     key_encipherment=False,
                                     data_encipherment=False,
                                     key_agreement=False,
                                     key_cert_sign=False,
                                     crl_sign=False,
                                     encipher_only=False,
                                     decipher_only=False), critical=True)\
        .sign(key, hashes.SHA256(), default_backend())

    pemCert = cert.public_bytes(serialization.Encoding.PEM).decode('ascii')
    new_cert = Certificate()
    new_cert.certificate_text = pemCert
    new_cert.serial_number_text = hex(sernum)
    new_cert.subject_text = ",".join(attr.rfc4514_string() for attr in cert.subject)
    new_cert.issuer_text = ",".join(attr.rfc4514_string() for attr in cert.issuer)
    ou_cnt = 0
    dc_cnt = 0
    for attribute in cert.subject:
        if attribute.oid == NameOID.COMMON_NAME:
            new_cert.common_name_text = attribute.value
        if attribute.oid == NameOID.COUNTRY_NAME:
            new_cert.country_code_text = attribute.value
        if attribute.oid == NameOID.LOCALITY_NAME:
            new_cert.locality_name_text = attribute.value
        if attribute.oid == NameOID.STATE_OR_PROVINCE_NAME:
            new_cert.state_name_text = attribute.value
        if attribute.oid == NameOID.STREET_ADDRESS:
            new_cert.street_name_text = attribute.value
        if attribute.oid == NameOID.ORGANIZATION_NAME:
            new_cert.organization_name_text = attribute.value
        if attribute.oid == NameOID.ORGANIZATIONAL_UNIT_NAME:
            if ou_cnt == 0:
                new_cert.organizational_unit_1_name_text = attribute.value
            if ou_cnt == 1:
                new_cert.organizational_unit_2_name_text = attribute.value
            if ou_cnt == 2:
                new_cert.organizational_unit_3_name_text = attribute.value
            if ou_cnt == 3:
                new_cert.organizational_unit_4_name_text = attribute.value
            if ou_cnt == 4:
                new_cert.organizational_unit_5_name_text = attribute.value
            ou_cnt += 1
        if attribute.oid == NameOID.SERIAL_NUMBER:
            new_cert.subject_serial_number_text = attribute.value
        if attribute.oid == NameOID.SURNAME:
            new_cert.sur_name_text = attribute.value
        if attribute.oid == NameOID.GIVEN_NAME:
            new_cert.given_name_text = attribute.value
        if attribute.oid == NameOID.TITLE:
            new_cert.title_text = attribute.value
        if attribute.oid == NameOID.GENERATION_QUALIFIER:
            new_cert.generation_qualifier_text = attribute.value
        if attribute.oid == NameOID.PSEUDONYM:
            new_cert.pseudonym_text = attribute.value
        if attribute.oid == NameOID.DOMAIN_COMPONENT:
            if dc_cnt == 0:
                new_cert.domain_component_1_text = attribute.value
            if dc_cnt == 1:
                new_cert.domain_component_2_text = attribute.value
            if dc_cnt == 2:
                new_cert.domain_component_3_text = attribute.value
            if dc_cnt == 3:
                new_cert.domain_component_4_text = attribute.value
            if dc_cnt == 4:
                new_cert.domain_component_5_text = attribute.value
            dc_cnt += 1
        if attribute.oid == NameOID.EMAIL_ADDRESS:
            new_cert.email_address_text = attribute.value
        if attribute.oid == NameOID.POSTAL_CODE:
            new_cert.postal_code_text = attribute.value
    new_cert.save()
    return HttpResponseRedirect(reverse('ca:certs_of_ca', args=(ca_id,)))


def download_cert(request, cert_id):
    cert = get_object_or_404(Certificate, pk=cert_id)

    response = HttpResponse(cert.certificate_text, content_type="application/force-download")
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(cert.common_name_text.replace(" ", "-") + '.pem')
    return response


def download_p12(request, cert_id):
    certificate = get_object_or_404(Certificate, pk=cert_id)

    # Load CA certificate and private key
    passwd = certificate.private_key.password_text
    rsakey = certificate.private_key.private_key_text
    key = load_pem_private_key(rsakey.encode('ascii'), passwd.encode('ascii'), default_backend())
    cert = x509.load_pem_x509_certificate(certificate.certificate_text.encode('ascii'), default_backend())
    cas = []
    try:
        cacert = Certificate.objects.filter(ca__isnull=False).get(subject_text__exact=certificate.issuer_text)
        while cacert is not None:
            tmp_cacert = x509.load_pem_x509_certificate(cacert.certificate_text.encode('ascii'), default_backend())
            cas.append(tmp_cacert)
            if cacert.subject_text == cacert.issuer_text:
                break
            else:
                cacert = Certificate.objects.filter(ca__isnull=False).get(subject_text__exact=cacert.issuer_text)
    except Certificate.DoesNotExist:
        pass

    p12 = pkcs12.serialize_key_and_certificates(certificate.common_name_text.encode('ascii'),
                                                key,
                                                cert,
                                                cas,
                                                serialization.BestAvailableEncryption(passwd.encode('ascii')))

    response = HttpResponse(p12, content_type="application/force-download")
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(certificate.common_name_text.replace(" ", "-") + '.p12')
    return response


class FillInCertForm(ModelForm):

    class Meta:
        model = Certificate
        fields = ['common_name_text',
                  'organization_name_text',
                  'country_code_text',
                  ]


# TODO Overkill for just a password
class FillInPasswordDetails(ModelForm):

    class Meta:
        model = PrivateKey
        fields = ['password_text']


def create_cert(request, ca_id):
    create_cert_form = FillInCertForm(request.POST or None, initial={
        'common_name_text': 'John Doe Encryption',
        'organization_name_text': 'Company',
        'country_code_text': 'BE', })
    password_form = FillInPasswordDetails(request.POST or None, initial={
        'password_text': 'system', })
    if create_cert_form.is_valid() and password_form.is_valid():
        ca_cert = get_object_or_404(Certificate, pk=ca_id)

        # Load CA certificate and private key
        passwd = ca_cert.private_key.password_text
        rsakey = ca_cert.private_key.private_key_text
        cakey = load_pem_private_key(rsakey.encode('ascii'), passwd.encode('ascii'), default_backend())
        cacert = x509.load_pem_x509_certificate(ca_cert.certificate_text.encode('ascii'), default_backend())

        certificate = create_cert_form.save(commit=False)
        common_name = certificate.common_name_text
        organization_name = certificate.organization_name_text
        common_country_code = certificate.country_code_text
        subject = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
            x509.NameAttribute(NameOID.COUNTRY_NAME, common_country_code), ])
        tmp_private_key = password_form.save(commit=False)

        password = tmp_private_key.password_text
        sernum = x509.random_serial_number()
        key = rsa.generate_private_key(public_exponent=65537,
                                       key_size=2048,
                                       backend=default_backend())
        cert = x509.CertificateBuilder().subject_name(subject) \
            .issuer_name(cacert.subject) \
            .serial_number(sernum) \
            .public_key(key.public_key()) \
            .not_valid_before(timezone.now())\
            .not_valid_after(timezone.now() + datetime.timedelta(days=366))\
            .add_extension(x509.KeyUsage(digital_signature=False,
                                         content_commitment=False,
                                         key_encipherment=True,
                                         data_encipherment=True,
                                         key_agreement=False,
                                         key_cert_sign=False,
                                         crl_sign=False,
                                         encipher_only=False,
                                         decipher_only=False), critical=True)\
            .sign(cakey, hashes.SHA256(), default_backend())
        certificate.serial_number_text = hex(sernum)
        certificate.subject_text = ",".join(attr.rfc4514_string() for attr in cert.subject)
        certificate.issuer_text = ",".join(attr.rfc4514_string() for attr in cert.issuer)
        certificate.certificate_text = cert.public_bytes(serialization.Encoding.PEM).decode('ascii')
        private_key_txt = key.private_bytes(encoding=serialization.Encoding.PEM,
                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                            encryption_algorithm=serialization.BestAvailableEncryption(password.encode('ascii')))

        tmp_private_key.private_key_text = private_key_txt.decode('ascii')
        tmp_private_key.save()
        certificate.private_key = tmp_private_key
        certificate.save()
        return HttpResponseRedirect(reverse('ca:certs_of_ca', args=(ca_id,)))

    return render(request, 'ca/create_cert.html', {
        'create_cert_form': create_cert_form,
        'password_form': password_form,
    })


def download_p12_base64(request, cert_id):
    certificate = get_object_or_404(Certificate, pk=cert_id)

    # Load CA certificate and private key
    passwd = certificate.private_key.password_text
    rsakey = certificate.private_key.private_key_text
    key = load_pem_private_key(rsakey.encode('ascii'), passwd.encode('ascii'), default_backend())
    cert = x509.load_pem_x509_certificate(certificate.certificate_text.encode('ascii'), default_backend())
    cas = []
    try:
        cacert = Certificate.objects.filter(ca__isnull=False).get(subject_text__exact=certificate.issuer_text)
        while cacert is not None:
            tmp_cacert = x509.load_pem_x509_certificate(cacert.certificate_text.encode('ascii'), default_backend())
            cas.append(tmp_cacert)
            if cacert.subject_text == cacert.issuer_text:
                break
            else:
                cacert = Certificate.objects.filter(ca__isnull=False).get(subject_text__exact=cacert.issuer_text)
    except Certificate.DoesNotExist:
        pass

    p12 = pkcs12.serialize_key_and_certificates(certificate.common_name_text.encode('ascii'),
                                                key,
                                                cert,
                                                cas,
                                                serialization.BestAvailableEncryption(passwd.encode('ascii')))

    b64P12 = b2a_base64(p12)
    response = HttpResponse(b64P12, content_type="text/plain")
    return response
