
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from classes import views
from classes_api.views import ClassroomListAPIView, ClassroomDetailAPIView, ClassroomCreateAPIView, ClassroomUpdateView, ClassroomDeleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('classrooms/', views.classroom_list, name='classroom-list'),
    path('classrooms/<int:classroom_id>/', views.classroom_detail, name='classroom-detail'),

    path('classrooms/create', views.classroom_create, name='classroom-create'),
    path('classrooms/<int:classroom_id>/update/', views.classroom_update, name='classroom-update'),
    path('classrooms/<int:classroom_id>/delete/', views.classroom_delete, name='classroom-delete'),

    path('classrooms/<int:classroom_id>/students/create', views.student_create, name='student-create'),
    path('classrooms/<int:classroom_id>/students/<int:student_id>/update/', views.student_update, name='student-update'),
    path('classrooms/<int:classroom_id>/students/<int:student_id>/delete/', views.student_delete, name='student-delete'),

    path('signup/',views.signup ,name='signup'),
    path('signin/',views.signin ,name='signin'),
    path('signout/',views.signout ,name='signout'),

    path('api/classrooms/list/', ClassroomListAPIView.as_view(), name='api-classroom-list'),
    path('api/classrooms/detail/<int:classroom_id>/', ClassroomDetailAPIView.as_view(), name='api-classroom-detail'),
    path('api/classrooms/create/', ClassroomCreateAPIView.as_view(), name='api-classroom-create'),
    path('api/classrooms/update/<int:classroom_id>/', ClassroomUpdateView.as_view(), name='api-classroom-update'),
    path('api/classrooms/delete/<int:classroom_id>/', ClassroomDeleteView.as_view(), name='api-classroom-delete'),
]

if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
