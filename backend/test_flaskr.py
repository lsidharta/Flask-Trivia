import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "lieke", "Glen2865", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'New test question',
            'answer': 'New test answer',
            'category': 1,
            'difficulty': 1
        }

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
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        with self.app.app_context():
            questions = Question.query.all()
            if questions == []: 
                self.assertEqual(data["total_questions"], 0) 
                self.assertEqual(data["questions"], []) 
            else:
                self.assertTrue(data["total_questions"])
                self.assertTrue(len(data["questions"]))

        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data["success"], True) 
        self.assertTrue(len(data["categories"]))

    def test_422_get_questions_page_exceeded(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)
        with self.app.app_context():
            questions = Question.query.all()
        # If table questions is empty
        if questions == []: 
            self.assertEqual(data["total_questions"], 0) 
            self.assertEqual(data["questions"], []) 
        # If table questions has data
        else: 
            self.assertTrue(data["total_questions"])
            self.assertEqual(len(data["questions"]), 0)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question(self):
        with self.app.app_context():
            res = self.client().delete("/questions/6")
            data = json.loads(res.data)
            questions = Question.query.all()
            question = Question.query.filter(Question.id == 6).one_or_none()

        # If table questions empty and question not exist
        if question is None: # tested OK 
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "unprocessable")
        else:
            self.assertEqual(res.status_code, 200) 
            self.assertEqual(data["success"], True)
            self.assertEqual(data["deleted"], 6)
            self.assertTrue(data["total_questions"])

    def test_422_question_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
    
    def test_405_if_create_question_not_allowed(self):
        res = self.client().post("/questions/1000", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(len(data["categories"]))

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        with self.app.app_context():
            questions = Question.query.all()
            if questions == []: # tested OK
                self.assertEqual(data["total_questions"], 0) # tested OK if question empty
                self.assertEqual(data["questions"], []) # tested OK if question empty
            else:
                self.assertTrue(data["total_questions"])
                self.assertTrue(len(data["questions"]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
                
    def test_search_questions_with_result(self):
        res = self.client().post("/questions", json={"searchTerm": "test1"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 0)

    def test_search_questions_without_result(self):
        res = self.client().post("/questions", json={"searchTerm": "test2"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 0)

    def test_quizz(self):
        res = self.client().post("/questions", json={"previous_questions":[12], "quiz_category":{"type":"click", "id":"0"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()