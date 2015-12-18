from django.contrib import admin

# Register your models here.
from models import Story

class StoryAdmin(admin.ModelAdmin):
	class Meta:
		model = Story
		
admin.site.register(Story,StoryAdmin)


