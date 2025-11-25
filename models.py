from django.db import models


# Create your models here.


class Customer(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=1000)
    mobile = models.BigIntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    status = models.BigIntegerField(default=3)

    class Meta:
        db_table = 'Customer'


class Admin(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'admin'


class Sent(models.Model):
    from_email = models.EmailField()
    to_email = models.EmailField()
    subject = models.CharField(max_length=500)
    body = models.TextField()
    status = models.CharField(max_length=500, default="NA")
    file = models.FileField(null=True, blank=True)
    reply = models.TextField()
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Sent'


class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification'
