from django.db import IntegrityError
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
import stripe

from payments.forms import SigninForm, CardForm, RegisterForm
from payments.models import User
from ecommerce_site import settings
import datetime


stripe.api_key = settings.STRIPE_SECRET

def time():
	"""Return the month and year"""
	time = datetime.date.today() + datetime.timedelta(days=30)
	return {'month': time.month, 'year': time.year}

def sign_in(request):
	"""Allow a user to sign in"""
	user = None
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			results = User.objects.filter(email=form.cleaned_data['email'])
			if len(results) == 1:
				results[0].check_password(form.cleaned_data['password'])
				request.session['user'] = results[0].pk
				return redirect('/')
			else:
				form.addError('Incorrect email address or password')
	else:
		form = SigninForm()

	print(form.non_field_errors())
	return render_to_response(
		'payments/sign_in.html',
		{
			'form': form,
			'user': user
		},
		context_instance=RequestContext(request)
	)

def sign_out(request):
	"""Allow a user to sign out"""
	del request.session['user']
	return redirect('/')

def register(request):
	"""Allow a user to register"""
	user = None
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			# update customer based on billing payment(Subscription vs One Time)
			customer = stripe.Customer.create(
				email=form.cleaned_data['email'],
				description=form.cleaned_data['name'],
				card=form.cleaned_data['stripe_token'],
				plan='gold'
			)
			'''customer = stripe.Customer.create(
					email=form.cleaned_data['email'],
					card=form.cleaned_data['stripe_token'],
					amount='100',
					currency='usd'
			)'''
			user = User(
				name=form.cleaned_data['name'],
				email=form.cleaned_data['email'],
				last_4_digits=form.cleaned_data['last_4_digits'],
				stripe_id=customer.id
			)
			# Ensure password is encrypted
			user.set_password(form.cleaned_data['password'])
			try:
				user.save()
			except IntegrityError:
				form.addError(user.email + ' is already a member')
			else:
				request.session['user'] = user.pk
				return redirect('/')
	else:
		form = RegisterForm()
	return render_to_response(
		'payments/register.html',
		{
			'form': form,
			'months': range(1, 13),
			'publishable': settings.STRIPE_PUBLISHABLE,
			'time': time(),
			'user': user,
			'years': range(2016, 2036),
		},
		context_instance=RequestContext(request)
	)

def edit(request):
	"""Allow a user to edit their profile"""
	uid = request.session.get('user')
	if uid is None:
		return redirect('/')
	user = User.objects.get(pk=uid)
	if request.method == 'POST':
		form = CardForm(request.POST)
		if form.is_valid():
			customer = stripe.Customer.retrieve(user.stripe_id)
			customer.card = form.cleaned_data['stripe_token']
			customer.save()
			user.last_4_digits = form.cleaned_data['last_4_digits']
			user.stripe_id = customer.id
			user.save()
			return redirect('/')
	else:
		post = CardForm()
	return render_to_response(
		'payments/edit.html',
		{
			'form': form,
			'publishable': settings.STRIPE_PUBLISHABLE,
			'time': time(),
			'months': range(1, 13),
			'years': range(2016, 2036),
		},
		context_instance=RequestContext(request)
	)
