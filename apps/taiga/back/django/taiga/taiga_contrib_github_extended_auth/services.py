from taiga_contrib_github_auth import connector
from taiga_contrib_github_auth.services import github_login_func as delegate_login_func
from urllib.parse import urljoin
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def check_org_membership(github_id, org, headers:dict=connector.HEADERS):
    logger.error("Checking membership of user with github id '{0}' in org {1}...".format(github_id, org))

    """
    Get authenticated user organization membership.    
    """
    url = urljoin(connector.API_URL, "orgs/{0}/members/{1}".format(org, github_id))
    try:
        connector._get(url, headers=headers)
        return True
    except connector.GitHubApiError as error:
        logger.error("User was not a member of GitHub organization {0}. Error was: {1}".format(org, error))
        return False


def github_login_func(request):
    logger.error("github_login_func inside taiga_contrib_github_extended_auth....")

    code = request.DATA.get('code', None)
    logger.error("code: {0}".format(code))

    email, user_info = connector.me(code)
    logger.error("email: {0}".format(email))
    logger.error("username: {0}".format(user_info.username))

    auth_info = connector.login(code)

    headers = connector.HEADERS.copy()
    headers["Authorization"] = "token {}".format(auth_info.access_token)

    organization = getattr(settings, "TAIGA_GITHUB_EXTENDED_AUTH_ORG",  None)
    logger.error("organization: {0}".format(organization))

    if organization and check_org_membership(user_info.username, organization, headers):
        logger.error("checking membership...")
        return delegate_login_func(request)
    else:
        return None
