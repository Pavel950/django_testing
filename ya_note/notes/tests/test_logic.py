from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.test_shared_data import TestPrepared


class TestNoteCreation(TestPrepared):

    def test_anonymous_user_cant_create_note(self):
        """Тест: анонимный пользователь не может создать заметку."""
        notes_num = Note.objects.count()
        response = self.client.post(self.URL_NOTE_ADD, data=self.form_data)
        expected_url = f'{self.URL_LOGIN}?next={self.URL_NOTE_ADD}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), notes_num)

    def test_user_can_create_note(self):
        """Тест: залогиненный пользователь может создать заметку."""
        Note.objects.all().delete()
        response = self.author_client.post(
            self.URL_NOTE_ADD,
            data=self.form_data
        )
        self.assertRedirects(response, self.URL_SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_not_unique_slug(self):
        """Тест: невозможно создать две заметки с одинаковым slug."""
        self.form_data['slug'] = self.note.slug
        notes_num = Note.objects.count()
        response = self.author_client.post(
            self.URL_NOTE_ADD,
            data=self.form_data
        )
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), notes_num)

    def test_empty_slug(self):
        """Тест: если при создании заметки не заполнен slug,
        то он формируется автоматически.
        """
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_client.post(
            self.URL_NOTE_ADD,
            data=self.form_data
        )
        self.assertRedirects(response, self.URL_SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.author)


class TestNoteEditDelete(TestPrepared):

    def test_author_can_delete_note(self):
        """Тест: пользователь может удалять свои заметки."""
        notes_num = Note.objects.count()
        response = self.author_client.post(self.URL_NOTE_DELETE)
        self.assertRedirects(response, self.URL_SUCCESS)
        self.assertEqual(Note.objects.count(), notes_num - 1)

    def test_user_cant_delete_note_of_another_user(self):
        """Тест: пользователь не может удалять чужие заметки."""
        notes_num = Note.objects.count()
        response = self.reader_client.post(self.URL_NOTE_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_num)

    def test_author_can_edit_note(self):
        """Тест: пользователь может редактировать свои заметки."""
        notes_num = Note.objects.count()
        response = self.author_client.post(
            self.URL_NOTE_EDIT,
            data=self.form_data
        )
        self.assertRedirects(response, self.URL_SUCCESS)
        self.assertEqual(Note.objects.count(), notes_num)
        self.assertEqual(notes_num, 1)
        note_from_db = Note.objects.get()
        self.assertEqual(note_from_db.title, self.form_data['title'])
        self.assertEqual(note_from_db.text, self.form_data['text'])
        self.assertEqual(note_from_db.slug, self.form_data['slug'])
        self.assertEqual(note_from_db.author, self.author)

    def test_user_cant_edit_note_of_another_user(self):
        """Тест: пользователь не может редактировать чужие заметки."""
        notes_num = Note.objects.count()
        response = self.reader_client.post(
            self.URL_NOTE_EDIT,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_num)
        self.assertEqual(notes_num, 1)
        note_from_db = Note.objects.get()
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)
