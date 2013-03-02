# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView

class CreateUserView(FormView):
    template_name = 'registration/newuser.html'
    form_class = UserCreationForm
    success_url = 'about'