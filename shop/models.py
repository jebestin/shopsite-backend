from django.db import models


class ShopSettings(models.Model):
    """Everything about the shop — controlled from Admin Panel. Singleton (only one row)."""
    shop_name = models.CharField(max_length=200, default="My Boutique")
    tagline = models.CharField(max_length=300, default="Fashion for Everyone", blank=True)
    logo = models.ImageField(upload_to='shop/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='shop/', blank=True, null=True)
    hero_heading = models.CharField(max_length=200, default="New Collection Arrived!")
    hero_subheading = models.CharField(max_length=300, default="Shop the latest trends", blank=True)

    # About Page
    about_heading = models.CharField(max_length=200, default="About Us", blank=True)
    about_text = models.TextField(blank=True, help_text="Tell customers about your shop's story")
    about_image = models.ImageField(upload_to='shop/', blank=True, null=True)
    years_in_business = models.PositiveIntegerField(null=True, blank=True)

    # Contact Info
    phone_number = models.CharField(max_length=20, default="+91XXXXXXXXXX")
    whatsapp_number = models.CharField(max_length=20, default="+91XXXXXXXXXX",
                                       help_text="Include country code, e.g. +919876543210")
    whatsapp_message = models.CharField(max_length=200, default="Hi! I want to know more about your products.")
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    # Social Media
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    # Google Maps
    google_maps_embed_url = models.TextField(blank=True,
                                              help_text="Google Maps > Share > Embed a map > copy src URL")

    # Theme Colors
    primary_color = models.CharField(max_length=7, default="#D4286A")
    secondary_color = models.CharField(max_length=7, default="#2D2D2D")
    accent_color = models.CharField(max_length=7, default="#FFD700")

    meta_description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shop Settings"
        verbose_name_plural = "Shop Settings"

    def __str__(self):
        return f"Settings for {self.shop_name}"


class Announcement(models.Model):
    text = models.CharField(max_length=500, help_text="E.g. '🎉 SALE: Up to 50% off this weekend!'")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:60]


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return None


class Offer(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    discount_text = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    background_color = models.CharField(max_length=7, default="#FF6B6B")
    valid_till = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.rating}★"


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.caption or f"Gallery Image {self.id}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d %b %Y')}"
