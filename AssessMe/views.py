# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from AssessMe.forms import UserCreateForm
from AssessMe.models import Classroom, Student


class CreateUserView(FormView):
    template_name = 'registration/newuser.html'
    form_class = UserCreateForm
    success_url = '/About'

    def post(self, request, *args, **kwargs):
        user_form = self.get_form(self.form_class)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username,password=password)
            login(request, user)
            return redirect("/About")
        return render(request, self.template_name, { 'user_form' : user_form })


class ClassroomListView(ListView):
    model = Classroom
    context_object_name = "classrooms"
    template_name = "classrooms/list.html"

class StudentListView(ListView):

    template_name = "students/list.html"
    context_object_name = "students"

    def get_queryset(self):
        return Student.objects.filter(classroom__id = self.kwargs['classroom_id'])



