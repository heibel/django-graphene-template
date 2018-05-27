from urllib.parse import urlencode

from django.urls import reverse


def test_missing_header(client):
    query = """
        query {
            viewer {
                email
            }
        }
    """

    expected = {"data": {"viewer": None}}

    url = "{}?{}".format(reverse("graphql"), urlencode({"query": query}))
    response = client.get(url)
    result = response.json()

    assert response.status_code == 200
    assert result == expected


def test_invalid_header(client, token):
    query = """
        query {
            viewer {
                email
            }
        }
    """

    expected = {"data": {"viewer": None}}

    url = "{}?{}".format(reverse("graphql"), urlencode({"query": query}))
    response = client.get(url, HTTP_AUTHORIZATION=token.replace("Bearer", "JWT"))
    result = response.json()

    assert response.status_code == 200
    assert result == expected


def test_invalid_token(client):
    query = """
        query {
            viewer {
                email
            }
        }
    """

    expected = {"data": {"viewer": None}}

    url = "{}?{}".format(reverse("graphql"), urlencode({"query": query}))
    response = client.get(url, HTTP_AUTHORIZATION="Bearer some.invalid.token")
    result = response.json()

    assert response.status_code == 200
    assert result == expected


def test_authenticated_user(client, user, token):
    query = """
        query {
            viewer {
                email
            }
        }
    """

    expected = {"data": {"viewer": {"email": user.email}}}

    url = "{}?{}".format(reverse("graphql"), urlencode({"query": query}))
    response = client.get(url, HTTP_AUTHORIZATION=token)
    result = response.json()

    assert response.status_code == 200
    assert result == expected
