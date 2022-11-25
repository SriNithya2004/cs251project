from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

# Create your forms here.

class NewUserForm(UserCreationForm):
	"""This form is to fill the credentials of the user to login to the portal. \n
	This is a default form with default fields namely username, password.
	Already signed in user log in using this.

	"""
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class SignUpForm(UserCreationForm):
    """This form is to fill the credentials of a newuser to sign up into the portal. \n
	This is a default form with default fields namely username, password, email, name.

    """
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role' )

class ProfileChangeForm(UserChangeForm):
	"""This form is to change the credentials of the user. \n
	This is a default form with default fields namely email, first_name, last_name.

	"""
	class Meta:
		model = User
		fields = (
		'email',
		'first_name',
		'last_name',
		)