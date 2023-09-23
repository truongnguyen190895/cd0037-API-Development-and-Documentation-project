import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from settings import DB_TEST_NAME, DB_USER, DB_PASSWORD
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_TEST_NAME
        self.database_path = "postgresql://{}/{}".format(
            DB_USER + ":" + DB_PASSWORD + "@localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories_success(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["categories"]) > 0)

    def test_categories_method_not_allowed(self):
        """Test sending a method not allowed (e.g., POST) to /categories (405 error)."""
        response = self.client().post("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 405)

    def test_get_questions_success(self):
        """Test retrieving questions successfully."""
        response = self.client().get("/questions?page=1")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["questions"]) > 0)
        self.assertTrue(data["total_questions"] > 0)

    def test_get_questions_page_2(self):
        """Test retrieving questions for page 2."""
        response = self.client().get("/questions?page=2")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["questions"]) > 0)
        self.assertTrue(data["total_questions"] > 0)

    def test_get_questions_error(self):
        """Test accessing a nonexistent page (404 error)."""
        response = self.client().get("/questions?page=9999")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)

    def test_delete_question_success(self):
        """Test deleting a question successfully."""
        # Create a test question to delete
        test_question = Question(
            question="Test question",
            answer="Test answer",
            category="1",
            difficulty=1,
        )
        test_question.insert()

        # Get the question ID to delete
        question_id = test_question.id

        response = self.client().delete(f"/questions/{question_id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["question_id"], question_id)

    def test_delete_question_failure(self):
        """Test deleting a nonexistent question (404 error)."""
        nonexistent_question_id = 9999  # An ID that doesn't exist

        response = self.client().delete(f"/questions/{nonexistent_question_id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)

    def test_create_question_success(self):
        """Test adding a new question successfully."""
        new_question = {
            "question": "What is 2 + 2?",
            "answer": "4",
            "category": "1",
            "difficulty": 1,
        }
        response = self.client().post("/questions", json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created_question_id"] > 0)

    def test_create_question_error(self):
        """Test adding a new question with missing fields (422 error)."""
        invalid_question = {"question": "What is 2 + 2?"}
        response = self.client().post("/questions", json=invalid_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 422)

    def test_get_questions_by_category_success(self):
        """Test retrieving questions by category success."""
        category_id = 1
        response = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["totalQuestions"] > 0)

    def test_get_questions_by_category_failure(self):
        """Test retrieving questions for a nonexistent category (404 error)."""
        nonexistent_category_id = 9999  # A category ID that doesn't exist
        response = self.client().get(f"/categories/{nonexistent_category_id}/questions")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)

    def test_get_quiz_question_success(self):
        """Test retrieving a quiz question success."""
        # Create a payload with a category ID and previous questions
        payload = {
            "quiz_category": {"id": 1},  # Replace with a valid category ID
            "previous_questions": [1, 2],  # IDs of questions that don't exist
        }

        response = self.client().post("/quizzes", json=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])

    def test_get_quiz_question_fail(self):
        """Test retrieving a quiz without quiz_category."""
        payload = {"previous_questions": []}

        response = self.client().post("/quizzes", json=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
