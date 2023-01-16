from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.show_general_page),
    path('searching', views.execute_Search),
    path('upload_leaks_form', views.show_upload_leak_file_form),
    path('upload_leak', views.upload_leak)
] + static(settings.STATIC_URL, document_rootr=settings.STATIC_ROOT)
