from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ShopSettings, Announcement, Category, Product,
    Offer, Testimonial, GalleryImage, ContactMessage
)


@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🏪 Basic Info', {
            'fields': ('shop_name', 'tagline', 'logo', 'meta_description')
        }),
        ('🖼️ Homepage Hero Banner', {
            'fields': ('hero_image', 'hero_heading', 'hero_subheading')
        }),
        ('📖 About Page', {
            'fields': ('about_heading', 'about_text', 'about_image', 'years_in_business')
        }),
        ('📞 Contact & WhatsApp', {
            'fields': ('phone_number', 'whatsapp_number', 'whatsapp_message', 'email', 'address')
        }),
        ('📱 Social Media Links', {
            'fields': ('instagram_url', 'facebook_url', 'youtube_url')
        }),
        ('📍 Google Maps', {
            'fields': ('google_maps_embed_url',),
        }),
        ('🎨 Brand Colors', {
            'fields': ('primary_color', 'secondary_color', 'accent_color'),
        }),
    )

    def has_add_permission(self, request):
        if ShopSettings.objects.exists():
            return False
        return True


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_display_links = ['text']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'original_price', 'discount_badge',
                    'is_featured', 'is_new_arrival', 'is_available', 'image_preview']
    list_editable = ['is_featured', 'is_new_arrival', 'is_available']
    list_filter = ['category', 'is_featured', 'is_new_arrival', 'is_available']
    search_fields = ['name', 'description']
    list_display_links = ['name']

    fieldsets = (
        ('Product Info', {'fields': ('name', 'category', 'description', 'image')}),
        ('Pricing', {'fields': ('price', 'original_price')}),
        ('Visibility', {'fields': ('is_featured', 'is_new_arrival', 'is_available')}),
    )

    def discount_badge(self, obj):
        pct = obj.discount_percent
        if pct:
            return format_html('<span style="color:red;font-weight:bold">{}% OFF</span>', pct)
        return "-"
    discount_badge.short_description = "Discount"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Photo"


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_text', 'valid_till', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_display_links = ['title']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_display_links = ['customer_name']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['caption', 'order', 'is_active', 'image_preview']
    list_editable = ['order', 'is_active']
    list_display_links = ['caption']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover" />', obj.image.url)
        return ""
    image_preview.short_description = "Preview"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'message_preview', 'is_read', 'created_at']
    list_filter = ['is_read']
    list_editable = ['is_read']
    list_display_links = ['name']
    readonly_fields = ['name', 'phone', 'email', 'message', 'created_at']

    def message_preview(self, obj):
        return obj.message[:60] + "..." if len(obj.message) > 60 else obj.message
    message_preview.short_description = "Message"

    def has_add_permission(self, request):
        return False
