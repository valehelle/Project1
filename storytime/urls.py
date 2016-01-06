"""storytime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from storytime.stories import views
import settings
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail

urlpatterns = [
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
            permanent=False),
        name="favicon"
    ),
	url(r'^admin/', include(admin.site.urls) ),
	url(r'^accounts/register/complete/register/closed/',views.register_closed),
	url(r'^request_access/',views.request_access),
	url(r'^accounts/login/',views.custom_login),
	url(r'^company/about/$',views.about),
	url(r'^company/privacy/$',views.privacy),
	url(r'^company/terms/$',views.terms),
	url(r'^company/acceptable/$',views.acceptable),
	url(r'^company/support/$',views.support),
	url(r'^accounts/register/complete/register/$', RegistrationViewUniqueEmail.as_view(),name='registration_register'),
	url(r'^accounts/register/complete/', include('registration.backends.default.urls')),
	url(r'^stories/create_stories/',views.create_stories),
	url(r'^stories/create_album/store_album/',views.store_album),
	url(r'^stories/create_album/store_image/',views.store_image),
	url(r'^stories/create_album/album_finish/',views.album_finish),
	url(r'^stories/create_album/',views.create_album),
	url(r'^stories/add_star/',views.add_star),
	url(r'^comments/posted/$',views.custom_posted),
	url(r'^comments/', include('django_comments.urls')),
	url(r'^stories/read/',views.read_stories),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
	url(r'^profile/edit/image/',views.image_edit),
	url(r'^profile/edit/name/',views.name_edit),
	url(r'^profile/edit/desc/',views.desc_edit),
	url(r'^profile/edit/',views.user_edit),
	url(r'^profile/update_seen/',views.update_seen),
	url(r'^profile/',views.user_profile),
	url(r'^relationship/unfollow/',views.unfollow),
	url(r'^relationship/follow/',views.follow),
	url(r'^feed/previous/',views.feed_previous),
	url(r'^feed/',views.feed),
	url(r'^feedback/',views.feedback),
	url(r'^discovery/previous/',views.discovery_previous),
	url(r'^discovery/',views.discovery),
	url(r'^bookmark/previous/',views.bookmark_previous),
	url(r'^bookmark/',views.bookmark),
	url(r'^load_following/',views.load_following),
	url(r'^following/',views.following),
	url(r'^load_notification/',views.load_notification),
	url(r'^load_comment/',views.load_comment),
	url(r'^delete_story/',views.delete_stories),
	url(r'^notifications/',views.notification),
	url(r'^user_search/',views.user_search),
	url(r'^$',views.feed),
]
