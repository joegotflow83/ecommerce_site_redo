from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext

from .forms import ContactForm
from django.contrib import messages

def contact(request):
	"""Allow users to contact staff"""
	if request.method == 'POST':
		form = ContactForm()
		if form.is_valid():
			our_form = form.save(commit=False)
			our_form.save()
			messages.add_message(request, messages.INFO,
								'Your message has been sent. '
								'Thank you.')
			return redirect('/')
	else:
		form = ContactForm()
	return render(request, 'contact/contact.html', {'form': form,})