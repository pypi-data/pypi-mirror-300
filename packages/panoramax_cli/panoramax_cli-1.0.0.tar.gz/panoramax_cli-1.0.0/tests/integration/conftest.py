import pytest
import os
from panoramax_cli.model import Panoramax
import requests


@pytest.fixture(scope="session")
def panoramax(pytestconfig):
    """
    If --external-panoramax-url has been given to pytest use an already running panoramax, else spawn a fully configured panoramax for integration tests
    """
    external_panoramax_url = pytestconfig.getoption("--external-panoramax-url")
    if external_panoramax_url:
        yield Panoramax(url=external_panoramax_url)
        return

    from testcontainers import compose

    dco_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "docker-compose-panoramax.yml",
    )
    with compose.DockerCompose(
        ".",
        compose_file_name=dco_file,
        pull=True,
    ) as compose:
        port = compose.get_service_port("panoramax-api", 5000)
        api_url = f"http://api.panoramax.localtest.me:{port}"
        compose.wait_for(api_url)

        yield Panoramax(url=api_url)
        stdout, stderr = compose.get_logs()
        if stderr:
            print("Errors\n:{}".format(stderr))


@pytest.fixture(scope="session")
def user_credential():
    """Credential of a fake created account on keycloak"""
    return ("elysee", "my password")


@pytest.fixture(scope="session")
def panoramax_with_token(panoramax, user_credential):
    token = _get_token(panoramax, user_credential)
    return Panoramax(
        url=panoramax.url,
        token=token,
    )


def _get_token(panoramax, user_credential):
    with requests.session() as s:
        login(s, panoramax, user_credential)
        tokens = s.get(f"{panoramax.url}/api/users/me/tokens")
        tokens.raise_for_status()
        token_link = next(
            t["href"] for t in tokens.json()[0]["links"] if t["rel"] == "self"
        )
        assert token_link
        jwt_token = s.get(token_link)
        jwt_token.raise_for_status()
        return jwt_token.json()["jwt_token"]


def login(session, panoramax, user_credential):
    login = session.get(f"{panoramax.url}/api/auth/login")

    url = _get_keycloak_authenticate_form_url(login)

    r = session.post(
        url,
        data={"username": user_credential[0], "password": user_credential[1]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        allow_redirects=True,
    )

    # a bit hacky, but since for the moment we only submit a form to keycloak, to know if the login was successful,
    # we need to check that we were redirected to panoramax
    r.raise_for_status()
    assert r.history != 0


def _get_keycloak_authenticate_form_url(response):
    """Little hack to parse keycloak HTML to get the url to the authenticate form"""
    import re

    url = re.search('action="(.*login-actions/authenticate[^"]*)"', response.text)

    assert url, f"impossible to find form action in keycloak response: {response.text}"
    url = url.group(1).replace("&amp;", "&")
    return url


@pytest.fixture(scope="function", autouse=True)
def override_config_home(tmp_path):
    """Set XDG_CONFIG_HOME to temporary directory, so tests newer write a real user config file"""
    old_var = os.environ.get("XDG_CONFIG_HOME")

    os.environ["XDG_CONFIG_HOME"] = str(tmp_path)
    yield

    if old_var:
        os.environ["XDG_CONFIG_HOME"] = old_var
    else:
        del os.environ["XDG_CONFIG_HOME"]


def cleanup_panoramax(panoramax):
    """Delete all collections on panoramax"""
    existing_cols = requests.get(f"{panoramax.url}/api/collections")
    existing_cols.raise_for_status()
    for c in existing_cols.json()["collections"]:
        r = requests.delete(
            f"{panoramax.url}/api/collections/{c['id']}",
            headers={"Authorization": f"Bearer {panoramax.token}"},
        )
        r.raise_for_status()
