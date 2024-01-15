import pytest
from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from yanews import settings


TOMORROW = 1


@pytest.fixture
def news():
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def news_id_for_args(news):
    return news.id,


@pytest.fixture
def news_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def comment_tomorrow(news, author):
    comment_tomorrow = Comment.objects.create(
        news=news,
        author=author,
        text='Текст еще одного комментария'
    )
    comment_tomorrow.created = timezone.now() + timedelta(days=TOMORROW)
    comment_tomorrow.save()
    return comment_tomorrow


@pytest.fixture
def comment_id_for_args(comment):
    return comment.id,


@pytest.fixture
def delete_comment_url(comment_id_for_args):
    return reverse('news:delete', args=comment_id_for_args)


@pytest.fixture
def edit_comment_url(comment_id_for_args):
    return reverse('news:edit', args=comment_id_for_args)


@pytest.fixture
def create_news_set():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
