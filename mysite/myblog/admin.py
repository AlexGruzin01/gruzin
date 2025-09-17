from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, Post, Comment, Site, News, Reviews, Projects, Gallery


# Register your models here.
class GalleryInline(admin.TabularInline):
    model = Gallery
    fk_name = 'project'
    extra = 1


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'slug')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('id','title', 'slug', 'category', 'order', 'is_published', 'page_image', 'get_html_photo')
    list_display_links = ('title', 'slug')
    list_editable = ('category', 'order', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    save_as = True

    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=50>')

    get_html_photo.short_description = 'Фото'


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'is_published')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    save_as = True


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'active')
    list_display_links = ('name', 'email', 'post')
    # prepopulated_fields = {'slug': ('slug',)}


class SiteAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Запрещаем добавлять новые записи
        return False

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление
        return False

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'year', 'order')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    save_as = True
    inlines = (GalleryInline,)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer', 'is_published')
    list_display_links = ('id', 'reviewer')
    list_editable = ('is_published',)



admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Projects, ProjectAdmin)