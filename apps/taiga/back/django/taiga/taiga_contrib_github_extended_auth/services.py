from taiga_contrib_github_auth import connector
from taiga_contrib_github_auth import github_login_func as delegate_login_func
import logging

logger = logging.getLogger(__name__)

def check_org_membership(github_id, org):
    logger.error("Checking membership of user with github id '{0}' in org {1}...".format(github_id, org))

    # todo implement API call to GitHub to check membership

    return None


def github_login_func(request):
    logger.error("github_login_funs inside taiga_contrib_github_extended_auth....")

    code = request.DATA.get('code', None)

    email, user_info = connector.me(code)

    if check_org_membership(user_info["username"], "BCDevOps"):
        return delegate_login_func(request)
    else:
        return None
