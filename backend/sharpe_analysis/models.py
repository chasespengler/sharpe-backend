from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    '''
    Customer/client model.
    '''

    #Fields
    client_name = models.CharField(max_length=120)
    email = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.client_name

class Portfolio(models.Model):
    '''
    Investment porfolio model. Has a many to one relationship with its parent, Client.

    '''
    
    #Fields
    portfolio_name = models.CharField(max_length=120)

    #Relationships
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.portfolio_name

class Security(models.Model):
    '''
    Investable security model. Has a many to one relationship with its parent, Portfolio.
    '''
    
    #Fields
    SECURITIES = (
        ('Equity', 'Equity'),
        ('Bond', 'Bond'),
        ('Crypto', 'Crypto')
    )
    security_type = models.CharField(max_length=120, choices=SECURITIES)
    ticker = models.CharField(max_length=12)  
    amount = models.FloatField()

    #Relationships
    portfolio_parent = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticker
