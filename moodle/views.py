from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect 
from .models import User
from .forms import SignUpForm, ProfileChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def homepage(request):
	""" This function is called when the user logs into the portal. \n
	This redirects to another function which inturn returns to a function which redirects to home page of the portal.
	
	:return: returns to another function
	:rtype: function
	
	"""
	if not request.user.is_authenticated:
		return redirect('login')
	return redirect('coursehomepage')

def user_register(request):
    """ This function is called when the user wants to sign up into the portal. \n
	This returns to a sign up html page which has a sign up form. If the form
	satisfies the requirements then a new account is created for the user.

    :return: This returns url of signup page 
    :rtype: link

    """
    if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
        user = form.save()
        return redirect('login')
    else:
      form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request, pk=None):
    """ This function is called when the user clicks on the view profile. \n
	This returns to a profile html page which has all the information the user
	has filled while signing up.

    :return: This returns url of profile page 
    :rtype: link

    """
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'registration/profile.html', args)

def profile_change(request):
	"""This function is called when the user clicks on the edit profile. \n
	This returns to a profile_change html page which contains a form to which 
	we can fill and update user's information.
	
	:return: This returns url of profile_change page
	:rtype: link
	
	"""
	if not request.user.is_authenticated:
		return redirect('logout')

	if request.method == 'POST':
		form = ProfileChangeForm(request.POST,instance = request.user)
		if form.is_valid():
			form.save()
			return redirect('homepage')

	else:
		form = ProfileChangeForm(instance = request.user)
	args = {'form': form }
	return render(request,'registration/profile_change.html',args)


def change_pass(request):
	""" This function is called when the user clicks on the change password. \n
	This returns to a paasword_change html which contains a form that can be filled to change the password.
	
	:return: This returns url of password_change page
	:rtype: link
	
	"""
	if not request.user.is_authenticated:
		return redirect('logout')

	if request.method == 'POST':
		form = PasswordChangeForm(data = request.POST,user = request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user) 
			return redirect('homepage')
		else:
			form = PasswordChangeForm(user = request.user)
			args = {'form': form , 'success': False}
			return render(request,'registration/password_change.html',args)

	else:
		form = PasswordChangeForm(user = request.user)
		args = {'form': form , 'success': True}
		return render(request,'registration/password_change.html',args)
