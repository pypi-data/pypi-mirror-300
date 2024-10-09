from django.conf import settings
from django.urls import path

from logui.controllers.base import (
    log_folders_view, log_files_view, log_file_view,
    download_log_file_view, api_log_file_view
)

app_name = 'logui'

urlpatterns = [
    path(f'{settings.LOGUI_URL_PREFIX}',
         log_folders_view,
         name='log_folders'),
    path(f'{settings.LOGUI_URL_PREFIX}<str:folder_name>/',
         log_files_view,
         name='log_files'),
    path(f'{settings.LOGUI_URL_PREFIX}<str:folder_name>/<str:file_name>/',
         log_file_view,
         name='log_file'),
    path(f'{settings.LOGUI_URL_PREFIX}<str:folder_name>/<str:file_name>/download/',
         download_log_file_view,
         name='log_file_download'),
    path(f'{settings.LOGUI_URL_PREFIX}api/<str:folder_name>/<str:file_name>/',
         api_log_file_view,
         name='api_log_file'),
]
