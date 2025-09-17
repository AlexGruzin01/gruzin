from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', CategoryPageView.as_view(), name='category'),
    path('post/<slug:slug>/', ProductPageView.as_view(), name='post'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('news/', NewsPageView.as_view(), name='news'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='new'),
    path('projects/', ProjectsPageView.as_view(), name='projects'),
    path('reviews/', ReviewsPageView.as_view(), name='reviews'),
    path('search/', SearchView.as_view(), name='search'),
    # path('tag/<slug:slug>/', show_tags, name='tag'),
    # path('rubric/<int:pk>/', show_rubric, name='rubrics'),
    path('contacts/', ContactPageView.as_view(), name='contacts')
]