import pytest

from django.urls import reverse

from yanews import settings


@pytest.mark.usefixtures('create_news_set')
@pytest.mark.django_db
class TestHomePage:
    HOME_URL = reverse('news:home')

    def test_news_count(self, client):
        response = client.get(self.HOME_URL)
        object_list = response.context['object_list']
        assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE

    def test_news_order(self, client):
        response = client.get(self.HOME_URL)
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
@pytest.mark.django_db
def test_comment_form_availability(
    parametrized_client, form_is_available, news_url
):
    response = parametrized_client.get(news_url)
    assert ('form' in response.context) is form_is_available


@pytest.mark.usefixtures('comment', 'comment_tomorrow')
@pytest.mark.django_db
def test_comment_order(client, news_url):
    response = client.get(news_url)
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    assert all_comments[0].created < all_comments[1].created
