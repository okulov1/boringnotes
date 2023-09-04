from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, DetailView

from .forms import RegisterUserForm, LoginUserForm, ContactForm, RedactNoteForm
from .models import *


class IndexView(View):
    def get(self, request, *args, **kwargs):
        try:
            notes = Notes.objects.filter(author=request.user).order_by('-time_update')
        except:
            context = {
                'title': 'BoringNotes'
            }
            return render(request, 'notes/index_n.html', context=context)

        context = {
            'title': 'BoringNotes',
            'notes': notes
        }

        return render(request, 'notes/index.html', context=context)


class NotesAbout(ListView):
    model = Notes
    template_name = 'notes/about.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BoringNotes - О нас'
        return context


class NotesAllNotes(ListView):
    model = Notes
    template_name = 'notes/all_notes.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BoringNotes - Все заметки'
        return context

    def get_queryset(self):
        return Notes.objects.filter(is_published=True).order_by('-time_update')


class NotesViewNote(ListView):
    model = Notes
    template_name = 'notes/view_note.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BoringNotes - Заметка'
        return context

    def get_queryset(self):
        return Notes.objects.filter(pk=self.kwargs['note_id'])


class NotesSingUp(CreateView):
    form_class = RegisterUserForm
    template_name = 'notes/sing_up.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BoringNotes - Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class NotesLogIn(LoginView):
    form_class = LoginUserForm
    template_name = 'notes/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BoringNotes - Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class NotesAccount(ListView):
    model = User
    template_name = 'notes/account.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'BoringNotes - @{self.request.user.username}'
        context['user'] = self.request.user
        return context


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('log_in')


class ContactView(View):
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            print('\n' * 5 + str(form.cleaned_data | {'user': request.user.username}) + '\n' * 5)
            return redirect('account')

        context = {
            'title': 'BoringNotes - Обратная связь',
            'form': form
        }
        return render(request, 'notes/contact.html', context=context)

    def get(self, request, *args, **kwargs):
        form = ContactForm()

        context = {
            'title': 'BoringNotes - Обратная связь',
            'form': form
        }
        return render(request, 'notes/contact.html', context=context)


class UserView(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs['username']
        try:
            user = User.objects.get(username=username)
        except:
            return redirect('home')

        context = {
            'title': f'BoringNotes - @{username}',
            'user': user
        }

        return render(request, 'notes/view_user.html', context=context)


def redact(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except:
        return HttpResponseNotFound('<title>BoringNotes - 404</title><h1>404</h1> <h3> Страница не найдена! </h3>')

    if request.method == 'POST':
        if request.POST:
            try:
                is_pub = request.POST['is_published']
            except:
                is_pub = False

            if is_pub == 'on':
                is_pub = True

            note_upd = note
            note_upd.title = request.POST['title']
            note_upd.text = request.POST['content']
            note_upd.is_published = is_pub
            note_upd.save()
            note = note_upd

    form = RedactNoteForm(initial={
        'title': note.title,
        'content': note.text,
        'is_published': note.is_published
    })

    context = {
        'title': f'BoringNotes - Заметка {note_id}',
        'note': note,
        'form': form
    }

    return render(request, 'notes/redact_note.html', context=context)


def add_note(request):
    user = request.user
    try:
        note = Notes.objects.create(title='Новая заметка', text='Текст новой заметки', author=user)
    except:
        context = {
            'title': 'BoringNotes - добавить заметку'
        }
        return render(request, 'notes/add_n.html', context=context)
    note_id = note.id
    note.save()

    return redirect('home')


def delete_note(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except:
        return redirect('home')

    try:
        user = request.user
        if note.author == user:
            note.delete()
    except:
        return redirect('home')

    return redirect('home')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>404</h1> <h3> Страница не найдена! </h3>')
