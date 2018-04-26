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

    url = urljoin(connector.API_URL, "orgs/{0}/members/{1}".format(org, github_id))
    logger.debug("Checking via URL {0}.".format(url))
    logger.debug("Headers: {0}".format(headers))

    response = requests.get(url, headers=headers)
    if response.status_code not in [204, 302]:
        logger.debug("User was not a member of GitHub organization {0}.Status was {1}".format(org, response.status_code))
        return False
    else:
        return True


# a twiddled replacement for the login method in taiga-contrib-github-auth/connector.py that requests a broader scope
def login(access_code:str, client_id: str=connector.CLIENT_ID, client_secret: str=connector.CLIENT_SECRET,
          headers: dict=connector.HEADERS):
    """
    Get access_token fron an user authorized code, the client id and the client secret key.
    (See https://developer.github.com/v3/oauth/#web-application-flow).
    """
    if not connector.CLIENT_ID or not connector.CLIENT_SECRET:
        raise connector.GitHubApiError({"error_message": _("Login with github account is disabled. Contact "
                                                 "with the sysadmins. Maybe they're snoozing in a "
                                                 "secret hideout of the data center.")})

    url = urljoin(connector.URL, "login/oauth/access_token")

    # note -> scope: read:user instead of "user:email"; required to determine *private* org membership
    params={"code": access_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "user:emails"}
    data = connector._post(url, params=params, headers=headers)
    return connector.AuthInfo(access_token=data.get("access_token", None))


def github_login_func(request):
    logger.debug("Attempting login using taiga_contrib_github_extended_auth plugin....")

    code = request.DATA.get('code', None)
    token = request.DATA.get('token', None)

    auth_info = login(code)

    headers = connector.HEADERS.copy()
    headers["Authorization"] = "token {}".format(auth_info.access_token)

    user_info = connector.get_user_profile(headers=headers)
    username = user_info.username
    logger.debug("username: {0}".format(username))

    organization = getattr(settings, "TAIGA_GITHUB_EXTENDED_AUTH_ORG",  None)
    logger.debug("organization: {0}".format(organization))

    if organization and check_org_membership(username, organization, headers=headers):
        logger.debug("confirmed membership...")

        emails = connector.get_user_emails(headers=headers)

        primary_email = next(filter(lambda x: x.is_primary, emails)).email

        logger.debug("Primary email is {}".format(primary_email))

        user = github_register(username=username,
                               email=primary_email,
                               full_name=user_info.full_name,
                               github_id=user_info.id,
                               bio=user_info.bio,
                               token=token)

        return make_auth_response_data(user)
    else:
        raise exc.PermissionDenied(detail="User {0} was not a member of GitHub organization {1} and is not permitted to register for access to this Taiga instance.".format(username, organization))
