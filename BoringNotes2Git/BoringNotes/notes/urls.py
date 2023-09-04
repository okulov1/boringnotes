"""
URL configuration for BoringNotes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('about/', NotesAbout.as_view(), name='about'),
    path('all-notes/', NotesAllNotes.as_view(), name='all_notes'),
    path('sing-up/', NotesSingUp.as_view(), name='sing_up'),
    path('log-in/', NotesLogIn.as_view(), name='log_in'),
    path('account/', NotesAccount.as_view(), name='account'),
    path('log-out/', LogoutView.as_view(), name='log_out'),
    path('note/<int:note_id>/', NotesViewNote.as_view(), name='view_note'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('user/<slug:username>/', UserView.as_view(), name='user'),
    path('redact/<int:note_id>', redact, name='redact'),
    path('add-note/', add_note, name='add_note'),
    path('delete/<int:note_id>/', delete_note, name='delete')
]
