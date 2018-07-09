from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Classroom(models.Model):
	subject = models.CharField(max_length=120)
	grade = models.IntegerField()
	year = models.CharField(max_length=40)
	teacher = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

	def __str__(self):
		return self.subject

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})

class Student(models.Model):
	name = models.CharField(max_length=120)
	dob = models.DateField()
	exam_grade = models.DecimalField(max_digits=5, decimal_places=2)
	classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
	GENDERS = (
	('M', 'Male'),
    ('F', 'Female'),
	)
	gender = models.CharField(
		max_length = 2,
		choices = GENDERS,
		default = 'F',
	)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('student-detail', kwargs={'student_id':self.id})

	class Meta:
		ordering = ('name', 'exam_grade',)
