from apps.mentor.models import UserProfile
def savedata(backend, user, response, *args, **kwargs):
	if backend.name == 'facebook':
		obj = UserProfile()
		profile = obj.create_user_profile(user,user,false)
		profile.gender = response.get('gender')
		profile.save()