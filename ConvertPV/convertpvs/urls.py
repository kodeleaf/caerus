from django.urls import path
from .views import files, fileConverion, download_file, download_zip_files, view_file, Profile

urlpatterns = [
    # path('', files),

    # path('admin/', files, name='admin'),

    path('conversion/', files, name='files'),
    path('fileconverter/',fileConverion, name='fileconverter'),
    path('profile/', Profile, name='home'),



]