from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db
FORM_DATA_NEW = {'text': 'Новый текст комментария'}


def test_anonymous_user_cant_create_comment(client, url_news_detail):
    """Тест: анонимный пользователь не может отправить комментарий."""
    comment_num = Comment.objects.count()
    client.post(url_news_detail, data=FORM_DATA_NEW)
    assert Comment.objects.count() == comment_num


def test_user_can_create_comment(
        admin_client, admin_user, news, url_news_detail
):
    """Тест: авторизованный пользователь может отправить комментарий."""
    comment_set = set(Comment.objects.all())
    response = admin_client.post(url_news_detail, data=FORM_DATA_NEW)
    assertRedirects(response, f'{url_news_detail}#comments')
    comment_set_difference = set(Comment.objects.all()).difference(comment_set)
    assert len(comment_set_difference) == 1
    comment = comment_set_difference.pop()
    assert comment.text == FORM_DATA_NEW['text']
    assert comment.news == news
    assert comment.author == admin_user


def test_user_cant_use_bad_words(admin_client, url_news_detail):
    """Тест: если комментарий содержит запрещённые слова,
    он не будет опубликован, а форма вернёт ошибку.
    """
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    comment_num = Comment.objects.count()
    response = admin_client.post(url_news_detail, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == comment_num


def test_author_can_delete_comment(
    author_client, url_comment_delete, url_news_detail
):
    """Тест: авторизованный пользователь может удалять свои комментарии."""
    url_to_comments = f'{url_news_detail}#comments'
    comment_num = Comment.objects.count()
    response = author_client.delete(url_comment_delete)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == comment_num - 1


def test_user_cant_delete_comment_of_another_user(
    admin_client, url_comment_delete
):
    """Тест: авторизованный пользователь не может удалять чужие комментарии."""
    comment_num = Comment.objects.count()
    response = admin_client.delete(url_comment_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comment_num


def test_author_can_edit_comment(
    author, author_client, comment, url_comment_edit, news, url_news_detail
):
    """Тест: авторизованный пользователь может
    редактировать свои комментарии.
    """
    comment_set = set(Comment.objects.all())
    response = author_client.post(url_comment_edit, data=FORM_DATA_NEW)
    assertRedirects(response, f'{url_news_detail}#comments')
    comment_set_new = set(Comment.objects.all())
    assert len(comment_set_new.difference(comment_set)) == 0
    assert len(comment_set) == len(comment_set_new) == 1
    comment = comment_set_new.pop()
    assert comment.text == FORM_DATA_NEW['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_edit_comment_of_another_user(
    admin_client, comment, url_comment_edit
):
    """Тест: авторизованный пользователь не может
    редактировать чужие комментарии.
    """
    comment_set = set(Comment.objects.all())
    response = admin_client.post(url_comment_edit, data=FORM_DATA_NEW)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_set_new = set(Comment.objects.all())
    assert len(comment_set) == len(comment_set_new) == 1
    comment = comment_set.pop()
    comment_new = comment_set_new.pop()
    assert comment.text == comment_new.text
    assert comment.news == comment_new.news
    assert comment.author == comment_new.author
