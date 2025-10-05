from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True,null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], blank=True, null=True)

    def __str__(self):
        return self.username
    
    
# -------------------------
# Seller Model
# -------------------------

class Seller(models.Model):

    # Contact Info
    seller_phone = models.CharField(max_length=10, unique=True)
    seller_email = models.EmailField(unique=True)
    seller_password = models.CharField(max_length=255,null=True)

    # Business Info
    business_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    seller_address = models.TextField()
    seller_pincode = models.CharField(max_length=6)

    BUSINESS_TYPE_CHOICES = [
        ("proprietorship", "Proprietorship"),
        ("partnership", "Partnership"),
        ("private_limited", "Private Limited"),
        ("llp", "LLP"),
        ("individual", "Individual Seller"),
    ]
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES)

    # Selling Info
    SELLING_CATEGORY_CHOICES = [
        ("all", "All Categories"),
        ("mobile", "Mobile Phones"),
        ("watch", "Watches"),
        ("laptop", "Laptop"),
        ("shoes", "Shoes"),
        ("tv", "Television"),
        ("earphones", "Ear Phones"),
        ("toys", "Toys"),
        ("books", "Books"),
    ]
    selling_category = models.CharField(
        max_length=50,
        choices=SELLING_CATEGORY_CHOICES,
        default="all"
    )

    gstin = models.CharField(max_length=15, blank=True, null=True, help_text="Enter 15-digit GSTIN")

    # Bank Details
    bank_account_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_password(self, raw_password):
        """Hash and set the seller password"""
        self.seller_password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check a raw password against the stored hash"""
        return check_password(raw_password, self.seller_password)
    
    def __str__(self):
        return f"{self.business_name} || :>> {self.seller_email}"



    
# Phone Product


class MobileProduct(models.Model):
    # --- General Info ---
    productName = models.CharField(max_length=200)
    brandName = models.CharField(max_length=100)
    modelNumber = models.CharField(max_length=100, null=True, blank=True)
    launchDate = models.DateField(null=True, blank=True)
    productDescription = models.TextField()

    SIM_CHOICE = [
        ("Single SIM (Nano-SIM)", "Single SIM (Nano-SIM)"),
        ("Dual SIM (Nano-SIM, dual stand-by)", "Dual SIM (Nano-SIM, dual stand-by)"),
        ("eSIM", "eSIM"),
        ("Dual SIM + eSIM", "Dual SIM + eSIM"),
    ]

    # --- Dimension ---
    height = models.CharField(max_length=10, null=True, blank=True)
    width = models.CharField(max_length=10, null=True, blank=True)
    thickness = models.CharField(max_length=10, null=True, blank=True)
    weight = models.CharField(max_length=50, null=True, blank=True)
    build = models.CharField(max_length=100, null=True, blank=True)
    simType = models.CharField(max_length=50, choices=SIM_CHOICE, null=True, blank=True)

    # --- Display ---
    displayType = models.CharField(max_length=100, null=True, blank=True)
    displaySize = models.CharField(max_length=50, null=True, blank=True)
    displayResolution1 = models.CharField(max_length=50, null=True, blank=True)
    displayResolution2 = models.CharField(max_length=50, null=True, blank=True)
    protection = models.CharField(max_length=100, null=True, blank=True)
    refreshRate = models.CharField(max_length=50, null=True, blank=True)

    # --- Platform ---
    OS_CHOICE = [
        ("Android", "Android"),
        ("IOS", "IOS"),
    ]
    os = models.CharField(max_length=50, choices=OS_CHOICE, null=True, blank=True)
    chipset = models.CharField(max_length=100, null=True, blank=True)
    cpu = models.CharField(max_length=100, null=True, blank=True)
    gpu = models.CharField(max_length=100, null=True, blank=True)

    # --- Memory ---
    CARDSLOT_CHOICE = [
        ("yes", "Yes"),
        ("no", "No"),
    ]
    cardSlot = models.CharField(max_length=10, choices=CARDSLOT_CHOICE, null=True, blank=True)
    internalStorageRam = models.CharField(max_length=50, null=True, blank=True)
    internalStorageRom = models.CharField(max_length=50, null=True, blank=True)

    # --- Camera ---
    CAMERA_CHOICE = [
        ("8k 30fps", "8k 30fps"),
        ("4k 120fps", "4k 120fps"),
        ("4k 60fps", "4k 60fps"),
        ("4k 30fps", "4k 30fps"),
        ("1080p 120fps", "1080p 120fps"),
        ("1080p 60fps", "1080p 60fps"),
        ("1080p 30fps", "1080p 30fps"),
    ]
    mainLens = models.TextField(null=True, blank=True)
    wideAngleLens = models.TextField(null=True, blank=True)
    macroLens = models.TextField(null=True, blank=True)
    telePhotoLens = models.TextField(null=True, blank=True)
    opticalZoom = models.TextField(null=True, blank=True)
    mainCameraVideo = models.CharField(max_length=20, choices=CAMERA_CHOICE, null=True, blank=True)
    selfieCamera = models.TextField(null=True, blank=True)
    selfieWideCamera = models.TextField(null=True, blank=True)
    selfieCameraVideo = models.CharField(max_length=20, choices=CAMERA_CHOICE, null=True, blank=True)

    # --- Sound ---
    loudspeaker = models.BooleanField(default=True)
    stereoSpeakers = models.BooleanField(default=True)
    audioJack = models.BooleanField(default=False)

    # --- Comms ---
    wlan = models.CharField(max_length=100, null=True, blank=True)
    bluetooth = models.CharField(max_length=100, null=True, blank=True)
    usb = models.CharField(max_length=100, null=True, blank=True)
    gps = models.BooleanField(default=True)
    nfc = models.BooleanField(default=False)
    infrared = models.BooleanField(default=False)
    radio = models.BooleanField(default=False)

    # --- Security ---
    FINGERPRINT_CHOICES = [
        ("none", "No Fingerprint"),
        ("rear-mounted", "Rear-mounted"),
        ("side-mounted", "Side-mounted"),
        ("front-mounted", "Front-mounted"),
        ("under-display-optical", "Under-display (Optical)"),
        ("under-display-ultrasonic", "Under-display (Ultrasonic)"),
        ("power-button", "Power Button Integrated"),
    ]
    fingerPrint = models.CharField(max_length=50, choices=FINGERPRINT_CHOICES, null=True, blank=True)
    faceUnlock = models.BooleanField(default=True)

    # --- Battery ---
    batteryType = models.CharField(max_length=50, null=True, blank=True)
    batteryCapacity = models.CharField(max_length=50, null=True, blank=True)
    chargingSpeed = models.CharField(max_length=100, null=True, blank=True)
    wirelessCharging = models.BooleanField(default=False)
    wirelessChargingSpeed = models.CharField(max_length=20, null=True, blank=True)  # e.g., "50W"

    # --- Other Specifications ---
    MODELS_CHOICES = [
        ("6 GB | 64 GB", "6 GB | 64 GB"),
        ("6 GB | 128 GB", "6 GB | 128 GB"),
        ("6 GB | 256 GB", "6 GB | 256 GB"),
        ("8 GB | 128 GB", "8 GB | 128 GB"),
        ("8 GB | 256 GB", "8 GB | 256 GB"),
        ("8 GB | 512 GB", "8 GB | 512 GB"),
        ("12 GB | 128 GB", "12 GB | 128 GB"),
        ("12 GB | 256 GB", "12 GB | 256 GB"),
        ("12 GB | 512 GB", "12 GB | 512 GB"),
        ("12 GB | 1 TB", "12 GB | 1 TB"),
        ("16 GB | 128 GB", "16 GB | 128 GB"),
        ("16 GB | 256 GB", "16 GB | 256 GB"),
        ("16 GB | 512 GB", "16 GB | 512 GB"),
        ("16 GB | 1 TB", "16 GB | 1 TB"),
    ]
    colors = models.CharField(max_length=200, null=True, blank=True)
    modelsAvailable = models.CharField(max_length=20, choices=MODELS_CHOICES, null=True, blank=True)
    sar = models.CharField(max_length=50, null=True, blank=True)

    # --- Seller ---
    productSellerName = models.CharField(max_length=200)
    productCompanyName = models.CharField(max_length=200)
    sellerPhone = models.CharField(max_length=15, null=True, blank=True)
    sellerEmail = models.EmailField(null=True, blank=True)

    # --- Images ---
    productImage1 = models.ImageField(upload_to='mobile_images/', null=True, blank=True)
    productImage2 = models.ImageField(upload_to='mobile_images/', null=True, blank=True)
    productImage3 = models.ImageField(upload_to='mobile_images/', null=True, blank=True)

    # --- Shipping ---
    productAddress = models.CharField(max_length=200)
    productState = models.CharField(max_length=100)
    productCountry = models.CharField(max_length=100)
    productPincode = models.CharField(max_length=10)

    # --- Pricing ---
    productPrice = models.DecimalField(max_digits=10, decimal_places=2)
    discountPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.brandName} {self.productName} ({self.modelNumber})'




# User Cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total() for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

# Cart Items
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(MobileProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        price = self.product.productPrice - self.product.discountPrice 
        return price * self.quantity

    def __str__(self):
        return f"{self.product.productName} × {self.quantity}"
