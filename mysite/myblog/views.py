from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.core.mail import send_mail, BadHeaderError
from unicodedata import category

from mysite import settings
from .forms import CommentForm, ContactForm
from .models import Post, Category, Comment, News, Projects, Reviews, Site


# Create your views here.
# def index(request):
#     return render(request, 'myblog/index.html')
#
#
# def category(request):
#     pass
#
#
# def get_post(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'myblog/post.html', {'post': post})
#
#
def product_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return redirect(request.path)
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request,
                  'myblog/post.html', context=context)
#
#
def contacts(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['name'], form.cleaned_data['content'], 'alfamilk2024@yandex.ru',
                      ['alfamilk2024@yandex.ru'], )
            if mail:
                messages.success(request, 'Ваше письмо отправлено')
                return redirect('contacts')
            else:
                messages.error(request, 'NO')
    else:
        form = ContactForm()
    return render(request, 'myblog/contacts.html', context={'form': form})


# classes
# class HomePageView(TemplateView):
#     template_name = 'myblog/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Главная страница!'
#         context["content"] = 'Тут будет сайт Альфамилк'
#         context['posts'] = Post.objects.filter(category__slug='uslugi', is_published=True)
#         return context


class IndexView(ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'posts'
    equipment_slug = 'oborudovanie'
    service_slug = 'uslugi'
    ordering = ['order','-created']

    def get_equipment_queryset(self):
        """QuerySet для оборудования"""
        return Post.objects.filter(
            category__slug=self.equipment_slug
        ).select_related('category').order_by('order','-created')[:10]

    def get_service_queryset(self):
        """QuerySet для услуг"""
        return Post.objects.filter(
            category__slug=self.service_slug
        ).select_related('category').order_by('order','-created')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная страница!'
        context['news'] = News.objects.filter(is_published=True).order_by('-created')[:2]
        context['equipment_qs'] = self.get_equipment_queryset()
        context['service_qs'] = self.get_service_queryset()
        context['info'] = Site.objects.all()
        return context

    # def get_queryset(self):
        # return Category.objects.filter(parent__isnull=False)
        # return Post.objects.filter(is_published=True)


class CategoryPageView(ListView):
    model = Post
    template_name = 'myblog/category.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class ProductPageView(DetailView):
    model = Post
    # form_class = CommentForm
    # success_url = "/index/"
    template_name = 'myblog/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=post)
        context['comment_form'] = CommentForm()
        context['other_posts'] = Post.objects.filter(is_published=True).exclude(slug=self.kwargs['slug']).exclude(category__slug='oborudovanie')
        context['title'] = post
        return context


class ContactPageView(FormView):
    template_name = 'myblog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        # Обработка данных формы
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        content = form.cleaned_data['content']

        # Здесь можно добавить логику обработки формы:
        # - Отправка email
        # - Сохранение в базу данных
        # - и т.д.

        # Пример отправки email:

        send_mail(
            subject,
            f"Сообщение от {name} ({email}):\n\n{content}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
        )

        try:
            # Отправляем email администратору (ОТ вашего сервера)
            send_mail(
                subject=f"Форма обратной связи: {subject}",
                message=content,
                from_email=settings.DEFAULT_FROM_EMAIL,  # ОТ вашего сервера
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # КУДА (ваш email)
                fail_silently=False,
            )

            # Отправляем подтверждение пользователю (ОТ вашего сервера)
            send_mail(
                subject=f"Подтверждение получения вашего сообщения: {subject}",
                message='user_message',
                from_email=settings.DEFAULT_FROM_EMAIL,  # ОТ вашего сервера
                recipient_list=[email],  # КУДА (email пользователя)
                fail_silently=False,
            )

            messages.success(self.request, 'Сообщение успешно отправлено! Мы скоро с вами свяжемся.')

        except BadHeaderError:
            messages.error(self.request, 'Обнаружен неверный заголовок.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Произошла ошибка при отправке: {str(e)}')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class AboutPageView(TemplateView):
    template_name = 'myblog/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Отзывы клиентов'
        context['reviews'] = Reviews.objects.filter(is_published=True).order_by('-created')
        return context


class NewsPageView(ListView):
    model = News
    template_name = 'myblog/news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-created')

class NewsDetailView(DetailView):
    model = News
    template_name = 'myblog/news_detail.html'
    context_object_name = 'new'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        new = get_object_or_404(News, slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['other_news'] = News.objects.filter(is_published=True).exclude(slug=self.kwargs['slug']).order_by('-created')
        context['title'] = new.title
        return context


class ProjectsPageView(ListView):
    model = Projects
    template_name = 'myblog/projects.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        return Projects.objects.prefetch_related('images').all().order_by('-year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проекты'
        return context


class ReviewsPageView(ListView):
    model = Reviews
    template_name = 'myblog/reviews.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Reviews.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отзывы'
        return context


class SearchView(ListView):
    # model = News
    template_name = 'myblog/search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            return []

        # Ищем в обеих моделях
        news = News.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        projects = Projects.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

        # Объединяем результаты
        return list(news) + list(projects)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.request.GET.get('q')
    #
    #     if query:
    #         queryset = queryset.filter(
    #             Q(title__icontains=query) |
    #             Q(content__icontains=query)
    #         )
    #     return queryset
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['query'] = self.request.GET.get('q', '')
    #     return context


