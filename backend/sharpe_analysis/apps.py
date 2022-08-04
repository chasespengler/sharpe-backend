from django.apps import AppConfig


class SharpeAnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sharpe_analysis'

    def ready(self):
        import sharpe_analysis.signals
