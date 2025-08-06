"""
URL configuration for DjangoSchool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from accounts.views import LoginView, LogoutView, RegisterView, DeleteUserView, EditUserView, AssignSubject
from school.forms import AddGradeObjectForm
from school.views import GradesView, AddGradeView, AddSubjectView, ShowUsersView, DeleteGradeView, \
    EditGradeView, CreateGradeObjectView, AddGradesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name='base.html'), name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register", RegisterView.as_view(), name="register"),
    path("grades", GradesView.as_view(), name="grades"),
    path("grades/delete/<int:pk>", DeleteGradeView.as_view(), name="delete_grade"),
    path("grades/edit/<int:pk>", EditGradeView.as_view(), name="edit_grade"),
    path("add_grade", AddGradeView.as_view(), name="add_grade"),
    path("add_subject", AddSubjectView.as_view(), name="add_subject"),
    path("show_users", ShowUsersView.as_view(), name="show_users"),
    path("show_users/delete/<int:pk>", DeleteUserView.as_view(), name="delete_user"),
    path("show_users/edit/<int:pk>", EditUserView.as_view(), name="edit_user"),
    path("assign_subject", AssignSubject.as_view(), name="assign_subject"),
    path("create_grade_object", CreateGradeObjectView.as_view(), name="create_grade_object"),
    path("add_grades", AddGradesView.as_view(), name="add_grades"),

]
