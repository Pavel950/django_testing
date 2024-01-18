from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()
SLUG = 'slug'


class TestPrepared(TestCase):
    URL_HOME = reverse('notes:home')
    URL_LOGIN = reverse('users:login')
    URL_LOGOUT = reverse('users:logout')
    URL_SIGNUP = reverse('users:signup')
    URL_NOTE_ADD = reverse('notes:add')
    URL_NOTE_EDIT = reverse('notes:edit', args=(SLUG,))
    URL_NOTE_DELETE = reverse('notes:delete', args=(SLUG,))
    URL_NOTE_DETAIL = reverse('notes:detail', args=(SLUG,))
    URL_NOTES_LIST = reverse('notes:list')
    URL_SUCCESS = reverse('notes:success')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='title',
            text='text',
            slug=SLUG,
            author=cls.author
        )
        cls.form_data = {
            'title': 'new title',
            'text': 'new text',
            'slug': 'new-slug'
        }
