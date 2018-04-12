from taiga_contrib_github_auth import connector
from taiga_contrib_github_auth.services import github_register
from taiga.auth.services import make_auth_response_data
from urllib.parse import urljoin
from django.conf import settings
import logging
import requests
from taiga.base import exceptions as exc

logger = logging.getLogger(__name__)


def check_org_membership(github_id, org, headers:dict=connector.HEADERS):
    logger.debug("Checking membership of user with github id '{0}' in org {1}...".format(github_id, org))

    """
    Get authenticated user organization membership.    
    """

    url = urljoin(connector.API_URL, "orgs/{0}/memberships/{1}".format(org, github_id))
    logger.debug("Checking via URL {0}.".format(url))

    response = requests.get(url, headers=headers)
    if response.status_code not in [200]:
        logger.debug("User was not a member of GitHub organization {0}.Status was {1}".format(org, response.status_code))
        return False
    else:
        return True



def github_login_func(request):
    logger.debug("Attempting login using taiga_contrib_github_extended_auth plugin....")

    code = request.DATA.get('code', None)
    token = request.DATA.get('token', None)

    auth_info = connector.login(code)

    headers = connector.HEADERS.copy()
    headers["Authorization"] = "token {}".format(auth_info.access_token)

    user_info = connector.get_user_profile(headers=headers)
    username = user_info.username
    logger.debug("username: {0}".format(username))

    organization = getattr(settings, "TAIGA_GITHUB_EXTENDED_AUTH_ORG",  None)
    logger.debug("organization: {0}".format(organization))

    if organization and check_org_membership(username, organization, headers):
        logger.debug("confirmed membership...")

        emails = connector.get_user_emails(headers=headers)

        primary_email = next(filter(lambda x: x.is_primary, emails))

        user = github_register(username=username,
                               email=primary_email,
                               full_name=user_info.full_name,
                               github_id=user_info.id,
                               bio=user_info.bio,
                               token=token)

        return make_auth_response_data(user)
    else:
        raise exc.PermissionDenied(detail="User {0} was not a member of GitHub organization {1} and is not permitted to register for access to this Taiga instance.".format(username, organization))
