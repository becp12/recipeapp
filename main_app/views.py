from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Recipe

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def recipes_index(request):
  return render(request, 'recipes/index.html')    

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class RecipeCreate(CreateView, LoginRequiredMixin):
  model = Recipe
  fields = ['title', 'servings', 'preptime', 'cookingtime', 'category', 'method']
  # success_url = '/recipes/'

  def form_valid(self, form):
    print('***')
    print(self.request.user)
    form.instance.chef = self.request.user
    return super().form_valid(form)