from django.db import models


# Create your models here.
class nsdl_instrument_details(models.Model):
    sr_no = models.AutoField(primary_key=True)
    isin =  models.TextField(blank=True, null=True)
    issuer_details =  models.TextField(blank=True, null=True)
    type =  models.TextField(blank=True, null=True)
    instrument_details =  models.TextField(blank=True, null=True)
    coupon_details =  models.TextField(blank=True, null=True)
    redemption_details =  models.TextField(blank=True, null=True)
    credit_ratings =  models.TextField(blank=True, null=True)
    listing_details =  models.TextField(blank=True, null=True)
    restructuring =  models.TextField(blank=True, null=True)
    default_details =  models.TextField(blank=True, null=True)
    keycontacts =  models.TextField(blank=True, null=True)
    keydocuments =  models.TextField(blank=True, null=True)
    updated_date =  models.TextField(blank=True, null=True)
    date_scraped = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='nsdl_instrument_details'