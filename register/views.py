from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User, Group

def register(request):
    """View function for user registration."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new user
            uname = form.cleaned_data['username']
            form.save()

            # Get the newly created user
            user = User.objects.get(username=uname)

            # Ensure the 'Member' group exists, create it if it doesn't
            member_group, created = Group.objects.get_or_create(name='Member')
            if created:
                print("Created the 'Member' group.")

            # Add the user to the 'Member' group
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
