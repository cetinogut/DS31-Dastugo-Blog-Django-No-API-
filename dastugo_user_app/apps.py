from django.apps import AppConfig


class DastugoUserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dastugo_user_app'

  
    def ready(self): # sınce we have a separate signals.py file , we need to override this method
        import dastugo_user_app.signals
