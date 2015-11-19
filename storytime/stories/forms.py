from django import forms
from models import Text,Image,Story,User_Info,Profile_Image

class StoryForm(forms.ModelForm):
	class Meta:
		model = Story
		exclude =("user","id","datetime","like","storyid","starcount","complete")

class TextForm(forms.ModelForm):
	class Meta:
		model = Text
		exclude = ("storyid","user","textid")
		
class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		exclude = ("storyid","user","imageid")
		
class EditForm(forms.ModelForm):
	class Meta:
		model = User_Info
		exclude = ("profile_pic","user")
		
class EditFormImage(forms.ModelForm):
	class Meta:
		model = Profile_Image
		exclude = ("user","used")