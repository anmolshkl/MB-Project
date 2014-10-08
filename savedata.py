from apps.mentor.models import UserProfile
def savedata(strategy,user, response,is_new=False,*args, **kwargs):
	if strategy.backend.name == 'linkedin':
		userProfile = UserProfile(user=user)
		userProfile.location =  response.get('location')
		userProfile.save()

