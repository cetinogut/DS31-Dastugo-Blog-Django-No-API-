from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm



def register(request):
    form = RegistrationForm(request.POST or None)
    if request.user.is_authenticated: # avouid user to manually reach users/register path if he has already registered
        messages.warning(request, "You already have an account!")
        return redirect("dastugo_blog_app:post-list")
    if form.is_valid():
        form.save()
        name = form.cleaned_data["username"]
        messages.success(request, f"Account created for {name}")
        return redirect("login")

    context = {
        "form": form,
    }

    return render(request, "dastugo_user_app/register.html", context)



def profile(request):
    # obj = User.objects.get(id=id)
    u_form = UserUpdateForm(request.POST or None, instance=request.user) # we will join to forms in the same html page
        
    p_form = ProfileUpdateForm(
        request.POST or None, request.FILES or None, instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, "Your profile has been updated!!")
        return redirect(request.path)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }

    return render(request, "dastugo_user_app/profile.html", context)