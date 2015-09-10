from django.db import models
from django.forms import ModelForm

class TitleQuery(models.Model):
	query = models.TextField()

#class TitleQueryForm(ModelForm):
#	class Meta:
#		model = TitleQuery