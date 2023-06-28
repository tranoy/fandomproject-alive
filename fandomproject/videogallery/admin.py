from django.contrib import admin
from . models import Gallery
# Register your models here.

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user_id', 'like_count') # 목록에 여러 필드 추가, 밑에 register에도 추가해줘야 함
    list_filter = ['title', 'user_id']  # 목록에 검색 필드 추가

admin.site.register(Gallery, GalleryAdmin)