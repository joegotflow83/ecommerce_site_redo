from django.forms import ModelForm
from django import forms
from .models import Contact


class ContactForm(ModelForm):
	"""Create the form for users to contact staff"""

	message = forms.CharField(widget=forms.Textarea)


	class Meta:
		"""Display which fields need to be shown for user to fill out"""

		model = Contact
		fields = ['name', 'email', 'topic', 'message']