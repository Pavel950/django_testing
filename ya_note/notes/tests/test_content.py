from notes.forms import NoteForm
from notes.tests.test_shared_data import TestPrepared


class TestContent(TestPrepared):
    def test_notes_list_for_user(self):
        """Тест: в список заметок одного пользователя
        не попадают заметки другого пользователя.
        """
        response = self.reader_client.get(self.URL_NOTES_LIST)
        object_list = response.context['object_list']
        self.assertEqual(len(object_list), 0)

    def test_notes_list_for_author(self):
        """Тест: отдельная заметка передаётся на страницу
        со списком заметок автора.
        """
        response = self.author_client.get(self.URL_NOTES_LIST)
        object_list = response.context['object_list']
        self.assertEqual(len(object_list), 1)
        note_from_list = object_list[0]
        self.assertEqual(note_from_list.title, self.note.title)
        self.assertEqual(note_from_list.text, self.note.text)
        self.assertEqual(note_from_list.slug, self.note.slug)
        self.assertEqual(note_from_list.author, self.note.author)

    def test_pages_contains_form(self):
        """Тест: на страницы создания и редактирования заметки
        передаются формы.
        """
        urls = (self.URL_NOTE_ADD, self.URL_NOTE_EDIT)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
