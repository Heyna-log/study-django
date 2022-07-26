from django.contrib import admin

from .models import Post, Category

admin.site.register(Post) # admin 페이지에 만든 모델을 등록


# admin custom
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # post를 추가할 경우 자동으로 카테고리 이름과 매핑되게 함(자동으로 카테고리 이름을 슬러그로 사용)


admin.site.register(Category, CategoryAdmin)