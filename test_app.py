import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Company, Policy
#, pop_mock_companies, pop_policies
# from models import test_db
# Used to manually clean up messes the test makes
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


        # Reset the test DB to a clean slate on each test run
        # test_db(self.db)
        # self.db.drop_all()
        # self.db.create_all()  

        # Add new companies
        # new_co = Company(name="Green Cola, Inc.", website="gcola.com")
        # new_co.insert()

        # new_co = Company(name="Googolplex AtoZ Data", \
        #     website="stopdoingevilwheneverconvenient.com")
        # new_co.insert()

        # new_co = Company(name="Spy App Inc.", website="spyonyourlovedones--butlovingly.com")
        # new_co.insert()      
        # pop_mock_companies()
        # pop_policies()

        if not os.getenv('CLIENT_TOKEN'):
            raise RuntimeError("Environment variables are not set, did you source setup.sh?")

        self.headers_client = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.getenv('CLIENT_TOKEN')
        }

        self.headers_admin = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.getenv('ADMIN_TOKEN')
        }

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
        self.new_co = {
            "name": "Facesmash, LLC",
            "website": "geturfacesmashed.biz"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass


    # Unit Tests

    # At least two per endpoint

    # For the simple GET endpoints (/, /companies, /policies), test both as a public user 
    # (no 'Authorization' header), and as a member (with header).  
    # Header should not break the public access.
    def test_get_index_public(self):
        """Gets the / endpoint as public user and checks valid results"""
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)
        self.assertEqual("This is my capstone project" in res.get_data(as_text=True), True)

    def test_get_index_member(self):
        """Gets the / endpoint as a member and checks valid results"""
        res = self.client().get('/', headers=self.headers_client)

        self.assertEqual(res.status_code, 200)
        self.assertEqual("This is my capstone project" in res.get_data(as_text=True), True)

    def test_get_all_companies_public(self):
        """Gets all companies as a public user and checks status and count."""
        res = self.client().get('/companies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['companies']), 3)

    def test_get_all_companies_member(self):
        """Gets all companies as a member and checks status and count."""
        res = self.client().get('/companies', headers=self.headers_client)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['companies']), 3)

    def test_get_all_policies_public(self):
        """Gets all policies as a public user and checks status and count."""
        res = self.client().get('/policies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['policies']), 4)

    def test_get_all_policies_member(self):
        """Gets all policies as a public user and checks status and count."""
        res = self.client().get('/policies', headers=self.headers_client)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['policies']), 4)

    def test_get_rendered_policy_valid(self):
        """Gets a valid rendered policy."""
        res = self.client().get('/rendered_policy/1/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual("TERMS OF SERVICE" in data['policy'], True)
        self.assertEqual("gcola.com" in data['policy'], True)

    def test_get_rendered_policy_invalid_company(self):
        """Attempts to get the rendered policy for an invalid company id."""
        res = self.client().get('/rendered_policy/1000/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    def test_get_rendered_policy_invalid_policy(self):
        """Attempts to get the rendered policy for an invalid policy id."""
        res = self.client().get('/rendered_policy/1/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_new_company(self):
        """Attempts to create a new company as Client."""
        res = self.client().post('/company', headers=self.headers_client, json=self.new_co)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        # Delete the company we added directly through the DB session
        Company.query.get(data['id']).delete()

    def test_post_new_company_without_token(self):
        """Attempts to create a new company without a token."""
        res = self.client().post('/company', json=self.new_co)
        
        self.assertEqual(res.status_code, 401)  # Should return Unauthorized
        
    def test_post_existing_company(self):
        """Attempts to create a new company with same name as existing one."""
        existing_co = {
            "name": "Spy App Inc.",
            "website": "spyonyourlovedones--butlovingly.com"
        }
        res = self.client().post('/company', headers=self.headers_client, json=existing_co)
        
        self.assertEqual(res.status_code, 422)  # Unprocessable
    
    def test_post_company_missing_name(self):
        """Attempts to create a new company but missing a name."""
        new_co = {
            "website": "abcdefghijklmnopqrstuvwxyz.gov"
        }
        res = self.client().post('/company', headers=self.headers_client, json=new_co)
        
        self.assertEqual(res.status_code, 422)  # Unprocessable

    def test_post_company_as_admin(self):
        """Attempts to create a new company as Admin."""
        res = self.client().post('/company', headers=self.headers_admin, json=self.new_co)
        
        self.assertEqual(res.status_code, 403)  # Should return as Forbidden (invalid permissions)

    def test_delete_company(self):
        """Attempts to delete a company successfully as Client."""
        # Create a test company to delete
        new_co = Company(name="we're toast, LLC", website="dooooooooooommmmed.com")
        new_co.insert()
        new_co_id = new_co.id

        # Make sure it added successfully
        all_companies = Company.query.all()
        self.assertEqual(len(all_companies), 4)    # 3 originally in test DB

        # Delete it through route
        res = self.client().delete(f'/company/{new_co_id}', headers=self.headers_client)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], new_co_id)

    def test_delete_nonexistent_company(self):
        """Attempts to delete a company that doesn't exist."""
        res = self.client().delete(f'/company/1000', headers=self.headers_client)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)  # Not Found
        self.assertEqual(data['success'], False)
        
    def test_delete_company_without_credentials(self):
        """Attempts to delete a company without any credentials."""
        res = self.client().delete(f'/company/1')
        data = json.loads(res.data)

        # AuthError throw different JSON format, no 'success' key
        self.assertEqual(res.status_code, 401)  # Unauthorized
        self.assertEqual(data['code'], "missing_auth_header")

    def test_delete_company_wrong_role(self):
        """Attempts to delete a company with a role that doesn't have correct permissions."""
        res = self.client().delete(f'/company/1', headers=self.headers_admin)
        data = json.loads(res.data)

        # AuthError throw different JSON format, no 'success' key
        self.assertEqual(res.status_code, 403)  # Forbidden
        self.assertEqual(data['code'], "forbidden")

    def test_update_policy(self):
        """Attempts to update a policy successfully as an Admin."""
        # Get current name of policy 1
        pol_1 = Policy.query.get(1)
        orig_name = pol_1.name

        # Change the policy name to FOOBAZ
        res = self.client().patch('/policy/1', headers=self.headers_admin, json={"name": "FOOBAZ"})
        data = json.loads(res.data)

        # Check that it updated OK
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Fetch from the /policies endpoint to make sure the name changed
        res = self.client().get('/policies')
        data = json.loads(res.data)
        
        self.assertEqual(len(data['policies']), 4)  # Make sure length of /policies remains the same
        self.assertNotEqual(orig_name, data['policies'][0]['name'])

        # Now put the name back
        res = self.client().patch('/policy/1', headers=self.headers_admin, json={"name": "Terms of Service"})
        
        # And fetch new policies
        res = self.client().get('/policies')
        data = json.loads(res.data)

        # Check that it updated OK
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        for policy in data['policies']: # Can't count on ordering
            if policy['id'] == 1:
                updated_name = policy['name']
                break
        self.assertEqual(updated_name, "Terms of Service")

    def test_update_nonexistent_policy(self):
        """Attempts to update a policy that doesn't exist."""
        res = self.client().patch('/policy/1000', headers=self.headers_admin, json={"name": "FOOBAZ"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)  # Not Found
        self.assertEqual(data['success'], False)

    def test_update_policy_without_credentials(self):
        """Attempts to update a policy without credentials."""
        res = self.client().patch('/policy/1', json={"name": "FOOBAZ"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)  # Unauthorized
        self.assertEqual(data['code'], "missing_auth_header")

    def test_update_policy_wrong_credentials(self):
        """Attempts to update a policy with incorrect credentials."""
        res = self.client().patch('/policy/1', headers=self.headers_client, json={"name": "FOOBAZ"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)  # Forbidden
        self.assertEqual(data['code'], "forbidden")



    # Test error handlers
    def test_404(self):
        """Test 404 error handler is API'd"""
        res = self.client().get('/companies/abcdefghijk')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['success'], False)
        





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