from django.db import models

class SecurityStats(models.Model):
    '''
    Security Stats model used to store information about each security
    '''

    #Fields
    ticker = models.CharField(max_length=12, unique=True, primary_key=True)
    mean = models.FloatField(null=True)
    sd = models.FloatField(null=True)

    def __str__(self):
        return self.ticker
