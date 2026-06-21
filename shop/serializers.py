from rest_framework import serializers
from .models import (
    ShopSettings, Announcement, Category, Product,
    Offer, Testimonial, GalleryImage, ContactMessage
)


class ShopSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSettings
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'text']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    discount_percent = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name', 'description',
            'price', 'original_price', 'discount_percent',
            'image', 'is_featured', 'is_new_arrival', 'is_available'
        ]


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'title', 'subtitle', 'discount_text', 'image', 'background_color', 'valid_till']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'customer_name', 'review', 'rating', 'photo']


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'caption']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'message']
