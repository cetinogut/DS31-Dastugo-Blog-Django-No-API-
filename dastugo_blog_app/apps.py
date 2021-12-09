from django.apps import AppConfig


class DastugoBlogAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dastugo_blog_app'
    
    def ready(self): # since we have a separate signals.py file , we need to override this method
        import dastugo_blog_app.signals
