from django.db import models


class Book(models.Model):
	ROMANS = 'romans'
	SF = 'sf'
	TECHNOLOGY = 'technology'
	HISTORY = 'history'
	FANTASY = 'fantasy'

	GENRE_CHOICES = [
		(ROMANS, 'Romans'),
		(SF, 'Science Fiction'),
		(TECHNOLOGY, 'Technology'),
		(HISTORY, 'Histoire'),
		(FANTASY, 'Fantasy'),
	]

	AVAILABLE = 'available'
	LIMITED = 'limited'
	OUT = 'out'
	RESERVED = 'reserved'

	AVAILABILITY_CHOICES = [
		(AVAILABLE, 'Disponible'),
		(LIMITED, 'Stock limité'),
		(OUT, 'Rupture'),
		(RESERVED, 'Réservé'),
	]

	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255, blank=True)
	genre = models.CharField(max_length=32, choices=GENRE_CHOICES, default=ROMANS)
	description = models.TextField(blank=True)
	cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
	availability = models.CharField(max_length=16, choices=AVAILABILITY_CHOICES, default=AVAILABLE)
	quantity = models.PositiveIntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.title} — {self.author}"

