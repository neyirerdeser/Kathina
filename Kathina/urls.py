from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'Kathina.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # add kathina_app urls
    url(r'^events/', include('kathina_app.urls', namespace='kathina')),
    url(r'^tasks/', include('kathina_app.urls', namespace='kathina')),
    url(r'^day/', include('kathina_app.urls', namespace='kathina')),
]
