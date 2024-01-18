import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('create_news_set')
def test_news_count(client, url_home):
    """Тест: количество новостей на главной странице — не более 10."""
    response = client.get(url_home)
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('create_news_set')
def test_news_order(client, url_home):
    """Тест: новости отсортированы от самой свежей к самой старой."""
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.parametrize(
    'parametrized_client, form_is_available',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('admin_client'), True),
    )
)
def test_comment_form_availability(
    parametrized_client, form_is_available, url_news_detail
):
    """Тест: анонимному пользователю недоступна форма для отправки
    комментария на странице отдельной новости,
    а авторизованному доступна.
    """
    response = parametrized_client.get(url_news_detail)
    assert ('form' in response.context) is form_is_available
    if form_is_available:
        assert isinstance(response.context['form'], CommentForm)


@pytest.mark.usefixtures('create_comment_set')
def test_comment_order(client, url_news_detail):
    """Тест: комментарии на странице отдельной новости
    отсортированы в хронологическом порядке.
    """
    response = client.get(url_news_detail)
    assert 'news' in response.context
    all_dates = [comment.created for comment
                 in response.context['news'].comment_set.all()]
    sorted_dates = sorted(all_dates)
    assert all_dates == sorted_dates
