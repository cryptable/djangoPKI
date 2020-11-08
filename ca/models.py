from django.db import models

class PrivateKey(models.Model):
    """
    Private key field with password
    """
    password_text = models.CharField(max_length=64)
    private_key_text = models.CharField(max_length=10240)


class CA(models.Model):
    """
    Defines a Certification Authority
    """
    crl_number_text = models.CharField(max_length=128)


class Certificate(models.Model):
    """
    Certificate model, where we unravel the certificate to search
    (sizes come from RFC 5280
    """
    common_name_text = models.CharField(max_length=64)
    given_name_text = models.CharField(max_length=16, blank=True, null=True)
    sur_name_text = models.CharField(max_length=40, blank=True, null=True)
    pseudonym_text = models.CharField(max_length=128, blank=True, null=True)
    generation_qualifier_text = models.CharField(max_length=3, blank=True, null=True)
    title_text = models.CharField(max_length=128, blank=True, null=True)
    street_name_text = models.CharField(max_length=128, blank=True, null=True)
    locality_name_text = models.CharField(max_length=128, blank=True, null=True)
    state_name_text = models.CharField(max_length=128, blank=True, null=True)
    organization_name_text = models.CharField(max_length=64, blank=True, null=True)
    organizational_unit_1_name_text = models.CharField(max_length=128, blank=True, null=True)
    organizational_unit_2_name_text = models.CharField(max_length=128, blank=True, null=True)
    organizational_unit_3_name_text = models.CharField(max_length=128, blank=True, null=True)
    organizational_unit_4_name_text = models.CharField(max_length=128, blank=True, null=True)
    organizational_unit_5_name_text = models.CharField(max_length=128, blank=True, null=True)
    postal_code_text = models.CharField(max_length=16, blank=True, null=True)
    country_code_text = models.CharField(max_length=2, blank=True, null=True)
    subject_serial_number_text = models.CharField(max_length=128, blank=True, null=True)    # TODO: length check
    domain_component_1_text = models.CharField(max_length=64, blank=True, null=True)       # TODO: length check
    domain_component_2_text = models.CharField(max_length=64, blank=True, null=True)       # TODO: length check
    domain_component_3_text = models.CharField(max_length=64, blank=True, null=True)       # TODO: length check
    domain_component_4_text = models.CharField(max_length=64, blank=True, null=True)       # TODO: length check
    domain_component_5_text = models.CharField(max_length=64, blank=True, null=True)       # TODO: length check
    email_address_text = models.CharField(max_length=128, blank=True, null=True)            # TODO: length check

    subject_text = models.CharField(max_length=8192)
    issuer_text = models.CharField(max_length=8192)
    serial_number_text = models.CharField(max_length=128)
    certificate_text = models.CharField(max_length=10240)
    private_key = models.OneToOneField(PrivateKey,
                                       on_delete=models.CASCADE,
                                       null=True,
                                       blank=True)
    ca = models.OneToOneField(CA,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
