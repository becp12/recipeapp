import os
import uuid
import boto3

from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Recipe, Comment, TipTrick, Photo
from .forms import CommentForm, TipTrickForm

# Create your views here.
def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')


@login_required
def recipes_index(request):
  recipes = Recipe.objects.all()
  return render(request, 'recipes/index.html', { 'recipes': recipes })    


@login_required
def recipes_myindex(request):
  recipes = Recipe.objects.filter(chef=request.user)
  return render(request,'recipes/myindex.html', { 'recipes': recipes })


def recipes_detail(request, recipe_id):
  recipe = Recipe.objects.get(id=recipe_id)
  comment_form = CommentForm()
  tiptrick_form = TipTrickForm()
  return render(request, 'recipes/detail.html', {
    'recipe': recipe,
    'comment_form': comment_form,
    'tiptrick_form': tiptrick_form,
  })


@login_required
def add_comment(request, recipe_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.recipe_id = recipe_id
    new_comment.chef_id = request.user.id
    new_comment.save()
  return redirect('detail', recipe_id=recipe_id)


@login_required
def add_tiptrick(request, recipe_id):
  form = TipTrickForm(request.POST)
  if form.is_valid():
    new_tiptrick = form.save(commit=False)
    new_tiptrick.recipe_id = recipe_id
    new_tiptrick.chef_id = request.user.id
    new_tiptrick.save()
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
  success_url = '/recipes/my/'

  def form_valid(self, form):
    form.instance.chef = self.request.user
    return super().form_valid(form)


class RecipeUpdate(UpdateView, LoginRequiredMixin):
  model = Recipe
  fields = ['title', 'servings', 'preptime', 'cookingtime', 'category', 'ingredients', 'method']
  success_url = '/recipes/my/'


class RecipeDelete(DeleteView, LoginRequiredMixin):
  model = Recipe
  success_url = '/recipes/'


class CommentDelete(DeleteView, LoginRequiredMixin):
  model = Comment
  success_url = f'/recipes/{{recipe_id}}/'


class TipTrickDelete(DeleteView, LoginRequiredMixin):
  model = TipTrick
  success_url = f'/recipes/{{recipe_id}}/'


def random(self):
  return self.objects.order_by('?').values('cookingtime','title','chef_id').first()

@login_required
def add_photo(request, recipe_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      # build the full url string
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      # we can assign to recipe_id or recipe (if you have a recipe object)
      Photo.objects.create(url=url, recipe_id=recipe_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', recipe_id=recipe_id)