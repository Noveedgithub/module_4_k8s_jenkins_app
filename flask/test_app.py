import unittest
from app import app, db, Todo
from flask import Flask
from flask_testing import TestCase

class TestTodoApp(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_todo.db"
    TESTING = True

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False 
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ToDo List', response.data)

    def test_create_todo_item(self):
        response = self.client.post('/', data=dict(title='Test Task', desc='Test Description'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        todo = Todo.query.filter_by(title='Test Task').first()
        self.assertIsNotNone(todo)
        self.assertEqual(todo.description, 'Test Description')

    def test_update_todo_item(self):
        todo = Todo(title='Initial Task', description='Initial Description')
        db.session.add(todo)
        db.session.commit()

        response = self.client.post(f'/update/{todo.task_id}', data=dict(title='Updated Task', desc='Updated Description'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_todo = Todo.query.filter_by(task_id=todo.task_id).first()
        self.assertEqual(updated_todo.title, 'Updated Task')
        self.assertEqual(updated_todo.description, 'Updated Description')

    def test_delete_todo_item(self):
        todo = Todo(title='Delete Task', description='Delete Description')
        db.session.add(todo)
        db.session.commit()

        response = self.client.get(f'/delete/{todo.task_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        deleted_todo = Todo.query.filter_by(task_id=todo.task_id).first()
        self.assertIsNone(deleted_todo)

if __name__ == '__main__':
    unittest.main()
