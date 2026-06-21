from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import (
    ShopSettings, Announcement, Category, Product,
    Offer, Testimonial, GalleryImage, ContactMessage
)
from .serializers import (
    ShopSettingsSerializer, AnnouncementSerializer, CategorySerializer,
    ProductSerializer, OfferSerializer, TestimonialSerializer,
    GalleryImageSerializer, ContactMessageSerializer
)


@api_view(['GET'])
def get_shop_data(request):
    """Single endpoint that returns ALL homepage + about page data."""
    settings_obj = ShopSettings.objects.first()
    settings_data = ShopSettingsSerializer(settings_obj, context={'request': request}).data if settings_obj else {}

    announcements = Announcement.objects.filter(is_active=True)
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True, is_available=True)
    new_arrivals = Product.objects.filter(is_new_arrival=True, is_available=True)[:8]
    offers = Offer.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    gallery = GalleryImage.objects.filter(is_active=True)

    return Response({
        'settings': settings_data,
        'announcements': AnnouncementSerializer(announcements, many=True).data,
        'categories': CategorySerializer(categories, many=True, context={'request': request}).data,
        'featured_products': ProductSerializer(featured_products, many=True, context={'request': request}).data,
        'new_arrivals': ProductSerializer(new_arrivals, many=True, context={'request': request}).data,
        'offers': OfferSerializer(offers, many=True, context={'request': request}).data,
        'testimonials': TestimonialSerializer(testimonials, many=True, context={'request': request}).data,
        'gallery': GalleryImageSerializer(gallery, many=True, context={'request': request}).data,
    })


@api_view(['GET'])
def get_products(request):
    category_slug = request.GET.get('category')
    products = Product.objects.filter(is_available=True)
    if category_slug:
        products = products.filter(category__slug=category_slug)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
def send_contact_message(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Message sent! We will contact you soon.'},
                        status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
