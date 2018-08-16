from employee_app_without_UI import app
import unittest


class FlaskTestCase(unittest.TestCase):

    # Ensure that we get all employees data
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that we can add new employee details
    def test_add(self):
        tester = app.test_client(self)
        new_employee = {
            'name': 'test',
            'designation': 'test designation',
            'mobile_number': 'test mobile_number',
            'email_id': 'test email_id'
        }
        response = tester.post('/add', json=new_employee)
        self.assertEqual(response.status_code, 200)

    # Ensure that we can update existing employees data
    def test_update(self):
        tester = app.test_client(self)
        update_employee = {
            'id': '10',
            'name': 'updated test',
            'designation': 'test designation',
            'mobile_number': 'test mobile_number',
            'email_id': 'test email_id'
        }
        response = tester.post('/update', json=update_employee)
        self.assertEqual(response.status_code, 200)

    # Ensures that we can delete an employee record
    def test_delete(self):
        tester = app.test_client(self)
        delete_employee = {'id': '11'}
        response = tester.post('/delete', json=delete_employee)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
