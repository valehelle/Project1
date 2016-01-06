from django import forms
from models import Text,Image,Story,User_Info,Profile_Image

class StoryForm(forms.ModelForm):
	class Meta:
		model = Story
		exclude =("user","id","datetime","like","storyid","starcount","complete","commentcount","type")

class TextForm(forms.ModelForm):
	class Meta:
		model = Text
		exclude = ("storyid","user","textid")
		
class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		exclude = ("caption","storyid","user","imageid")
		
class AlbumForm(forms.ModelForm):
	class Meta:
		model = Image
		exclude = ("user","imageid")
	
		
class EditUsername(forms.ModelForm):
	class Meta:
		model = User_Info
		exclude = ("profile_pic","user","desc")
		
class EditDesc(forms.ModelForm):
	class Meta:
		model = User_Info
		exclude = ("profile_pic","user","username")
		
class EditFormImage(forms.ModelForm):
	class Meta:
		model = Profile_Image
		exclude = ("user","used")