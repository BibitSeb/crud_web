import unittest
from flask import Flask
from appl import app, db, Stud  

class TestStudentDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        cls.app.config['SECRET_KEY'] = "hi"  
        cls.client = cls.app.test_client()

        with cls.app.app_context():  
            cls.db = db
            cls.db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():  
            cls.db.session.remove()
            cls.db.drop_all()

    def setUp(self):
        with self.app.app_context():
            self.student = Stud(id=1, name="John Doe", age=20)
            self.db.session.add(self.student)
            self.db.session.commit()    

    def tearDown(self):
        with self.app.app_context():
            self.db.session.query(Stud).delete()
            self.db.session.commit()            

    def test_add_student(self):
        with self.app.app_context():
            response = self.client.post('/add', data=dict(id=2, nam='Alice', age=22), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Student details is entered succesfully !', response.data) 
            student = Stud.query.filter_by(id=2).first()
            self.assertIsNotNone(student)
            self.assertEqual(student.name, 'Alice')
            self.assertEqual(student.age, 22)
             
            

    def test_add_student_invalid_id(self):
        response = self.client.post('/add', data=dict(id=-1, nam='Jane Doe', age=25), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ID must be a positive integer.', response.data)     

    def test_add_student_invalid_age(self):
        response = self.client.post('/add', data=dict(id=2, nam='Alice Smith', age=-5), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Age must be a non-negative integer.', response.data)   

    def test_value_error(self):
        response = self.client.post('/add', data=dict(id='asd', nam='John Doe', age=20), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid numeric value for ID and age.', response.data)  

    def test_unique_constraint_violation(self):
        response = self.client.post('/add', data=dict(id=1, nam='Jane Doe', age=25), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'UNIQUE constraint error occurred. Please try again later.',response.data)

    def test_del_student(self):
        with self.app.app_context():
            student=Stud.query.filter_by(id=1).first()
            self.assertIsNotNone(student)

            response=self.client.post('/delete',data=dict(id=1),follow_redirects=True)
            self.assertEqual(response.status_code,200)
            self.assertIn(b'Student with ID 1 has been deleted.',response.data)

            student=Stud.query.filter_by(id=1).first()
            self.assertIsNone(student)

    def test_del_student_nonexistent_id(self):
            response=self.client.post('/delete',data=dict(id=2),follow_redirects=True)    
            self.assertEqual(response.status_code,200)
            self.assertIn(b'No student found with ID 2.',response.data)    

    def test_del_student_invalid_id(self):
        response=self.client.post('/delete',data=dict(id=-2),follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'ID must be a positive integer.',response.data)

    def test_del_student_error(self):
        response=self.client.post('/delete',data=dict(id='ab'),follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Please enter a valid numeric value for ID.',response.data)

    def test_update_student(self):
        response=self.client.post('/update',data=dict(id=1,nam="Alice",age=23),follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Student with ID 1 has been updated.',response.data)
        with self.app.app_context():
            student=Stud.query.filter_by(id=1).first()
            self.assertIsNotNone(student) 
            self.assertEqual(student.name,"Alice")
            self.assertEqual(student.age,23)

    def test_update_student_nonexistent_id(self):
            response=self.client.post('/update',data=dict(id=2,nam="Alice",age=23),follow_redirects=True)    
            self.assertEqual(response.status_code,200)
            self.assertIn(b'No student found with ID 2',response.data)    

    def test_update_student_invalid_id(self):
        response=self.client.post('/update',data=dict(id=-2,nam="Alice",age=23),follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'ID must be a positive integer.',response.data)

    
    def test_update_student_invalid_age(self):
        response=self.client.post('/update',data=dict(id=2,nam="Alice",age=-23),follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Age must be a non-negative integer.',response.data)

    def test_update_student_error1(self):
        response=self.client.post('/update',data=dict(id='ab',nam="Alice",age=23),follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Please enter a valid numeric value for ID and age.',response.data)         
            
    def test_update_student_error2(self):
        response=self.client.post('/update',data=dict(id=1,nam="Alice",age='asd'),follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Please enter a valid numeric value for ID and age.',response.data)         

    def test_view(self):
        response = self.client.get('/view')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'1', response.data)
        self.assertIn(b'John Doe', response.data)
        self.assertIn(b'20', response.data)

if __name__ == "__main__":
    unittest.main()
