from django import forms
from .models import Customer, Sent, Notification


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ["status"]


class SentForm(forms.ModelForm):
    class Meta:
        model = Sent
        fields = ["from_email", "to_email", "subject", "body", "file", "status"]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Sent
        fields = ["reply"]


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        exclude = ['date_time']
