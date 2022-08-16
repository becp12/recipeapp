from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Recipe, Comment
from .forms import CommentForm

# Create your views here.
def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')


@login_required
def recipes_index(request):
  recipes = Recipe.objects.all()
  return render(request, 'recipes/index.html', { 'recipes': recipes })    


def recipes_detail(request, recipe_id):
  recipe = Recipe.objects.get(id=recipe_id, chef=request.user)
  comment_form = CommentForm()
  return render(request, 'recipes/detail.html', { 'recipe': recipe, 'comment_form': comment_form })

@login_required
def add_comment(request, recipe_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.recipe_id = recipe_id
    new_comment.chef_id = request.user.id
    new_comment.save()
  return redirect('detail', recipe_id=recipe_id)


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
  fields = ['title', 'servings', 'preptime', 'cookingtime', 'category', 'ingredients', 'method']

  def form_valid(self, form):
    form.instance.chef = self.request.user
    return super().form_valid(form)


class RecipeUpdate(UpdateView, LoginRequiredMixin):
  model = Recipe
  fields = ['title', 'servings', 'preptime', 'cookingtime', 'category', 'ingredients', 'method']


class RecipeDelete(DeleteView, LoginRequiredMixin):
  model = Recipe
  success_url = '/recipes/'

class CommentDelete(DeleteView, LoginRequiredMixin):
  model = Comment
  success_url = f'/recipes/{{recipe_id}}/'