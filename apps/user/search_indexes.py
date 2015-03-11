from haystack import indexes
from django.contrib.auth.models import User
from apps.user.models import UserProfile

class UserProfileIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	college = indexes.CharField(model_attr='college')
	first_name = indexes.CharField(model_attr='user__first_name')
	last_name = indexes.CharField(model_attr='user__last_name')
	id = indexes.CharField(model_attr='user__id')
	city = indexes.CharField(model_attr='city')
	state = indexes.CharField(model_attr='state')
	#content_auto = indexes.EdgeNgramField(model_attr='city')


	def get_model(self):
		return UserProfile

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()