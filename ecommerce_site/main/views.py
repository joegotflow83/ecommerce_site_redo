from django.shortcuts import render, render_to_response


def index(request):
	"""Create home page"""
	uid = request.session.get('user')
	if uid is None:
		return render_to_response('main/index.html')
	else:
		return render_to_response(
			'payments/user.html',
			{'user': User.objects.get(pk=uid)}
		)
	return render(request, 'main/index.html')

def about(request):
	"""Create an about page"""
	return render(request, 'main/about.html')