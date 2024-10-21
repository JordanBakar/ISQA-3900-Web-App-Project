from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User, Group

# Create your views here.
def register(request):
    """View function for user registration."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new user
            uname = form.cleaned_data['username']
            form.save()

            # Get the newly created user and add them to the 'Member' group
            user = User.objects.get(username=uname)
            member_group = Group.objects.get(name='Member')  # Ensure 'Member' group exists in the admin panel
            user.groups.add(member_group)
            user.save()

            # Redirect to the login page after successful registration
            return redirect('login')

        # In case of invalid form, redirect back to the registration page
        return redirect("register")
    else:
        # Display the registration form if the request is GET
        form = RegisterForm()

    return render(request, "register.html", {"form": form})
