from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import (
    Category,
    Genre,
    Movie,
    MovieShots,
    Actor,
    Rating,
    RatingStar,
    Review,
)


class MovieAdminForm(forms.ModelForm):
    """Форма с виджетом ckeditor"""

    class Meta:
        model = Movie
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""

    list_display = ("name", "url")
    list_display_links = ("name",)
    prepopulated_fields = {"url": ("name",)}


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""

    model = Review
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""

    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    prepopulated_fields = {"url": ("title",)}
    actions = ["publish", "unpublish"]
    form = MovieAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {"fields": (("title", "tagline"),)}),
        (None, {"fields": ("description", ("poster", "get_image"))}),
        (None, {"fields": (("year", "world_premiere", "country"),)}),
        (
            "Actors",
            {
                "classes": ("collapse",),
                "fields": (("actors", "directors", "genres", "category"),),
            },
        ),
        (None, {"fields": (("budget", "fees_in_usa", "fess_in_world"),)}),
        ("Options", {"fields": (("url", "draft"),)}),
    )

    @admin.display(description="Постер")
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    @admin.action(description="Снять с публикации", permissions=("change",))
    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    @admin.action(description="Опубликовать", permissions=("change",))
    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""

    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""

    list_display = ("name", "url")
    prepopulated_fields = {"url": ("name",)}


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""

    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    @admin.display(description="Изображение")
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""

    list_display = ("star", "movie", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""

    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    @admin.display(description="Изображение")
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
