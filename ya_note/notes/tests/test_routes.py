from http import HTTPStatus

from notes.tests.test_shared_data import TestPrepared


class TestRoutes(TestPrepared):
    URLS_ALL = (
        TestPrepared.URL_HOME,
        TestPrepared.URL_NOTE_ADD,
        TestPrepared.URL_NOTE_EDIT,
        TestPrepared.URL_NOTE_DELETE,
        TestPrepared.URL_NOTE_DETAIL,
        TestPrepared.URL_NOTES_LIST,
        TestPrepared.URL_SUCCESS,
        TestPrepared.URL_LOGIN,
        TestPrepared.URL_SIGNUP,
        TestPrepared.URL_LOGOUT,
    )
    URLS_FOR_AUTHOR_ONLY = (
        TestPrepared.URL_NOTE_EDIT,
        TestPrepared.URL_NOTE_DELETE,
        TestPrepared.URL_NOTE_DETAIL,
    )
    URLS_FOR_USERS_ONLY = (
        TestPrepared.URL_NOTE_ADD,
        TestPrepared.URL_NOTE_EDIT,
        TestPrepared.URL_NOTE_DELETE,
        TestPrepared.URL_NOTE_DETAIL,
        TestPrepared.URL_NOTES_LIST,
        TestPrepared.URL_SUCCESS,
    )

    def test_pages_availability_for_author(self):
        """Тест доступности страниц для автора заметки."""
        for url in self.URLS_ALL:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_user(self):
        """Тест доступности страниц для аутентифицированного пользователя,
        не автора заметки.
        """
        for url in self.URLS_ALL:
            with self.subTest(url=url):
                response = self.reader_client.get(url)
                if url in self.URLS_FOR_AUTHOR_ONLY:
                    self.assertEqual(
                        response.status_code,
                        HTTPStatus.NOT_FOUND
                    )
                else:
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availabilty_for_anonymous_user(self):
        """Тест доступности страниц для анонимного пользователя."""
        for url in self.URLS_ALL:
            with self.subTest(url=url):
                response = self.client.get(url)
                if url in self.URLS_FOR_USERS_ONLY:
                    self.assertRedirects(
                        response,
                        f'{self.URL_LOGIN}?next={url}'
                    )
                else:
                    self.assertEqual(response.status_code, HTTPStatus.OK)
