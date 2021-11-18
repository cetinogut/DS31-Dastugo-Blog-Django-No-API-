from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from django.contrib.auth.models import User

#admin.site.register(Profile) # moved the Profile into the bolg_app admin file and register it from there, you can do it from here and actually it is better to do it fro mhere. it was just a trial.

# below added custom user Profile info inlina to the default user info.
# https://stackoverflow.com/questions/3400641/how-do-i-inline-edit-a-django-user-profile-in-the-admin-interface
class UserProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False
    
class AccountsUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

# unregister old user admin
admin.site.unregister(User)
# register new user admin that includes a UserProfile
admin.site.register(User, AccountsUserAdmin)
