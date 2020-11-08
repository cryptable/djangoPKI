from mozilla_django_oidc.auth import OIDCAuthenticationBackend
import logging


logger = logging.getLogger(__name__)


class MyOIDCAB(OIDCAuthenticationBackend):
    """
    Adapt the basic authentication to the claims of OIDC
    """
    def verify_claims(self, claims):
        for item in claims.items():
            logger.info("Claim: " + item[0] + ":" +item[1])
        verified = super(MyOIDCAB, self).verify_claims(claims)
        is_admin = 'admin' in claims.get('group', [])
        return verified and is_admin