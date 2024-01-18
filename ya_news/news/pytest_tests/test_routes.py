from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('url_home'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_news_detail'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_login'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_logout'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_signup'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_comment_delete'),
         pytest.lazy_fixture('author_client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_comment_edit'),
         pytest.lazy_fixture('author_client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_comment_delete'),
         pytest.lazy_fixture('admin_client'),
         HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('url_comment_edit'),
         pytest.lazy_fixture('admin_client'),
         HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability(url, parametrized_client, expected_status):
    """Тест доступности страниц для разных пользователей."""
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_comment_delete'),
        pytest.lazy_fixture('url_comment_edit'),
    )
)
def test_redirect_for_anonymous_client(client, url, url_login):
    """Тест перенаправления анонимного пользователя на страницу авторизации
    при попытке перейти на страницу редактирования или удаления комментария.
    """
    response = client.get(url)
    assertRedirects(response, f'{url_login}?next={url}')
