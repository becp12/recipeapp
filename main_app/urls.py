from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('recipes/', views.recipes_index, name='index'),
    path('recipes/my/', views.recipes_myindex, name='myindex'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipe_create'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name='detail'),
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe_delete'),
    path('recipes/<int:recipe_id>/add_comment/', views.add_comment, name='add_comment'),
    path('recipes/<int:pk>/comment_delete', views.CommentDelete.as_view(), name='comment_delete'),
    path('recipes/<int:recipe_id>/add_tiptrick/', views.add_tiptrick, name='add_tiptrick'),
    path('recipes/<int:pk>/tiptrick_delete', views.TipTrickDelete.as_view(), name='tiptrick_delete'),
    path('recipes/<int:recipe_id>/add_photo/', views.add_photo, name='add_photo'),

]

