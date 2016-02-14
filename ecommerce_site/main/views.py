from django.shortcuts import render


def index(request):
	"""Create home page"""
	return render(request, 'main/index.html')

def about(request):
	"""Create an about page"""
	return render(request, 'main/about.html')