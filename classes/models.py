from django.db import models
from django.urls import reverse

class Classroom(models.Model):
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=120)
	year = models.IntegerField()
	teacher = models.ForeignKey()

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})


class Student(models.Model):
	name = models.CharField(max_length=120)
	dob = models.DateField()
	grade = models.IntegerField()
	classroom = models.ForeignKey(on_delete=)
