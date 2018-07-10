from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from classes.models import Classroom, Student
from classes.forms import ClassroomForm, StudentForm, SignupForm, SigninForm
from classes.views import classroom_create, classroom_delete, classroom_update, student_create
from django.http import response

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="admin",
            password='adminadmin',
            )
        self.user.set_password(self.user.password)
        self.user.save()

    def test_create(self):
        classroom = Classroom.objects.create(
            teacher= self.user,
            subject="Science",
            grade=5,
            year="2018",
            )
        student = Student.objects.create(
            name="Laila",
            dob="1995-01-02",
            exam_grade=100,
            classroom=classroom,
            )

class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username="bob",
            password='adminadmin',
            is_staff=True,
            )
        self.user.set_password(self.user.password)
        self.user.save()
        self.user2 = User.objects.create(
            username="bob2",
            password='adminadmin',
            )
        self.user2.set_password(self.user2.password)
        self.user2.save()
        self.user3 = User.objects.create(
            username="bob3",
            password='adminadmin',
            )
        self.user3.set_password(self.user3.password)
        self.user3.save()

        self.classroom_data = {
            "subject": "Science",
            "grade": 5,
            "year": "2018",
            }
        self.student_data = {
            "name": "Laila",
            "dob": "1995-01-02",
            "exam_grade": 100,
        }

        self.classroom_1 = Classroom.objects.create(
            teacher=self.user,
            subject="Classroom 1",
            grade=1,
            year="2018",
            )
        self.student_1_1 = Student.objects.create(
            name="Student 1",
            dob="1995-02-01",
            exam_grade=100,
            classroom=self.classroom_1,
            )
        self.student_1_2 = Student.objects.create(
            name="Student 2",
            dob="1995-02-01",
            exam_grade=98,
            classroom=self.classroom_1,
            )

        self.classroom_2 = Classroom.objects.create(
            teacher=self.user,
            subject="Classroom 2",
            grade=2,
            year="2018",
            )
        self.student_2_1 = Student.objects.create(
            name="Student 1",
            dob="1995-02-01",            
            exam_grade=100,
            classroom=self.classroom_2,
            )
        self.student_2_2 = Student.objects.create(
            name="Student 2",
            dob="1995-02-01",
            exam_grade=98,
            classroom=self.classroom_2,
            )

        self.classroom_3 = Classroom.objects.create(
            teacher=self.user,
            subject="Classroom 1",
            grade=5,
            year="2018",
            )
        self.student_3_1 = Student.objects.create(
            name="Student 1",
            dob="1995-02-01",
            exam_grade=100,
            classroom=self.classroom_3,
            )
        self.student_3_2 = Student.objects.create(
            name="Student 2",
            dob="1995-02-01",
            exam_grade=98,
            classroom=self.classroom_3,
            )

        self.user_data_1 = {
            "username": "bob",
            "password": "adminadmin"
            }
        self.user_data_2 = {
            "username": "billy",
            "password": "adminadmin",
            }
        self.user_data_3 = {
            "username": "bob",
            "password": "",
            }
        self.user_data_4 = {
            "username": "",
            "password": "somepassword",
            }

    def test_classroom_list_view(self):
        list_url = reverse("classroom-list")
        response = self.client.get(list_url)
        for classroom in Classroom.objects.all():
            self.assertIn(classroom, response.context['classrooms'])
            self.assertContains(response, classroom.subject)
            self.assertContains(response, classroom.grade)
            self.assertContains(response, classroom.year)
        self.assertTemplateUsed(response, 'classroom_list.html')
        self.assertEqual(response.status_code, 200)

    def test_classroom_detail_view(self):
        detail_url = reverse("classroom-detail", kwargs={"classroom_id":self.classroom_1.id})
        response = self.client.get(detail_url)
        self.assertContains(response, self.classroom_1.subject)
        self.assertContains(response, self.classroom_1.grade)
        self.assertContains(response, self.classroom_1.year)
        for student in Student.objects.filter(classroom=self.classroom_1):
            self.assertContains(response, student.name)
            # print(student.dob.strftime("%B %d, %Y"))
            # self.assertContains(response, student.dob)
            self.assertContains(response, student.exam_grade)
        self.assertTemplateUsed(response, 'classroom_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_classroom_create_view(self):
        create_url = reverse("classroom-create")
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(create_url)
        request.user = self.user
        response1 = classroom_create(request)
        self.assertEqual(response1.status_code, 200)

        request2 = self.factory.post(create_url, self.classroom_data)
        request2.user = self.user
        response2 = classroom_create(request2)
        self.assertEqual(response2.status_code, 302)

    def test_student_create_view(self):
        create_url = reverse("student-create", kwargs={"classroom_id":self.classroom_2.id})
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(create_url)
        request.user = self.user
        response1 = student_create(request, classroom_id=self.classroom_2.id)
        self.assertEqual(response1.status_code, 200)

        request = self.factory.get(create_url)
        request.user = self.user2
        response1 = student_create(request, classroom_id=self.classroom_2.id)
        self.assertEqual(response1.status_code, 200)

        request = self.factory.get(create_url)
        request.user = self.user3
        response1 = student_create(request, classroom_id=self.classroom_2.id)
        self.assertEqual(response1.status_code, 302)

        request = self.factory.post(create_url, self.student_data)
        request.user = self.user2
        response2 = student_create(request, classroom_id=self.classroom_2.id)
        self.assertEqual(response2.status_code, 302)

        detail_url = reverse("classroom-detail", kwargs={"classroom_id":self.classroom_2.id})
        response = self.client.get(detail_url)
        self.assertTrue(Student.objects.filter(classroom=self.classroom_2, student="Laila").exists())

    def test_classroom_update_view(self):
        update_url = reverse("classroom-update", kwargs={"classroom_id":self.classroom_2.id})
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(update_url)
        request.user = self.user
        response1 = classroom_update(request, classroom_id=self.classroom_2.id)
        self.assertEqual(response1.status_code, 200)

        request = self.factory.get(update_url)
        request.user = self.user2
        response1 = classroom_update(request, classroom_id=self.classroom_2.id)
        self.assertEqual(response1.status_code, 200)

        request = self.factory.get(update_url)
        request.user = self.user3
        response1 = classroom_update(request, classroom_id=self.classroom_2.id)
        self.assertEqual(response1.status_code, 302)

        request2 = self.factory.post(update_url, self.classroom_data)
        request2.user = self.user
        response2 = classroom_update(request2, classroom_id=self.classroom_2.id)
        self.assertEqual(response2.status_code, 302)

    def test_classroom_delete_view(self):
        delete_url = reverse("classroom-delete", kwargs={"classroom_id":self.classroom_1.id})
        request = self.factory.get(delete_url)
        request.user = self.user
        response = classroom_delete(request, classroom_id=self.classroom_1.id)
        self.assertEqual(response.status_code, 302)

        delete_url = reverse("classroom-delete", kwargs={"classroom_id":self.classroom_2.id})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)

    def test_signup_view(self):
        signup_url = reverse("signup")

        response = self.client.get(signup_url)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post(signup_url, self.user_data_1)
        self.assertEqual(response2.status_code, 200)

        response3 = self.client.post(signup_url, self.user_data_2)
        self.assertEqual(response3.status_code, 302)

        response4 = self.client.post(signup_url, self.user_data_3)
        self.assertEqual(response4.status_code, 200)

        response5 = self.client.post(signup_url, self.user_data_4)
        self.assertEqual(response5.status_code, 200)

    def test_signin_view(self):
        signin_url = reverse("signin")
        
        response = self.client.get(signin_url)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post(signin_url, self.user_data_1)
        self.assertEqual(response2.status_code, 302)

        response2 = self.client.post(signin_url, self.user_data_2)
        self.assertEqual(response2.status_code, 200)

        response2 = self.client.post(signin_url, self.user_data_3)
        self.assertEqual(response2.status_code, 200)

        response2 = self.client.post(signin_url, self.user_data_4)
        self.assertEqual(response2.status_code, 200)

    def test_signout_view(self):
        signout_url = reverse("signout")
        response = self.client.get(signout_url)
        self.assertEqual(response.status_code, 302)

class ClassroomFormTestCase(TestCase):
    def test_valid_form(self):
        subject = "Some random classroom"
        grade = 5
        year = "2018"
        data = {
            'subject':subject,
            'grade': grade,
            'year': year,
        }
        form = ClassroomForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('subject'), subject)
        self.assertEqual(form.cleaned_data.get('grade'), grade)

    def test_invalid_form(self):
        subject = "Some classroom"
        year = "Some random year"
        data = {
            'subject':subject,
            'year': year,
        }
        form = ClassroomForm(data=data)
        self.assertFalse(form.is_valid())

class StudentFormTestCase(TestCase):
    def test_valid_form(self):
        name = "A Student"
        dob = "1995-02-01"
        exam_grade = 100
        data = {
            'name':name,
            'dob': dob,
            'exam_grade': exam_grade,
        }
        form = StudentForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('name'), name)
        # self.assertEqual(form.cleaned_data.get('dob'), dob)
        self.assertEqual(form.cleaned_data.get('exam_grade'), exam_grade)

    def test_invalid_form(self):
        name = "A Student"
        dob = "1995-02-01"
        exam_grade = 100
        data = {
            'name':name,
            'dob': dob,
        }
        data2 = {
            'name':name,
            'exam_grade': exam_grade,
        }
        data3 = {
            'exam_grade':exam_grade,
            'dob': dob,
        }
        form = StudentForm(data=data)
        form2 = StudentForm(data=data2)
        form3 = StudentForm(data=data3)
        self.assertFalse(form.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertFalse(form3.is_valid())

class AuthFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="bob",
            password='adminadmin',
        )
        self.user_data_1 = {
            "username": "bob",
            "password": "adminadmin",
        }
        self.user_data_2 = {
            "username": "billy",
            "password": "adminadmin",
        }
        self.user_data_3 = {
            "username": "bob",
            "password": "",
        }
        self.user_data_4 = {
            "username": "",
            "password": "somepassword",
        }

    def test_valid_signin_form(self):
        form = SigninForm(data=self.user_data_1)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('username'), self.user_data_1['username'])
        self.assertEqual(form.cleaned_data.get('password'), self.user_data_1['password'])

    def test_invalid_signin_form(self):
        form = SigninForm(data=self.user_data_3)
        self.assertFalse(form.is_valid())
        form = SigninForm(data=self.user_data_4)
        self.assertFalse(form.is_valid())

    def test_valid_signup_form(self):
        form = SignupForm(data=self.user_data_2)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], self.user_data_2['username'])
        self.assertEqual(form.cleaned_data.get('password'), self.user_data_2['password'])

    def test_invalid_signup_form(self):
        form = SignupForm(data=self.user_data_1)
        self.assertFalse(form.is_valid())
        form = SignupForm(data=self.user_data_3)
        self.assertFalse(form.is_valid())
        form = SignupForm(data=self.user_data_4)

        
        self.assertFalse(form.is_valid())