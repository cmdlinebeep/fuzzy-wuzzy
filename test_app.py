import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
# from models import setup_db, Company, Policy, pop_policies, pop_mock_companies

# from app import APP
# from models import db, Company, Policy


class RoboTermsTestsCase(unittest.TestCase):
    """This class represents the test case for the RoboTerms app"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres:a@localhost:5432/roboterms_test"
        # setup_db(self.app, self.database_path)

        # binds the app to the current context (https://flask.palletsprojects.com/en/1.1.x/appcontext/)
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.app = self.app  # jdw added, not sure
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.drop_all()  # jdw
        #     self.db.create_all()
        #     # pop_policies()

        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path # FIXME: combine above
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        self.db = SQLAlchemy()
        self.db.app = self.app
        self.db.init_app(self.app)

        # self.db.drop_all()
        # self.db.create_all()        
        # pop_mock_companies()

        # APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:a@localhost:5432/roboterms_test'
        # APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # self.app = APP
        # self.client = APP.test_client
        
        # db.drop_all()
        # db.create_all()


        # new Company for testing
        # self.new_co = {
        #     "name": "Facesmash, LLC",
        #     "website": "geturfacesmashed.biz"
        # }

    def tearDown(self):
        """Executed after reach test"""
        pass


    # Unit Tests
    # At least two per endpoint

    def test_get_index(self):
        """Gets the / endpoint and checks valid results"""
        res = self.client().get('/')

        # Here we'll count this as the two tests since this is an extra endpoint 
        # and not much more to test with it    
        self.assertEqual(res.status_code, 200)
        self.assertEqual("This is my capstone project" in res.get_data(as_text=True), True)

    def test_get_all_companies(self):
        """Gets all companies."""
        res = self.client().get('/companies')
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['companies']), 3)

        # self.assertEqual(data['total_questions'], 19)
        # self.assertEqual(len(data['questions']), 10)
        # self.assertEqual(data['questions'][0]['id'], 5)

    # def test_pagination(self):
    #     """Tests the pagination by getting page 2 and looking for known features"""
    #     res = self.client().get('/api/questions?page=2')
    #     data = json.loads(res.data)

    #     # This endpoint should default to page one, which should have id 5 first
    #     # and total questions of 19
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(len(data['categories']), 6)
    #     self.assertEqual(data['total_questions'], 19)
    #     self.assertEqual(len(data['questions']), 9)     # Should be 9 left
    #     self.assertEqual(data['questions'][0]['id'], 15)

    # def test_page_doesnt_exist(self):
    #     """Make sure we get a 404 error on a page which we know doesn't exist"""
    #     res = self.client().get('/api/questions?page=1000')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)  # Now using API-friendly custom error handlers
    #     self.assertEqual(data['error'], 404)


    # def test_delete_question(self):
    #     """Create a new question, then test deleting it"""
        
    #     # Create a test question to delete
    #     new_question = Question(question=self.new_question['question'], answer=self.new_question['answer'], \
    #         category=self.new_question['category'], difficulty=self.new_question['difficulty'])
    #     new_question.insert()
    #     nq_id = new_question.id

    #     # Test added successfully
    #     all_questions = Question.query.all()
    #     self.assertEqual(len(all_questions), 20)    # 19 originally in test DB

    #     # Delete it through route
    #     res = self.client().delete(f'/api/questions/{nq_id}')
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], nq_id)

    # def test_invalid_delete_question(self):
    #     """Try to delete a question that doesn't exist, should get a 404 error"""
    #     res = self.client().delete(f'/api/questions/1000')
    #     data = json.loads(res.data)

    #     self.assertEqual(data['error'], 404)

    # def test_post_new_question(self):
    #     """POST a new question and make sure it's in there on the last page"""
    #     # Count first and before doing any changes
    #     all_questions = Question.query.all()
    #     orig_num_questions = len(all_questions)
    #     self.assertEqual(orig_num_questions, 19)    # 19 originally in test DB

    #     # POST a new question using API endpoint
    #     res = self.client().post('/api/questions', json=self.new_question)
    #     data = json.loads(res.data)
    #     nq_id = data['added']

    #     self.assertEqual(data['success'], True)
        
    #     # The API returns the primary key id of the new question, but this changes with 
    #     # each test run as the DB keeps incrementing the sequence, so don't have a constant
    #     # value to check it against.
    #     # e.g. self.assertEqual(data['added'], ???)
        
    #     # Count that a new question was added, should have 20 after add
    #     all_questions = Question.query.all()
    #     self.assertEqual(len(all_questions), orig_num_questions + 1)    # 19 originally in test DB

    #     # Delete question from database again with another client request.  
    #     # API returns the primary key
    #     res = self.client().delete(f'/api/questions/{nq_id}')
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], nq_id)

    # def test_post_empty_question(self):
    #     """POST a new question without a question or answer, should fail 400"""
    #     empty_question = {
    #         "question": "          ",
    #         "answer": "           ",
    #         "category": "6",
    #         "difficulty": 1
    #     }
    #     res = self.client().post('/api/questions', json=empty_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['error'], 400)

    # def test_get_questions_of_category(self):
    #     """Test GET request of questions only by a certain category"""
    #     # Get all the questions for Geography (id=3), should be 3 questions
    #     res = self.client().get('/api/categories/3/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['total_questions'], 3)

    #     # Get questions for category 100 (doesn't exist, should 404)
    #     res = self.client().get('/api/categories/100/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['error'], 404)

    # def test_question_search(self):
    #     """Search for a term in a question"""
    #     res = self.client().post('/api/questions', json={"searchTerm": "  PeaNUT  "})   # Who invented Peanut Butter?
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(len(data['questions']), 1)
    #     self.assertEqual(data['questions'][0]['id'], 12)

    # # For testing the Quiz:
    # # 
    # # We'll test on the Geography category (3), which has 3 questions [13, 14, 15]
    # # 
    # # From Developer Tools, examples of the Request Payload looks like this:
    # # {previous_questions: [], quiz_category: {type: "click", id: 0}} # 0 is ALL
    # # {previous_questions: [], quiz_category: {type: "Art", id: "2"}}
    # # {previous_questions: [17, 16, 18], quiz_category: {type: "Art", id: "2"}}

    # def test_play_quiz_1(self):
    #     """Tests out the quiz playing functionality"""
    #     # Test Quiz when all 3 questions are left
    #     res = self.client().post('/api/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Geography", "id": "3"}})
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'], True)                 # check success
    #     self.assertIsNotNone(data['question'])                  # check question is not blank
    #     self.assertEqual(data['question']['category'], 3)       # check correct category

    # def test_play_quiz_2(self):
    #     """Tests out the quiz playing functionality"""
    #     # Test Quiz when 2 of 3 have been asked and only one choice left (15)
    #     res = self.client().post('/api/quizzes', json={"previous_questions": [13, 14], "quiz_category": {"type": "Geography", "id": "3"}})
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'], True)                 # check success
    #     self.assertEqual(data['question']['id'], 15)            # check question 15 returns (only choice left)
        
    # def test_play_quiz_3(self):
    #     """Tests out the quiz playing functionality"""
    #     # Test Quiz when no questions are left in category
    #     res = self.client().post('/api/quizzes', json={"previous_questions": [13, 14, 15], "quiz_category": {"type": "Geography", "id": "3"}})
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'], True)                 # check success
    #     self.assertFalse('question' in data)                    # question key isn't in response when no questions left

    # def test_play_quiz_4(self):
    #     """Tests out the quiz playing functionality"""
    #     # Test Quiz with malformed request (category missing).  Should return 400 error.
    #     res = self.client().post('/api/quizzes', json={"previous_questions": [13], "quiz_category": {"type": "Geography"}})
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'], False)                 # check success is false
    #     self.assertEqual(data['error'], 400)                     # error 400, malformed client request


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()