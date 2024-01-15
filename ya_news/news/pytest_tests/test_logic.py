import pytest
from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA_NEW = {'text': 'Новый текст комментария'}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news_url):
    client.post(news_url, data=FORM_DATA_NEW)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(admin_client, admin_user, news, news_url):
    response = admin_client.post(news_url, data=FORM_DATA_NEW)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA_NEW['text']
    assert comment.news == news
    assert comment.author == admin_user


def test_user_cant_use_bad_words(admin_client, news_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = admin_client.post(news_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    author_client, delete_comment_url, news_url
):
    url_to_comments = news_url + '#comments'
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    admin_client, delete_comment_url
):
    response = admin_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
    author_client, comment, edit_comment_url, news_url
):
    url_to_comments = news_url + '#comments'
    response = author_client.post(edit_comment_url, data=FORM_DATA_NEW)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == FORM_DATA_NEW['text']


def test_user_cant_edit_comment_of_another_user(
    admin_client, comment, edit_comment_url
):
    response = admin_client.post(edit_comment_url, data=FORM_DATA_NEW)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != FORM_DATA_NEW['text']
