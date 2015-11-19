from django.shortcuts import render
from forms import TextForm,ImageForm,StoryForm,EditForm,EditFormImage
from django.template.context_processors import csrf
from django.forms.formsets import formset_factory
from models import Story,Text,Image,Person,RELATIONSHIP_FOLLOWING,User_Info,Profile_Image,Star
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import login
from django_comments.views.comments import post_comment
from django_comments.models import Comment
from django.utils.timesince import timesince
from sorl.thumbnail import get_thumbnail

def stream_readers(id,string):
	#Stream to all users who follows.
	user,created = Person.objects.get_or_create(name_id = id,id = id)
	followers = user.get_followers()
	import user_streams
	user_streams.add_stream_following(followers, string)
	return True
	

def stream_feed(id,string):
	#Stream to all users who follows.
	user,created = Person.objects.get_or_create(name_id = id,id = id)
	followers = user.get_followers()
	import user_streams
	user_streams.add_stream_feed(followers, string)
	
def stream_user(id,string):
	#Stream to all users who follows.
	user = User.objects.get(id = id)
	import user_streams
	user_streams.add_stream_item(user,string)
	return True

def add_star(request):
	if request.POST:
		#Get the story ID
		id = request.POST.get("storyid")
		#Fetch the story
		story = Story.objects.get(storyid = id)
		star = story.starcount
		#Get the star object. If it is not created, create 1 for user.
		starobject,created = Star.objects.get_or_create(storyid = story,user_id = request.user)
		if created:
			#Increment the story star by 1
			story.starcount = star + 1
			story.save()
			#Tell the author of story that the user has star the story
			stream_user(story.user_id,str(request.user.id)+":star your story:"+str(story.storyid))
			#Tell the user following that the user has star the story
			stream_readers(request.user.id,str(request.user.id)+":star a story:"+str(story.storyid))
			
		import json
		data = {}
		data['string'] = "<button type=\"button\" class=\"btn btn-success\" id = \"star\" value = \"" + str(story.storyid) + "\">Star <span>" + str(story.starcount) + "</span></button>"
		return HttpResponse(json.dumps(data), content_type = "application/json")
			
		

def custom_posted(request):
	if request.GET:
		commentid = request.GET.get('c')
		comment = Comment.objects.get(id = commentid)
		story = Story.objects.get(id = comment.object_pk)
		user = User.objects.get(id = story.user_id)
		profile = User_Info.objects.get(user_id = comment.user_id)
		#If another person that is not the author comment, notify the author.
		if not (user.id == comment.user_id):
			#Notify the story author that the user has commented.
			stream_user(user.id,str(comment.user_id) + ':has commented on your story:' + str(story.storyid))
			#Notify the follower of the user that the user has commented on this story
			stream_readers(request.user.id, str(comment.user_id) + ':has commented on a story:' + str(story.storyid))
		#Increase the comment count
		count = story.commentcount
		story.commentcount = count + 1
		story.save()
		#Get time
		time = timesince(comment.submit_date).split(', ')[0]
		import json
		data = {}
		div = "<div class = \"col-lg-10\"><div class = \"col-lg-1\" style = \"padding-left:0px; padding-right:0px; \">"
		try:
			image = profile.profile_pic.image
			im = get_thumbnail(image, '330x330', crop='center', quality=99)
			div = div + "<img class =\"img-circle img-responsive user-pic\" style=\"height:60px; width: 60px;\"  src = \"" + im.url + "\" /></div>"
		except:
			div = div + "<img class = \"img-circle img-responsive user-pic\" style=\"height:60px;  width: 60px; \"  src = \"/media/media/default/DefaultIconBlack_1.png\" /></div>"
		div = div + "<div class = \"col-lg-10\"><h4><a href = \"/profile?u=" + str(request.user.username) + "\">" + str(request.user.username) + "</a> " + " " + str(comment.comment) + "<h6>" + time + " ago</h6></h4></div></div><div class = \"col-lg-10\"><hr></div>"
		
		data['string'] = div
		return HttpResponse(json.dumps(data), content_type = "application/json")
			
	
def custom_login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/following/")
	else:
		return login(request)
		
# Create your views here.
def create_stories(request):
	if request.user.is_authenticated():
		if request.POST:
			current_user = request.user
			list_form = []
			#Get the story form
			storyform = StoryForm(request.POST,prefix = "Story")
			#Check if text and image exists
			if not (request.POST.getlist('text') and request.FILES.getlist('source')):
				from django.contrib import messages
				messages.add_message(request, messages.WARNING, 'Please insert at least 1 text and 1 image')
				return render_page(request,"create_stories.html","custom error")
				
			#Handle insertion for the title.
			if storyform.is_valid():
				story = storyform.save(commit = False)
				story.user_id = current_user.id
				story.save()
				#Handle insertion of the text
				for f,p in zip(request.POST.getlist('text'),request.POST.getlist('text_position')):
					text = TextForm(request.POST,{'position' : p,'text': f })
					if text.is_valid():
						addtext = text.save(commit = False)
						addtext.storyid_id = story.id
						addtext.user = current_user
						addtext.position = p
						addtext.text = f
						list_form.append(addtext);
					else:
						return render_page(request,"create_stories.html",{'form': text})


				#Handle insertion of the image
				for f,p in zip(request.FILES.getlist('source'),request.POST.getlist('position')):
					if f.size > 5000000:
						from django.contrib import messages
						messages.add_message(request, messages.WARNING, 'Image size should not be more than 5MB.')
						return render_page(request,"create_stories.html","custom error")
					form = ImageForm(request.POST, {'source': f })
					if form.is_valid():
						addimage = form.save(commit = False)
						addimage.storyid_id = story.id
						addimage.user = current_user
						addimage.position = p
						list_form.append(addimage);
					else:
						return render_page(request,"create_stories.html",{'form': form})
				#All form has been validated. Save it permanently
				for item_form in list_form:
					item_form.save()
				#Change the story complete to true so user can see it.
				story.complete = True;
				story.save();
				#Stream to all users who follows.				
				stream_feed(request.user.id,str(request.user.id) + ':' + str(story.storyid))
				
				return HttpRespondeRedirect('/complete')
			else:
				return render_page(request,"create_stories.html",{'form': storyform})
		else:
			return render_page(request,"create_stories.html","no error")
	else:
		return HttpRespondeRedirect("home.html")
		
#Render page. This is for create_stories
def render_page(request,html,form):
	#Create all the form required for the page
	imageform = ImageForm()
	textform = TextForm()
	storyform = StoryForm(prefix = "Story")
	profile = User_Info.objects.get(user_id = request.user.id)
	count = get_notification_count(request)
	notification = get_notification(request)
	args = {}
	#Add csrf security
	args.update(csrf(request))
	args['textform'] = textform
	args['imageform'] = imageform
	args['storyform'] = storyform
	args['profile'] = profile 
	args['notification'] = notification
	args['count'] = count
	
	#if there is an error add it inside the args
	if isinstance(form, dict):
		args['form'] = form['form']
	#Render the page with the args.
	return render(request,html,args)
	

#Read a specific story given the url.
def read_stories(request):
	#Import library needed
	from uuid import UUID
	from operator import attrgetter
	from itertools import chain
	
	if request.GET:
		#Get the story id from url.
		r_id = request.GET.get('s')
		try:
			val = UUID(r_id, version=4)
		except ValueError:
			# If it's a value error, then the string 
			# is not a valid hex code for a UUID.
			return HttpRespondeRedirect("/home")
			
		#Fetch the data necessary from database
		story = Story.objects.get(storyid = r_id)
		image = Image.objects.filter(storyid = story.id)
		text = Text.objects.filter(storyid = story.id)
		profile = User_Info.objects.get(user_id = request.user.id)
		author = User_Info.objects.get(user_id = story.user_id)
		
				
		comment = get_comment(story.id)

		#Combine result for text and image. Sort according to position
		combine = sorted(
						chain(text,image),
						key=attrgetter('position'))
		count = get_notification_count(request)
		notification = get_notification(request)
		args = {}
		args.update(csrf(request))
		args['story'] = story
		args['items'] = combine
		args['author'] = author
		args['profile'] = profile
		args['notification'] = notification
		args['count'] = count
		args['comments'] = comment
		return render (request,"read_stories.html",args)
	else:
		return HttpRespondeRedirect("/home")
	
#Show story from people who you followed	
def feed(request):
	if request.user.is_authenticated():
		#Create profile for user the first time.
		user,created = User_Info.objects.get_or_create(username = request.user.username,user_id = request.user.id)
		#Get the data streams for the user
		import user_streams
		items = user_streams.get_stream_feed(request.user)
		imagelist = []
		storylist = []
		for item in items:
			#Split the string into the user id and story id
			object = item.content.split(":")
			story = Story.objects.get(storyid = object[1])
			user_info = User_Info.objects.get(user_id = story.user_id)
			image = {}
			storyimage = Image.objects.filter(storyid = story.id).first()
			image['story'] = storyimage.source
			image['time'] = timesince(story.datetime).split(', ')[0]
			try:
				image['user'] = user_info.profile_pic.image
			except:
				image['user'] = None

			imagelist.append(image)
			storylist.append(story)
		profile = User_Info.objects.get(user_id = request.user.id)
		list = zip(storylist,imagelist)
		notification = get_notification(request)
		count = get_notification_count(request)

		args = {}
		args['list'] = list
		args['profile'] = profile
		args['notification'] = notification
		args['count'] = count
		return render (request,"feed.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")

#Show story from people who you starred	
def bookmark(request):
	if request.user.is_authenticated():
		#Create profile for user the first time.
		stars = Star.objects.filter(user_id = request.user.id)
		
		imagelist = []
		storylist = []
		for item in stars:
			story = Story.objects.get(id = item.storyid_id)
			user_info = User_Info.objects.get(user_id = story.user_id)
			image = {}
			storyimage = Image.objects.filter(storyid = story.id).first()
			image['story'] = storyimage.source
			image['time'] = timesince(story.datetime).split(', ')[0]
			try:
				image['user'] = user_info.profile_pic.image
			except:
				image['user'] = None

			imagelist.append(image)
			storylist.append(story)
		profile = User_Info.objects.get(user_id = request.user.id)
		list = zip(storylist,imagelist)
		notification = get_notification(request)
		count = get_notification_count(request)

		args = {}
		args['list'] = list
		args['profile'] = profile
		args['notification'] = notification
		args['count'] = count
		return render (request,"bookmark.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")
		

#Show what people you followed are doing
def following(request):
	if request.user.is_authenticated():
		#Get the data streams for the user
		import user_streams
		items = user_streams.get_stream_following(request.user)
		personlist = []
		storylist = []
		for item in items:
			#Split the string into the user id and story id
			object = item.content.split(":")
			#Get the first user.
			user1 = User.objects.get(id = object[0])
			hash = {}
			hash['user1'] = user1.username
			user_info_1 = User_Info.objects.get(user_id = user1.id)

			#Try to get the story object if it is a story
			try:
				story = Story.objects.get(storyid = object[2])
				user_info_2 = User_Info.objects.get(user_id = story.user_id)
				storyimage = Image.objects.filter(storyid = story.id).first()
				hash['story'] = storyimage.source
				
			#If fail then it is a follow/star
			except:
				story = None
				user2 = User.objects.get(id = object[2])
				hash['user2'] = user2.username
			hash['time'] = timesince(item.created_at).split(', ')[0]
			hash['content'] = object[1]
			try:
				hash['user_image'] = user_info_1.profile_pic.image
			except:
				hash['user_image'] = None

			personlist.append(hash)
			storylist.append(story)
		profile = User_Info.objects.get(user_id = request.user.id)
		list = zip(storylist,personlist)
		notification = get_notification(request)
		count = get_notification_count(request)

		args = {}
		args['list'] = list
		args['profile'] = profile
		args['notification'] = notification
		args['count'] = count
		return render (request,"following.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")


#Show notifaction 
def notification(request):
	if request.user.is_authenticated():
		list = get_notification(request)
		#Get more than 5 notification since this is the notification page
		mainnotification = get_notification(request,1,10)
		count = get_notification_count(request)
		profile = User_Info.objects.get(user_id = request.user.id)
		args = {}
		args.update(csrf(request))
		args['notification'] = list
		args['mainnotification'] = mainnotification
		args['profile'] = profile
		args['count'] = count
		return render (request,"notification.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def load_comment(request):
	if request.POST:
		start = request.POST.get('number')
		id = request.POST.get('id')
		story = Story.objects.get(storyid=id)
		comments = get_comment(story.id,int(start))
		divcom = []
		for comment in comments:
			div = "<div class = \"col-lg-10\"><div class = \"col-lg-1\" style = \"padding-left:0px; padding-right:0px; \">"
			try:
				image = comment['image']
				im = get_thumbnail(image, '330x330', crop='center', quality=99)
				div = div + "<img class =\"img-circle img-responsive user-pic\" style=\"height:60px; width: 60px;\"  src = \"" + im.url + "\" /></div>"
			except:
				div = div + "<img class = \"img-circle img-responsive user-pic\" style=\"height:60px;  width: 60px; \"  src = \"/media/media/default/DefaultIconBlack_1.png\" /></div>"
		
			div = div + "<div class = \"col-lg-10\"><h4><a href = \"/profile?u=" + str(comment['username']) + "\">" + str(comment['username']) + "</a> " + " " + str(comment['comment']) + "<h6>" + comment['time'] + " ago</h6></h4></div></div><div class = \"col-lg-10\"><hr></div>"
			divcom.append(div)
		import json
		data = {}
		data['string'] = divcom
		return HttpResponse(json.dumps(data), content_type = "application/json")

#Get the latest comment
def get_comment(id,start=1,multiple = 5):
	end = start * multiple
	start = end - multiple
	comments = Comment.objects.filter(object_pk = id).order_by('-id')[start:end]
	list = []
	for comment in comments:
		user = User.objects.get(id = comment.user_id)
		profile = User_Info.objects.get(user_id = comment.user_id)
		item = {}
		try:
			item['image'] = profile.profile_pic.image
		except:
			image = None
			item['image'] = image
			
		item['comment'] = comment.comment
		item['username'] = user.username
		item['time'] = timesince(comment.submit_date).split(', ')[0]
		list.append(item)
	list.reverse()
	return list

#Update last seen
def update_seen(request):
	from last_seen.models import LastSeen
	from django.utils import timezone
	seen = LastSeen.objects.get(user=request.user)
	seen.last_seen = timezone.now()
	seen.save()
	import json
	data = {}
	data['string'] = "True"
	return HttpResponse(json.dumps(data), content_type = "application/json")
	

#Function to retrieve the notification list
def get_notification_count(request):
	#Get user last seen
	from last_seen.models import LastSeen
	seen = LastSeen.objects.when(user=request.user)
	#Get the data streams for the user
	import user_streams
	count = user_streams.get_stream_items(request.user).filter(created_at__gte = seen).count()
	return count

def load_notification(request):	
	if request.POST:
		start = request.POST.get('number')
		list = get_notification(request,int(start))
		divnoti = ""
		for notification in list:
			div = "<div class = \"col-lg-8 col-lg-push-2\" style =\"margin-top:20px;\"><div class =\"row\"><div class = \"col-lg-1\" style = \"padding-left:0px; padding-right:0px; \">"		
			try:
				image = notification['image']
				im = get_thumbnail(image, '330x330', crop='center', quality=99)
				div = div + "<img class =\"img-circle img-responsive user-pic\" style=\"height:50px; width: 50px;\"  src = \"" + im.url + "\" /></div>"
			except:
				div = div + "<img class = \"img-circle img-responsive user-pic\" style=\"height:50px;  width: 50px; \"  src = \"/media/media/default/DefaultIconBlack_1.png\" /></div>"
			
			try:
				div = div + "<h4>" + "<a href=\"/profile?u=" + str(notification['username']) + "\">" + str(notification['username']) + "</a>" + "<a href = \"/stories/read/?s=" + str(notification['story']) + "\">" + " " + str(notification['topic']) + "</a></h4>"
			except :
				div = div  + "<h4>" + "<a href=\"/profile?u=" + str(notification['username']) + "\"> " +  str(notification['username']) + "</a> " + str(notification['topic']) + "</h4>"

			div = div + "<h6>" + notification['time'] + " ago</h6><hr></div></div>"
			divnoti = divnoti + div
		import json
		data = {}
		data['string'] = divnoti
		return HttpResponse(json.dumps(data), content_type = "application/json")
#Function to retrieve the notification list
def get_notification(request,start=1,multiple = 5):	
	end = start * multiple
	start = end - multiple
	#Get the data streams for the user
	import user_streams
	items = user_streams.get_stream_items(request.user)[start:end]
	list = []
	for item in items:
		#Split the string for info about the user.
		object = item.content.split(":")
		#Get the username from the id
		username = User.objects.get(id=object[0])
		profile = User_Info.objects.get(user_id = object[0])
		data = {}
		try:
			data['image'] = profile.profile_pic.image
		except:
			image = None
			data['image'] = image
			
		data['username'] = username
		data['topic'] = object[1]
		data['time'] = timesince(item.created_at).split(', ')[0]
		if len(object) == 3:
			story = Story.objects.get(storyid = object[2])
			image = Image.objects.filter(storyid = story.id).first()
			data['story_image'] = image.source
			data['story'] = object[2]
		list.append(data)
	return list

		
#User edit
def user_edit(request):
	if request.user.is_authenticated():
		if request.POST:
			user_info = EditForm(request.POST)
			if user_info.is_valid():
				if not (User.objects.filter(username = user_info.cleaned_data['username']).exists()):
					auth_user = User.objects.get(id = request.user.id)
					user = User_Info.objects.get(user_id = request.user.id)
					#Change data at user info table
					user.username = user_info.cleaned_data['username']
					user.desc = user_info.cleaned_data['desc']
					#Change data at auth_user table
					auth_user.username = user_info.cleaned_data['username']
					#Save both to database
					auth_user.save()
					user.save()
					return render_page(request,"user_edit.html",{'form': user_info})
				else:
					#Return user already exists error
					return render_page(request,"error.html",{'form': user_info})
			else:
				return render_page(request,"user_edit.html",{'form': user_info})
		
		
		profile = User_Info.objects.get(user_id = request.user.id)
		list = get_notification(request)
		count = get_notification_count(request)
		form = EditForm()
		args = {}
		args['form'] = form
		args['profile'] = profile
		args['count'] = count
		args['notification'] = notification
		return render (request,"user_edit.html",args)

#User Image edit
def image_edit(request):
	if request.user.is_authenticated():
		if request.POST:
			image_info = EditFormImage(request.POST, request.FILES)
			if image_info.is_valid():
				image = image_info.save(commit = False)
				image.user_id = request.user.id
				#Create the image
				image.save()
				#Edit the user to point to the newly created image
				user = User_Info.objects.get(user_id = request.user.id)
				user.profile_pic = image
				user.save()
				return render_page(request,"image_edit.html",{'form': image_info})
			else:
				print image_info
				return render_page(request,"image_edit.html",{'form': image_info})
		
		
		profile = User_Info.objects.get(user_id = request.user.id)
		list = get_notification(request)
		count = get_notification_count(request)
		form = EditFormImage()
		args = {}
		args['form'] = form
		args['profile'] = profile
		args['count'] = count
		args['notification'] = notification
		return render (request,"image_edit.html",args)
				

#Show the user profile given the url
def user_profile(request):
	if request.user.is_authenticated():
		if request.GET:
			name = request.GET.get('u')
			#Get the person from the username
			person = User.objects.get(username=name)
			#Count number of story
			stories = Story.objects.filter(user_id = person.id)
			storycount = stories.count()
			#Get the first image of the story
			imagelist = []
			for story in stories:
				#Get the first image of every story and append to image list.
				image = Image.objects.filter(storyid = story.id).first()
				imagelist.append(image)
				
			list = zip(stories,imagelist)
			#Get the person object from the username
			profileuser, profilecreated = Person.objects.get_or_create(name_id = person.id,id = person.id)
			#Get the user following and follower
			followers = profileuser.get_followers()
			followingcount = profileuser.get_following().count()
			followercount = profileuser.get_followers().count()

			#Determine whether the user is looking at his/her own profile
			item = ""
			if person.id == request.user.id :
				item = "User"
			else:
				try:
					followers.get(name = request.user.id)
					item = "Unfollow"
				except :
					item = "Follow"
			
			notification = get_notification(request)
			count = get_notification_count(request)
			args = {}
			args.update(csrf(request))
			profile = User_Info.objects.get(user_id = request.user.id)
			args['storycount'] = storycount
			args['list'] = list
			args['followingcount'] = followingcount
			args['followerscount'] = followercount
			args['profile'] = profile
			args['person'] = person
			args['user'] = request.user
			args['item'] = item
			args['count'] = count
			args['notification'] = notification
		return render (request,"user_profile.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")
		
#Handle unfollow request	
def unfollow(request):
	if request.POST:
		#Get the username for the user and the person he/she want to unfollow
		person = User.objects.get(username=request.POST.get("username"))
		user = request.user
		#Get the person object for both of the person
		profileuser,profilecreated = Person.objects.get_or_create(id = person.id,name_id = person.id)
		user,usercreated = Person.objects.get_or_create(id = user.id,name_id = user.id)
		#Remove their relationship
		user.remove_relationship(profileuser,RELATIONSHIP_FOLLOWING)
		import json
		data = {}
		data['string'] = '<button type="button" class="btn btn-success item" id = "follow" value = "' + person.username + '">Follow</button>'
		return HttpResponse(json.dumps(data), content_type = "application/json")
		
#Handle unfollow request	
def follow(request):
	if request.POST:
		#Get the username for the user and the person he/she want to unfollow
		person = User.objects.get(username=request.POST.get("username"))
		user = request.user
		#Get the person object for both of the person
		profileuser,profilecreated   = Person.objects.get_or_create(id = person.id,name_id = person.id)
		user,usercreated = Person.objects.get_or_create(id = user.id,name_id = user.id)
		#Add their relationship
		user.add_relationship(profileuser,RELATIONSHIP_FOLLOWING)
		#Notify the person that the user has followed him
		stream_user(person.id,str(request.user.id) + ':has become your reader')
		#Notify user followers that the user has folllowed this person
		stream_readers(request.user.id,str(request.user.id) + ":has become a reader of:" + str(person.id))
		#Reply to ajax
		import json
		data = {}
		data['string'] = '<button type="button" class="btn btn-success item" id = "unfollow" value = "' + person.username +' ">Unfollow</button>'
		return HttpResponse(json.dumps(data), content_type = "application/json")

