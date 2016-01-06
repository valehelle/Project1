from django.shortcuts import render
from forms import TextForm,ImageForm,StoryForm,EditFormImage,AlbumForm
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
from django.contrib.staticfiles.templatetags.staticfiles import static


def about(request):
	args = []
	return render(request,'about.html',args)
	
def privacy(request):
	args = []
	return render(request,'privacy.html',args)

def terms(request):
	args = []
	return render(request,'terms.html',args)

def acceptable(request):
	args = []
	return render(request,'acceptable.html',args)

def support(request):
	args = []
	return render(request,'support.html',args)
	
def stream_readers(id,string):
	#Stream to all users who follows.
	user,created = Person.objects.get_or_create(name_id = id,id = id)
	followers = user.get_followers()
	import user_streams
	user_streams.add_stream_following(followers, string)
	return True

def register_closed(request):
	args = {}
	args.update(csrf(request))
	return render(request,'registration_closed.html',args)	
	
	
def feedback(request):
	from django.core.mail import send_mail
	from django.contrib import messages
	from django.core.exceptions import ValidationError
	from django.core.validators import validate_email

	if request.POST:
		feedback = request.POST.get('feedback')	
		
		send_mail("Feedback:" + request.user.email,request.user.username + ":" + feedback, 'mementhoactivate@google.com',['hazmiirfan92@gmail.com'], fail_silently=False)

		div = "<h4 id = \"server-feedback\">Thank Your for the feedback! :D</h4>"
		data = {}
		data['string'] = div
		import json
		return HttpResponse(json.dumps(data), content_type = "application/json")		

	
def request_access(request):
	from django.core.mail import send_mail
	from django.contrib import messages
	from django.core.exceptions import ValidationError
	from django.core.validators import validate_email

	if request.POST:
		email = request.POST.get('email')
		if not email:
			messages.add_message(request, messages.SUCCESS, 'Please insert your email')
			args = {}
			args.update(csrf(request))
			return render(request,'login.html',args)	
		username = request.POST.get('username')
		if not username:
			messages.add_message(request, messages.SUCCESS, 'Please insert your username')
			args = {}
			args.update(csrf(request))
			return render(request,'login.html',args)
		try:
			validate_email(email)
		except ValidationError as e:
			messages.add_message(request, messages.SUCCESS, 'Please enter a valid email address')
		else:			
			send_mail('Mementho Registration', username + " : " + email, 'mementhoactivate@google.com',['hazmiirfan92@gmail.com','bakhtiarateyz@gmail.com','syahmi2555@gmail.com'], fail_silently=False)
			send_mail('Mementho', 'Thank You ' + username + ' for subscribing to Mementho. We hope that in the long run we can provide you with a platform for great communities. It will usually take up to 1 day to create an account. Thank You for your patience', 'mementhoactivate@google.com',[email], fail_silently=False)
			messages.add_message(request, messages.SUCCESS, 'Thank You for joining to our community!. Please check your email and we will create an account for you as soon as possible!')
			args = {}
			args.update(csrf(request))
			return render(request,'login.html',args)	
	args = {}
	args.update(csrf(request))
	return render(request,'login.html',args)

def delete_stories(request):
	if request.user.is_authenticated():
		if request.POST:
			id = request.POST.get('id')
			story = Story.objects.get(storyid = id)
			#Check if it is really the user of the story who requested it
			if (story.user_id == request.user.id):
				story.delete = True
				story.save()
				import json
				data = {}
				data['string'] = "<h4 id = \"server-feedback\">Your story have been deleted. Please refresh the page.</h4>"
				return HttpResponse(json.dumps(data), content_type = "application/json")				
			else:
				return False
		else:
			return False
	return False
	
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
	if request.user.is_authenticated():
		if request.POST:
			#Get the story ID
			id = request.POST.get("storyid")
			#Fetch the story
			story = Story.objects.get(storyid = id)
			#Author of the story cannot star his/her own story
			if not (story.user_id == request.user.id):
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

			
			div = "<span id = \"starcount\"> " + str(story.starcount) + "</span>"
			import json
			data = {}
			data['string'] = div
			return HttpResponse(json.dumps(data), content_type = "application/json")			
	else:
		return False

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
		div = "<div data-id = \"" + str(comment.id) + "\" class = \"comment-item col-xs-12 col-sm-12 col-md-10 col-lg-10\">"
		div = div + "<div class = \"visible-md visible-lg col-md-1 col-lg-1\" style = \"padding-left:0px; padding-right:0px; \">"
		try:
			image = profile.profile_pic.image
			im = get_thumbnail(image, '330x330', crop='center', quality=99)
			div = div + "<img class =\"img-circle img-responsive user-pic\" src = \"" + str(im.url) + "\" /></div>"
		except:
			div = div + "<img class = \"img-circle img-responsive user-pic\"  src = \"" + static('image/default/DefaultIconBlack_1.png') + "\" /></div>"	
		div = div + "<div class = \"col-xs-12 col-sm-12 col-md-10 col-lg-10\">"
		div = div + "<h4><a href = \"/profile?u=" + str(comment.user_name) + "\" class = \"text-green\">" + str(comment.user_name) + "</a> " + str(comment.comment) + "</h4><h6>" + time + " ago</h6>"
		div = div + "</div></div>"
		div = div + "<div class = \"col-xs-12 col-sm-12 col-md-10 col-lg-12\"><hr></div>"
		data['string'] = div
		return HttpResponse(json.dumps(data), content_type = "application/json")
			
	
def custom_login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/feed/")
	else:
		return login(request)
		
# Create your views here.
def album_finish(request):
	if request.user.is_authenticated:
		if request.POST:
			storyid = request.POST.get('story-id')
			story = Story.objects.get(id = storyid)
			story.complete = True
			story.type = 1
			story.save()
			#Stream to all users who follows.				
			stream_feed(request.user.id,str(request.user.id) + ':' + str(story.storyid))
			data = {}
			data['result'] = "/stories/read/?s=" + str(story.storyid)
			import json
			return HttpResponse(json.dumps(data), content_type = "application/json")
		else:
			return False;
	else:
			return False;
	
# Create your views here.
def store_image(request):
	if request.user.is_authenticated():
		if request.POST:
			image = AlbumForm(request.POST, request.FILES)
			if image.is_valid():
				imageform = image.save(commit = False)
				imageform.user_id = request.user.id
				imageform.save()
				import json
				data = {}
				data['result'] = "Success"
				print request.POST
				return HttpResponse(json.dumps(data), content_type = "application/json")
			else:
				print "image is invalid"
				print request.POST
				return False
		else:
			print "request is not a POST"
			return False

	else:
	
		print("user not authenticated") 
		return False
		
def store_album(request):
	if request.user.is_authenticated():
		if request.POST:
			storyform = StoryForm(request.POST,prefix = "Story")
			if storyform.is_valid():
				story = storyform.save(commit = False)
				story.user_id = request.user.id
				story.save()
				import json
				data = {}
				data['id'] = str(story.id)
			return HttpResponse(json.dumps(data), content_type = "application/json")
		else:
			return False
	else:
		return False
		
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
				print "error image"
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
					if f.size > 10000000:
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
				
				return HttpResponseRedirect("/stories/read/?s=" + str(story.storyid))
			else:
				print "not valid"
				return render_page(request,"create_stories.html",{'form': storyform})
		else:
			return render_page(request,"create_stories.html","no error")
	else:
		return HttpRespondeRedirect("home.html")

# Create your views here.
def create_album(request):
	if request.user.is_authenticated():
		args = {}
		args.update(csrf(request))
		return render (request,"create_album.html",args)
	else:
		return HttpRespondeRedirect("/")

#Render page. This is for create_stories
def render_page(request,html,form):
	#Create all the form required for the page
	imageform = ImageForm()
	textform = TextForm()
	storyform = StoryForm(prefix = "Story")
	profile = User_Info.objects.get(user_id = request.user.id)
	count = get_notification_count(request)
	notification = get_notification_latest(request)
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
		args = {}
		try:
			val = UUID(r_id, version=4)
		except ValueError:
			# If it's a value error, then the string 
			# is not a valid hex code for a UUID.
			return HttpResponseRedirect("/feed/")
		
		try:					
			#Fetch the data necessary from database
			story = Story.objects.get(storyid = r_id,delete = False)
			
			image = Image.objects.filter(storyid = story.id)
			image = sorted(image,key=attrgetter('position'))
			text = Text.objects.filter(storyid = story.id)
			banner = image.pop(0)
			banner = banner.source
			if request.user.is_authenticated():
				profile = User_Info.objects.get(user_id = request.user.id)
				count = get_notification_count(request)
				notification = get_notification_latest(request)
				args.update(csrf(request))
			else:
				profile = None
				count = None
				notification = None
			
			author = User_Info.objects.get(user_id = story.user_id)		
			comment = get_comment_latest(story.id)
			combine = sorted(
							chain(text,image),
							key=attrgetter('position'))

			
			args['story'] = story
			args['banner'] = banner
			args['items'] = combine
			args['author'] = author
			args['profile'] = profile
			args['notification'] = notification
			args['count'] = count
			args['comments'] = comment
			args['metaimage'] = image
		except:
			return HttpResponseRedirect("/feed/")
		if story.type == 0:
			return render (request,"read_stories.html",args)
		else:
			return render (request,"read_album.html",args)
	else:
		return HttpResponseRedirect("/feed/")

#Get featured author. For now only show those who recently joined.
def featured_author():
	users = User.objects.filter().order_by('-id')[:5]
	featured = []
	for user in users:
		user_info = User_Info.objects.get(user_id = user.id)
		list = {}
		try:
			list['image'] = user_info.profile_pic.image
		except:
			list['image'] = None
		list['username'] = user.username
		list['desc'] = user_info.desc
		featured.append(list)
	return featured
		
	
#Show story from people who you followed	
def feed(request):
	
	if request.user.is_authenticated():
		#Create profile for user the first time.
		user,created = User_Info.objects.get_or_create(username = request.user.username,user_id = request.user.id)
		#Get the data streams for the user
		items = get_feed_latest(request.user)
		imagelist = []
		storylist = []
		for item in items:
			#Split the string into the user id and story id
			object = item.content.split(":")
			try:
				story = Story.objects.get(storyid = object[1],delete = False)
				user_info = User_Info.objects.get(user_id = story.user_id)
				image = {}
				storyimage = Image.objects.filter(storyid = story.id).first()
				image['story'] = storyimage.source
				image['time'] = timesince(story.datetime).split(', ')[0]
				image['id'] = item.id
				try:
					image['user'] = user_info.profile_pic.image
				except:
					image['user'] = None

				imagelist.append(image)
				storylist.append(story)
			except:
				object = None
		profile = User_Info.objects.get(user_id = request.user.id)
		list = zip(storylist,imagelist)
		notification = get_notification_latest(request)
		count = get_notification_count(request)
		f_author = featured_author()
		args = {}
		args.update(csrf(request))
		args['list'] = list
		args['profile'] = profile
		args['notification'] = notification
		args['count'] = count
		args['featured'] = f_author
		return render (request,"feed.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")


	
#Get previous feed
def feed_previous(request):
	if request.user.is_authenticated():
		if request.POST:
			max_id = request.POST.get('max-id')
			max_id = int(max_id)
			list = get_feed_previous(request.user,max_id)	
			string = html_feed(list)
			import json
			data = {}
			data['string'] = string
			return HttpResponse(json.dumps(data), content_type = "application/json")

	
#Return feed previous
def get_feed_latest(user,max_id=0,count=10):
	import user_streams
	list = user_streams.get_stream_feed(user).filter(id__gt = max_id)[:count]
	return list
	
#Return feed latest
def get_feed_previous(user,max_id=0,count=10):
	import user_streams
	list = user_streams.get_stream_feed(user).filter(id__lt = max_id)[:count]
	return list
	
#Given a list, return a string of html
def html_feed(list):
	storylist = []

	for item in list:
		string = ""
		#Split the string into the user id and story id
		object = item.content.split(":")
		try:
			story = Story.objects.get(storyid = object[1],delete = False)
			user_info = User_Info.objects.get(user_id = story.user_id)
			image = {}
			storyimage = Image.objects.filter(storyid = story.id).first()
			im = get_thumbnail(storyimage.source, '500x500', crop='center', quality=99)
			time = timesince(story.datetime).split(', ')[0]

			string = "<div data-id = \" " + str(item.id) + " \" class = \"story-item col-md-6 col-lg-6\" style =\"padding:3px; background-color:#DCE0D5\">"
			string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12 card\" style = \"padding:0; margin-bottom:0px;\">"
			string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\" style = \"padding:0;\">"
			string = string + "<a class = \"story\" href = \"/stories/read/?s=" + str(story.storyid) + "\" >"
			string = string + "<img class = \"img-responsive\"  src=\"" + str(im.url) +"\" style = \"text-align:center;\" width = \"" + str(im.width) + "\"  height = \"" + str(im.height) + "\"></a></div>"
			string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\" >"
			string = string + "<h3 class = \"visible-lg visible-md\" style = \"text-align: center\">" + str(story.title) + "</h3>"
			string = string + "<h4 class = \"visible-xs visible-sm col-xs-12 col-sm-12\" style = \"text-align: center\">" + str(story.title) + "</h4></div>"
			string = string + "<div  class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\"  style=\"margin-bottom:20px;\">"
			string = string + "<div class = \"col-lg-12\" style=\"margin-bottom:10px;\">"
			string = string + "<div class = \" col-xs-4 col-xs-push-4 col-sm-4 col-sm-push-4 col-md-8 col-md-push-2 col-lg-8 col-lg-push-2\" style=\"margin-bottom:10px;\">"

			try:
				#Try to get user profile
				story_user = user_info.profile_pic.image
				user_im =  get_thumbnail(story_user, '330x330', crop='center', quality=99)
				string = string + "<img class = \"img-circle img-responsive user-pic\"  src = \"" + str(user_im.url) + "\"/> </div> </div>"
			except:
				string = string + "<img class = \"img-circle img-responsive user-pic\"  src = \""  + static('image/default/DefaultIconBlack_1.png') + "\"/> </div></div>"
					
			string = string + "<div  class = \"story-profile col-md-12 col-lg-12 col-xs-12 col-sm-12\" style = \"text-align:center;\">"
			string = string + "<h4 class = \"dont-break-out\">by <a href = \"/profile?u=" + str(story.user.username) + "\">" +  str(story.user.username)  + "</a> </h4>"
			string = string + "<h5>" + time + " ago</h5> </div> </div>"
			string = string + "<div  class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\">"
			string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12 btn btn-success text-green no-effect-hover\" style=\"background-color:white; margin-bottom:2px;\">"
			string = string + "	" + str(story.commentcount) + " comments </div>"
			string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12 btn btn-success text-green no-effect-hover\" style=\"background-color:white; margin-bottom:15px;\">"
			string = string + "	" + str(story.starcount) + " stars </div> </div> </div></div>"		
			storylist.append(string)
		except:
			story = None

	return storylist
	
	
#Get the latest story from everyone
	
#Show story from people who you followed	
def discovery(request):
	if request.user.is_authenticated():
		#Create profile for user the first time.
		user,created = User_Info.objects.get_or_create(username = request.user.username,user_id = request.user.id)
		#Get the data streams for the user
		items = get_discovery_latest(request.user)
		imagelist = []
		storylist = []
		for item in items:
			#Split the string into the user id and story id
			object = item['content'].split(":")
			story = Story.objects.get(storyid = object[1])
			user_info = User_Info.objects.get(user_id = story.user_id)
			image = {}
			storyimage = Image.objects.filter(storyid = story.id).first()
			image['story'] = storyimage.source
			image['time'] = timesince(story.datetime).split(', ')[0]
			#This is for ordering of the list when fetching
			image['id'] = item['id']
			try:
				image['user'] = user_info.profile_pic.image
			except:
				image['user'] = None

			imagelist.append(image)
			storylist.append(story)
		profile = User_Info.objects.get(user_id = request.user.id)
		list = zip(storylist,imagelist)
		notification = get_notification_latest(request)
		count = get_notification_count(request)
		f_author = featured_author()
		args = {}
		args.update(csrf(request))
		args['list'] = list
		args['profile'] = profile
		args['notification'] = notification
		args['count'] = count
		args['featured'] = f_author
		return render (request,"discovery.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")

#Get previous feed
def discovery_previous(request):
	if request.user.is_authenticated():
		if request.POST:
			max_id = request.POST.get('max-id')
			max_id = int(max_id)
			list = get_discovery_previous(request.user,max_id)	
			string = html_discovery(list)
			import json
			data = {}
			data['string'] = string
			
			return HttpResponse(json.dumps(data), content_type = "application/json")

	
#Return feed previous
def get_discovery_latest(user,max_id=0,count=10):
	list = []
	
	stories = Story.objects.filter(delete = False).order_by('-id')[:count]
	for story in stories:
		id = story.id
		hex = story.storyid
		storylist = {}
		string = str(id) + ":" + str(hex)
		storylist['content'] = string
		storylist['id'] = id
		list.append(storylist)
	return list
	
#Return feed latest
def get_discovery_previous(user,max_id=0,count=10):
	import user_streams
	list = []
	
	stories = Story.objects.filter(id__lt = max_id,delete = False).order_by('-id')[:count]
	for story in stories:
		id = story.id
		hex = story.storyid
		storylist = {}
		string = str(id) + ":" + str(hex)
		storylist['content'] = string
		storylist['id'] = id
		list.append(storylist)

	return list
	
#Given a list, return a string of html
def html_discovery(list):
	storylist = []

	for item in list:
		string = ""
		#Split the string into the user id and story id
		object = item['content'].split(":")
		story = Story.objects.get(storyid = object[1])
		user_info = User_Info.objects.get(user_id = story.user_id)
		image = {}
		storyimage = Image.objects.filter(storyid = story.id).first()
		im = get_thumbnail(storyimage.source, '500x500', crop='center', quality=99)
		time = timesince(story.datetime).split(', ')[0]

		string = "<div data-id = \" " + str(item['id']) + " \" class = \"story-item col-md-6 col-lg-6\" style =\"padding:3px; background-color:#DCE0D5\">"
		string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12 card\" style = \"padding:0; margin-bottom:0px;\">"
		string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\" style = \"padding:0;\">"
		string = string + "<a class = \"story\" href = \"/stories/read/?s=" + str(story.storyid) + "\" >"
		string = string + "<img class = \"img-responsive\"  src=\"" + str(im.url) +"\" style = \"text-align:center;\" width = \"" + str(im.width) + "\"  height = \"" + str(im.height) + "\"></a></div>"
		string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\" >"
		string = string + "<h3 class = \"visible-lg visible-md\" style = \"text-align: center\">" + str(story.title) + "</h3>"
		string = string + "<h4 class = \"visible-xs visible-sm col-xs-12 col-sm-12\" style = \"text-align: center\">" + str(story.title) + "</h4></div>"
		string = string + "<div  class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\"  style=\"margin-bottom:20px;\">"
		string = string + "<div class = \"col-lg-12\" style=\"margin-bottom:10px;\">"
		string = string + "<div class = \"col-xs-4 col-xs-push-4 col-sm-4 col-sm-push-4 col-md-8 col-md-push-2 col-lg-8 col-lg-push-2\" style=\"margin-bottom:10px;\">"

		try:
			#Try to get user profile
			story_user = user_info.profile_pic.image
			user_im =  get_thumbnail(story_user, '330x330', crop='center', quality=99)
			string = string + "<img class = \"img-circle img-responsive user-pic\"  src = \"" + str(user_im.url) + "\"/> </div></div>"
		except:
			string = string + "<img class = \"img-circle img-responsive user-pic\"  src = \""  + static('image/default/DefaultIconBlack_1.png') + "\"/> </div></div>"
				
		string = string + "<div  class = \"dont-break-out col-md-12 col-lg-12 col-xs-12 col-sm-12\" style = \"text-align:center;\">"
		string = string + "<h4 class = \"dont-break-out\">by <a href = \"/profile?u=" + str(story.user.username) + "\">" +  str(story.user.username)  + "</a> </h4>"
		string = string + "<h4>" + time + " ago</h4> </div> </div>"
		string = string + "<div  class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\">"
		string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12 btn btn-success text-green no-effect-hover\" style=\"background-color:white; margin-bottom:2px;\">"
		string = string + "	" + str(story.commentcount) + " comments </div>"
		string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12 btn btn-success text-green no-effect-hover\" style=\"background-color:white; margin-bottom:15px;\">"
		string = string + "	" + str(story.starcount) + " stars </div> </div> </div></div>"		
		storylist.append(string)

	return storylist
	

#Show story from people who you starred	
def bookmark(request):
	if request.user.is_authenticated():
		#Create profile for user the first time.
		stars = get_star_latest(request.user)
		
		imagelist = []
		storylist = []
		for item in stars:
			story = Story.objects.get(id = item.storyid_id)
			user_info = User_Info.objects.get(user_id = story.user_id)
			image = {}
			storyimage = Image.objects.filter(storyid = story.id).first()
			image['story'] = storyimage.source
			image['time'] = timesince(story.datetime).split(', ')[0]
			image['id'] = item.id
			try:
				image['user'] = user_info.profile_pic.image
			except:
				image['user'] = None

			imagelist.append(image)
			storylist.append(story)
		profile = User_Info.objects.get(user_id = request.user.id)
		list = zip(storylist,imagelist)
		notification = get_notification_latest(request)
		count = get_notification_count(request)

		args = {}
		args['list'] = list
		args['profile'] = profile
		args['notification'] = notification
		args['count'] = count
		return render (request,"bookmark.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")
		
def get_star_previous(user,max_id=0,count=10):
	stars = Star.objects.filter(user_id = user.id, id__lt = max_id).order_by('-id')[:count]
	return stars
def get_star_latest(user,max_id=0,count=10):
	stars = Star.objects.filter(user_id = user.id,id__gt = max_id).order_by('-id')[:count]
	return stars	

#Get bookmark feed
def bookmark_previous(request):
	if request.user.is_authenticated():
		if request.POST:
			max_id = request.POST.get('max-id')
			max_id = int(max_id)
			list = get_star_previous(request.user,max_id)	
			string = html_bookmark(list)
			import json
			data = {}
			data['string'] = string
			return HttpResponse(json.dumps(data), content_type = "application/json")

#Given a list, return a string of html
def html_bookmark(list):
	storylist = []

	for item in list:
		string = ""
		#Split the string into the user id and story id
		story = Story.objects.get(id = item.storyid_id)
		user_info = User_Info.objects.get(user_id = story.user_id)
		storyimage = Image.objects.filter(storyid = story.id).first()
		im = get_thumbnail(storyimage.source, '500x500', crop='center', quality=99)
		time = timesince(story.datetime).split(', ')[0]

		string = "<div data-id = \"" + str(item.id) + "\" class = \"story-item col-md-12 col-lg-6 col-xs-12 col-sm-6\" style =\"margin-top:30px; margin-bottom:10px; \">"
		string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\" >"
		string = string + "<a class = \"story\" href = \"/stories/read/?s=" + str(story.id) + "\" >"
		string = string + "<img class = \"img-responsive img-rounded\"  src=\"" + str(im.url) +"\" style = \"text-align:center;\"></a></div>"
		string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\" style = \"height:80px;\">"
		string = string + "<h3 class = \"visible-lg visible-md\" style = \"text-align: center\">" + str(story.title) + "</h3>"
		string = string + "<h4 class = \"visible-xs visible-sm col-xs-12 col-sm-12\" style = \"text-align: center\">" + str(story.title) + "</h4></div>"
		string = string + "<div  class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\"  style=\"margin-bottom:20px;\">"
		string = string + "<div class = \"col-md-4 col-lg-4 visible-lg visible-md\" style=\"margin-bottom:10px;\">"

		try:
			#Try to get user profile
			story_user = user_info.profile_pic.image
			user_im =  get_thumbnail(story_user, '330x330', crop='center', quality=99)
			string = string + "<img class = \"img-circle img-responsive user-pic\"  src = \"" + str(user_im.url) + "\"/> </div>"
		except:
			string = string + "<img class = \"img-circle img-responsive user-pic\"  src = \""  + static('image/default/DefaultIconBlack_1.png') + "\"/> </div>"
				
		string = string + "<div  class = \"v-center story-profile col-md-6 col-lg-6 col-xs-12 col-sm-12\">"
		string = string + "<h4>by <a href = \"/profile?u=" + str(story.user.username) + "\">" +  str(story.user.username)  + "</a> </h4>"
		string = string + "<h4>" + time + " ago</h4> </div> </div>"
		string = string + "<div  class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\">"
		string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12 btn btn-success text-green no-effect-hover\" style=\"background-color:white; margin-bottom:2px;\">"
		string = string + "	" + str(story.commentcount) + " comments </div>"
		string = string + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12 btn btn-success text-green no-effect-hover\" style=\"background-color:white; margin-bottom:2px;\">"
		string = string + "	" + str(story.starcount) + " stars </div> </div> </div>"		
		storylist.append(string)

	return storylist

#Show what people you followed are doing
def following(request):
	if request.user.is_authenticated():
		items = following_latest(request.user)
		personlist = []
		storylist = []
		for item in items:
			#Split the string into the user id and story id
			object = item.content.split(":")
			#Get the first user.
			user1 = User.objects.get(id = object[0])
			hash = {}
			hash['user1'] = user1.username
			hash['time'] = timesince(item.created_at).split(', ')[0]
			hash['content'] = object[1]
			hash['id'] = item.id
			
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

			try:
				hash['user_image'] = user_info_1.profile_pic.image
			except:
				hash['user_image'] = None

			personlist.append(hash)
			storylist.append(story)
		profile = User_Info.objects.get(user_id = request.user.id)
		list = zip(storylist,personlist)
		notification = get_notification_latest(request)
		count = get_notification_count(request)

		args = {}
		args['list'] = list
		args['profile'] = profile
		args['notification'] = notification
		args['count'] = count
		return render (request,"following.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def load_following(request):
	if request.user.is_authenticated():
		if request.POST:
			max_id = request.POST.get('max-id')
			items = following_previous(request.user,max_id)
			string = html_following(items)
			import json
			data = {}
			data['string'] = string
			return HttpResponse(json.dumps(data), content_type = "application/json")
	else:
		return HttpResponseRedirect("/accounts/login/")

def html_following(items):
	div = ""
	for item in items:
		#Split the string into the user id and story id
		object = item.content.split(":")
		#Get the first user.
		user1 = User.objects.get(id = object[0])
		hash = {}
		hash['user1'] = user1.username
		time = timesince(item.created_at).split(', ')[0]
		hash['content'] = object[1]
		user_info_1 = User_Info.objects.get(user_id = user1.id)
		div = div + "<div data-item = \"" + str(item.id) + "\" class = \"following-item col-lg-12 col-md-12 col-xs-12 col-sm-12\">"
		div = div + "<div class = \"visible-md visible-lg visible-sm col-md-2 col-lg-2 col-sm-2\">"
		try:
			im =  get_thumbnail(user_info_1.profile_pic.image, '330x330', crop='center', quality=99)
			div = div + "<img class = \"img-circle img-responsive user-pic\" src = \"" + str(im.url) + "\"/></div>"
		except:
			div = div + "<img class = \"img-circle img-responsive user-pic\"  src = \""  + static('image/default/DefaultIconBlack_1.png') + "\" /> </div>"
			
		div = div + "<div class = \"col-xs-12 col-sm-8 col-md-8 col-lg-8 v-center\" >"
		div = div + "<h3 style = \"padding:0;\">"
		div = div + "<a href = \"/profile?u=" + str(user1.username) + "\" >" + str(user1.username) + "</a>"
		div = div + "<span> " + str(object[1]) + "&nbsp;</span>  "
		try:
			user2 = User.objects.get(id = object[2])
			div = div + "<a href = \"/profile?u=" + str(user2.username) + "\" >" + str(user2.username) + "</a></h3>"
			div = div + "<h6>" + time +  " ago</h6></div>"
		except:
			story = Story.objects.get(storyid = object[2])
			user_info_2 = User_Info.objects.get(user_id = story.user_id)
			storyimage = Image.objects.filter(storyid = story.id).first()
			im1 =  get_thumbnail(storyimage.source, '330x330', crop='center', quality=99)
			
			div = div + "<h6>" + time + " ago</h6></div>"
			div = div + "<div class = \"col-md-2 col-lg-2 col-xs-12 col-sm-2\">"
			div = div + "<a href = \"/stories/read/?s=" + str(story.storyid) + "\"><img class = \"img-rounded img-responsive\"   src = \"" + str(im1.url) + "\" /></a></div>"
		div = div + "<div class = \"col-md-12 col-lg-12 col-xs-12 col-sm-12\"><hr></div></div>"
	return div
		
def following_latest(user,max_id = 0, count = 10):
	#Get the data streams for the user
	import user_streams
	list = user_streams.get_stream_following(user).filter(id__gt = max_id)[:count]
	return list
	
def following_previous(user,max_id = 0, count = 10):
	#Get the data streams for the user
	import user_streams
	list = user_streams.get_stream_following(user).filter(id__lt = max_id)[:count]
	return list

#Show notifaction 
def notification(request):
	if request.user.is_authenticated():
		list = get_notification_latest(request)
		#Get more than 5 notification since this is the notification page
		mainnotification = get_notification_latest(request)
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
		max_id = request.POST.get('max-id')
		id = request.POST.get('id')
		story = Story.objects.get(storyid=id)
		comments = get_comment_previous(story.id,int(max_id))
		divcom = []
		for comment in comments:
			div = "<div data-id = \"" + str(comment['id']) +  "\" class = \"comment-item col-xs-12 col-sm-12 col-md-12 col-lg-12\"><div class = \"visible-md visible-lg col-md-1 col-lg-1\" style = \"padding-left:0px; padding-right:0px; \">"
			try:
				image = comment['image']
				im = get_thumbnail(image, '330x330', crop='center', quality=99)
				div = div + "<img class =\"img-circle img-responsive user-pic\"  src = \"" + im.url + "\" /></div>"
			except:
				div = div + "<img class = \"img-circle img-responsive user-pic\" src = \""  + static('image/default/DefaultIconBlack_1.png') + "\" /></div>"
		
			div = div + "<div class = \"col-xs-12 col-sm-12 col-md-10 col-lg-10\"><h4><a href = \"/profile?u=" + str(comment['username']) + "\" class = \"text-green\">" + str(comment['username']) + "</a> " + " " + str(comment['comment']) + "<h6>" + comment['time'] + " ago</h6></h4></div></div><div class = \"col-xs-12 col-sm-12 col-md-10 col-lg-12\"><hr></div>"
			divcom.append(div)
		import json
		data = {}
		data['string'] = divcom
		return HttpResponse(json.dumps(data), content_type = "application/json")

#Get the latest comment
def get_comment_latest(id,max_id=0,count=5):
	comments = Comment.objects.filter(object_pk = id,id__gt = max_id).order_by('-id')[:count]
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
		item['id'] = comment.id
		item['comment'] = comment.comment
		item['username'] = user.username
		item['time'] = timesince(comment.submit_date).split(', ')[0]
		list.append(item)
	list.reverse()
	return list

#Get the latest comment
def get_comment_previous(id,max_id=0,count=5):
	
	comments = Comment.objects.filter(object_pk = id,id__lt = max_id).order_by('-id')[:count]
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
		item['id'] = comment.id
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
		max_id = request.POST.get('max-id')
		list = get_notification_previous(request,int(max_id))
		divnoti = ""
		for notification in list:
			div = "<div data-id= \"" + str(notification['id']) + "\" class = \"notification-item col-sm-12 col-xs-12 col-md-12 col-lg-12 card\">"	
			try:
				image = notification['story_image']
				im = get_thumbnail(image, '330x330', crop='center', quality=99)
				div = div + "<div class = \"col-sm-8 col-xs-12 col-md-9 col-lg-9\">"
				div = div + "<h4><a href = \"/profile?u=" + str(notification['username']) + "\">" + str(notification['username']) + "</a> " + str(notification['topic']) +" <h6>" + notification['time'] + " ago</h6></h4></div>"
				div = div + "<div class = \"col-sm-4 col-xs-12  col-md-3 col-lg-2 col-lg-push-1\">"
				div = div + "<a href = \"/stories/read/?s=" + str(notification['story']) + "\"><img class = \"img-rounded img-responsive\"   src = \"" + str(im.url) + "\" /></a> </div>"
			except :
				div = div + "<div class = \"col-sm-12 col-xs-12  col-md-12 col-lg-12\">"
				div = div  + "<h4><a href = \"/profile?u=" + str(notification['username']) + "\">" + str(notification['username'])  + "</a> " + str(notification['topic']) + "<h6> " +  notification['time'] + " ago</h6></h4></div>"

			div = div + "</div>"
			divnoti = divnoti + div
		import json
		data = {}
		data['string'] = divnoti
		return HttpResponse(json.dumps(data), content_type = "application/json")
		
#Function to retrieve the notification list
def get_notification_latest(request,max_id=0,count = 5):	
	#Get the data streams for the user
	import user_streams
	items = user_streams.get_stream_items(request.user).filter(id__gt = max_id)[:count]
	list = []
	for item in items:
		#Split the string for info about the user.
		object = item.content.split(":")
		#Get the username from the id
		username = User.objects.get(id=object[0])
		profile = User_Info.objects.get(user_id = object[0])
		data = {}
		data['id'] = item.id
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

#Function to previous the notification list
def get_notification_previous(request,max_id=0,count = 5):	
	#Get the data streams for the user
	import user_streams
	items = user_streams.get_stream_items(request.user).filter(id__lt = max_id)[:count]
	list = []
	for item in items:
		#Split the string for info about the user.
		object = item.content.split(":")
		#Get the username from the id
		username = User.objects.get(id=object[0])
		profile = User_Info.objects.get(user_id = object[0])
		data = {}
		data['id'] = item.id
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
	
#Name edit
def name_edit(request):
	from forms import EditUsername
	from django.contrib import messages
	
	if request.user.is_authenticated():
		if request.POST:
			user_info = EditUsername(request.POST)
			if user_info.is_valid():
				if not (User.objects.filter(username = user_info.cleaned_data['username']).exists()):
					auth_user = User.objects.get(id = request.user.id)
					user = User_Info.objects.get(user_id = request.user.id)
					#Change data at user info table
					user.username = user_info.cleaned_data['username']
					#Change data at auth_user table
					auth_user.username = user_info.cleaned_data['username']
					#Save both to database
					auth_user.save()
					user.save()
					newuser = auth_user.username
					return HttpResponseRedirect("/profile?u=" + str(newuser))
				else:
					#Return user already exists error
					messages.add_message(request, messages.WARNING, 'Username already exists')
					return render_page(request,"username_edit.html",{'form': user_info})
			else:
				messages.add_message(request, messages.WARNING, 'Something went wrong. We cannot process your request right now')
				return render_page(request,"username_edit.html",{'form': user_info})
		
		
		profile = User_Info.objects.get(user_id = request.user.id)
		list = get_notification_latest(request)
		count = get_notification_count(request)
		form = EditUsername()
		args = {}
		
		args['form'] = form
		args['profile'] = profile
		args['count'] = count
		args['notification'] = list
		return render (request,"username_edit.html",args)
		
#Description edit
def desc_edit(request):
	from forms import EditDesc
	if request.user.is_authenticated():
		if request.POST:
			user_info = EditDesc(request.POST)
			if user_info.is_valid():
				user = User_Info.objects.get(user_id = request.user.id)
				#Change data at user info table
				user.desc = user_info.cleaned_data['desc']
				#Change data at auth_user table
				#Save both to database
				user.save()
				return HttpResponseRedirect("/profile?u=" + str(user.username))
				
			else:
				messages.add_message(request, messages.WARNING, 'Something went wrong. We cannot process your request right now')
				return render_page(request,"desc_edit.html",{'form': user_info})
		
		
		profile = User_Info.objects.get(user_id = request.user.id)
		list = get_notification_latest(request)
		count = get_notification_count(request)
		form = EditDesc()
		args = {}
		args.update(csrf(request))
		args['form'] = form
		args['profile'] = profile
		args['count'] = count
		args['notification'] = list
		return render (request,"desc_edit.html",args)

#Description edit
def user_edit(request):
	if request.user.is_authenticated():
		profile = User_Info.objects.get(user_id = request.user.id)
		list = get_notification_latest(request)
		count = get_notification_count(request)
		args = {}
		args['profile'] = profile
		args['count'] = count
		args['notification'] = list
		return render (request,"user_edit.html",args)
	else:
		return HttpResponseRedirect("/")
		
		

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
				return HttpResponseRedirect("/profile?u=" + str(user.username))
			else:
				return render_page(request,"image_edit.html",{'form': image_info})
		
		
		profile = User_Info.objects.get(user_id = request.user.id)
		list = get_notification_latest(request)
		count = get_notification_count(request)
		form = EditFormImage()
		args = {}
		args.update(csrf(request))
		args['form'] = form
		args['profile'] = profile
		args['count'] = count
		args['notification'] = list
		return render (request,"image_edit.html",args)
			
			
#Search user
def user_search(request):
	if request.user.is_authenticated():
		args = {}
		if request.GET:
			name = request.GET.get('u')
			notification = get_notification_latest(request)
			count = get_notification_count(request)
			args = {}
			args.update(csrf(request))
			args['username'] = name
			args['count'] = count
			args['notification'] = notification
			return render (request,"user_search.html",args)
		else:
			return render (request,"user_search.html",args)

#Show the user profile given the url
def user_profile(request):
	if request.user.is_authenticated():
		if request.GET:
			name = request.GET.get('u')
			try:
				#Get the person from the username
				person = User.objects.get(username=name,is_active = 1)
			except:
				return HttpResponseRedirect("/user_search/?u=" + str(name))
			
			#Count number of story
			stories = Story.objects.filter(user_id = person.id,complete = 1,delete = False).order_by('-id')
			
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
			
			notification = get_notification_latest(request)
			count = get_notification_count(request)
			args = {}
			args.update(csrf(request))
			#Get the profile of the user
			profile = User_Info.objects.get(user_id = request.user.id)
			profile = User_Info.objects.get(user_id = request.user.id)
			#Get the profile info of the person user is seeing
			author = User_Info.objects.get(user_id = person.id)
			
			args['storycount'] = storycount
			args['list'] = list
			args['followingcount'] = followingcount
			args['followerscount'] = followercount
			args['profile'] = profile
			args['person'] = person
			args['author'] = author
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
		print "sfddsf"
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

