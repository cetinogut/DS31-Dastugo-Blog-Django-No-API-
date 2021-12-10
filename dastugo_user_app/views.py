from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

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

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)