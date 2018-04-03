from taiga_contrib_github_auth import connector
from taiga_contrib_github_auth.services import github_login_func as delegate_login_func
from urllib.parse import urljoin
from django.conf import settings
import logging
import requests

logger = logging.getLogger(__name__)


def check_org_membership(github_id, org, headers:dict=connector.HEADERS):
    logger.error("Checking membership of user with github id '{0}' in org {1}...".format(github_id, org))

    """
    Get authenticated user organization membership.    
    """
    url = urljoin(connector.API_URL, "orgs/{0}/members/{1}".format(org, github_id))

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error("User was not a member of GitHub organization {0}.".format(org))
        return False
    else:
        return True



def github_login_func(request):
    logger.error("github_login_func inside taiga_contrib_github_extended_auth....")

    code = request.DATA.get('code', None)
    logger.error("code: {0}".format(code))

    auth_info = connector.login(code)
    logger.error("access token: {0}".format(auth_info.access_token))

    headers = connector.HEADERS.copy()
    headers["Authorization"] = "token {}".format(auth_info.access_token)

    user_info = connector.get_user_profile(headers=headers)
    logger.error("username: {0}".format(user_info.username))

    organization = getattr(settings, "TAIGA_GITHUB_EXTENDED_AUTH_ORG",  None)
    logger.error("organization: {0}".format(organization))

    if organization and check_org_membership(user_info.username, organization, headers):
        logger.error("checking membership...")
        return delegate_login_func(request)
    else:
        return None
