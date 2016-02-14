from django.forms import ModelForm
from django import forms
from .models import Contact


class ContactForm(ModelForm):


	message = forms.CharField(widget=forms.Textarea)


	class Meta:


		model = Contact
		fields = ['name', 'email', 'topic', 'message']