from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

class PaymentForm(forms.Form):
	"""Create payment form for users to pay through stripe"""

	def addError(self):
		"""Populate an error if the form is not valid"""
		self._errors[NON_FIELD_ERRORS] = self.error_class([message])


class SigninForm(PaymentForm):
	"""Create the form for users to log on too"""

	email = forms.EmailField(required=True)
	password = forms.CharField(
		required=True, 
		widget=forms.PasswordInput(render_value=False)
	)


class CardForm(PaymentForm):
	"""Create the form for inputting the users CC info"""

	last_4_digits = forms.CharField(
		required=True,
		min_length=4,
		max_length=4,
		widget=forms.HiddenInput()
	)
	stripe_token = forms.CharField(
		required=True,
		widget=forms.HiddenInput()
	)

class RegisterForm(CardForm):
	"""Create the form for user registration"""

	name = forms.CharField(required=True)
	email = forms.CharField(required=True)
	password = forms.CharField(required=True,
								label=(u'Password'),
								widget=forms.PasswordInput)
	ver_password = forms.CharField(
		required=True,
		label=(u'Verify Password'),
		widget=forms.PasswordInput(render_value=True)
	)

	def clean(self):
		"""Verify that the passwords match up accordingly"""
		cleaned_data = self.cleaned_data
		password = cleaned_data.get('password')
		ver_password = cleaned_data.get('ver_password')
		if password != ver_password:
			raise forms.ValidationError('Passwords do not match')
		return cleaned_data