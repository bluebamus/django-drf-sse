"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import (
    index,
    index_update_state,
    sse_stream,
    sse_stream_update_state,
)

urlpatterns = [
    path("", index, name="index"),
    path("1/", index_update_state, name="index_update_state"),
    path("stream/", sse_stream, name="sse_stream"),
    path("stream1/", sse_stream_update_state, name="sse_stream_update_state"),
]
