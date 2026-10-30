from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Tour, BookingRequest, Card, UserTour

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Дополнительно', {'fields': ('phone',)}),)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'duration', 'is_active')
    list_filter = ('category', 'is_active')

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'masked_number', 'created_at')

@admin.register(UserTour)
class UserTourAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'status', 'purchase_date')
    list_filter = ('status',)