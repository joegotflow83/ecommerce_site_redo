from django.db import models
import datetime

class Contact(models.Model):


	name = models.CharField(max_length=32)
	email = models.EmailField(max_length=255)
	topic = models.CharField(max_length=255)
	message = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		"""Return prettier output"""
		return self.email

	class Meta:


		ordering = ['-timestamp']