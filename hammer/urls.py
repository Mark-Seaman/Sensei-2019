from django.conf.urls import url, include
from django.urls import path
from django.contrib.admin import site


# URL Route
urlpatterns = [

    # User Admin
    path('admin/', site.urls),

    # Insight
    path('insight/', include('insight.urls')),

    # Brain
    url(r'^brain/', include('brain.urls')),

    # Task
    url(r'^task/', include('tasks.urls')),

    # UNC
    url(r'^unc/', include('unc.urls')),

    # MyBook
    url(r'^', include('mybook.urls')),
]

