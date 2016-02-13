from django.shortcuts import render


def index(request):
	"""Create home page"""
	return render(request, 'main/index.html')