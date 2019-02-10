from django.shortcuts import render
from classes.models import Classroom
from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,RetrieveUpdateAPIView,DestroyAPIView
from .serializers import ClassroomListSerializer,ClassroomDetailSerializer,ClassroomUpdateSerializer



class ListView(ListAPIView):
	queryset = Classroom.objects.all()
	serializer_class  = ClassroomListSerializer

class DetailView(RetrieveAPIView):
	queryset = Classroom.objects.all()
	serializer_class  = ClassroomDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'classroom_id'

class CreateView(CreateAPIView):
	serializer_class  = ClassroomListSerializer

	def perform_create(self,serializer):
		serializer.save(teacher = self.request.user)

class UpdateView(RetrieveUpdateAPIView):
	queryset = Classroom.objects.all()
	serializer_class  = ClassroomUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'classroom_id'

class DeleteView(DestroyAPIView):
	queryset = Classroom.objects.all()
	serializer_class  = ClassroomListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'classroom_id'

