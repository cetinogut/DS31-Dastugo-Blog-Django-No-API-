from django.urls import path
from django.contrib.auth import views as auth_views # as a best practive we renamed the views
from .views import register, profile # used in Web Framework
from .views import CustomUserCreate, BlacklistTokenUpdateView #added for API
from .forms import PasswordResetEmailCheck

app_name = 'dastugo_user_app'

urlpatterns = [
    #path('create/', CustomUserCreate.as_view(), name="create_user"), #added for API
    #path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), # added for aPI
     #    name='blacklist'),
    
    path("register/", register, name="register"), # in Django Web framework app
    path("profile/", profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="dastugo_user_app/login.html"), name="login"), # name must be login. can't change it
    path("logout/", auth_views.LogoutView.as_view(template_name="dastugo_user_app/logout.html"), name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='dastugo_user_app/password_reset_email.html', form_class=PasswordResetEmailCheck), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='dastugo_user_app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='dastugo_user_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='dastugo_user_app/password_reset_complete.html'), name='password_reset_complete'),    
   
]

