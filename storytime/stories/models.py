from django.conf import settings
from django.db import models
from time import time
import datetime
import uuid
from sorl.thumbnail import ImageField

# Create your models here.
#Return the name to the Image file.
def get_upload_file_name(instance,filename):
	return "media/" + str(instance.user_id) + "/%s_%s" % (str(time()).replace('.','_'),filename)


# User can have multiple story
class Story(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	datetime = models.DateTimeField(auto_now_add=True, blank=False)
	starcount = models.IntegerField(default = 0)
	title = models.CharField(max_length = 200)
	storyid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	complete = models.BooleanField(default=False)
	commentcount = models.IntegerField(default = 0)
	
#Text will be inside story
class Text(models.Model):
	id = models.AutoField(primary_key=True)
	text = models.CharField(max_length = 200)
	position = models.IntegerField(default = 0)
	storyid = models.ForeignKey(Story)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default = 1)
	
	
	
#Item will be inside story
class Image(models.Model):
	source = models.ImageField(upload_to = get_upload_file_name)
	position = models.IntegerField(default = 0)
	storyid = models.ForeignKey(Story)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default = 1)
	
class Profile_Image(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	image = models.ImageField(upload_to = get_upload_file_name,default='media/default/UserIconBlack.png')
	used = models.BooleanField(default=True)

class User_Info(models.Model):
	username = models.CharField(max_length = 200)
	user = models.OneToOneField(settings.AUTH_USER_MODEL,primary_key=True)
	desc = models.CharField(max_length = 200)
	profile_pic = models.ForeignKey(Profile_Image,null=True)
	
class Person(models.Model):
	name = models.ForeignKey(settings.AUTH_USER_MODEL)
	relationships = models.ManyToManyField('self', through='Relationship',
                                           symmetrical=False,
                                           related_name='related_to')
	def __unicode__(self):
		return '%s' %  (self.name)
	def add_relationship(self, person, status):
		relationship, created = Relationship.objects.get_or_create(
			from_person=self,
			to_person=person,
			status=status)
		return relationship

	def remove_relationship(self, person, status):
		Relationship.objects.filter(
			from_person=self,
			to_person=person,
			status=status).delete()
		return		
	def get_relationships(self, status):
		return self.relationships.filter(
			to_people__status=status,
			to_people__from_person=self)

	def get_related_to(self, status):
		return self.related_to.filter(
			from_people__status=status,
			from_people__to_person=self)

	def get_following(self):
		return self.get_relationships(RELATIONSHIP_FOLLOWING)

	def get_followers(self):
		return self.get_related_to(RELATIONSHIP_FOLLOWING)
#Relationship
RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class Relationship(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_people')
    to_person = models.ForeignKey(Person, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
	
class Star(models.Model):
	storyid = models.ForeignKey(Story)
	user_id = models.ForeignKey(settings.AUTH_USER_MODEL)
	status = models.BooleanField(default=True)


