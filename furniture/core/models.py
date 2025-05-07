from django.db import models
from django.contrib.auth.models import User

# =========================
# 1. Profile
# =========================
class Profile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('furnisher', 'Furnisher'),
        ('consultant', 'Consultant'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    middle_name = models.CharField(max_length=50, blank=True, null=True)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    
    def save(self, *args, **kwargs):
        if self.user:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()
        super().save(*args, **kwargs)


# =========================
# 2. Category
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

    def __str__(self):
        return self.name


# =========================
# 3. Goods courses
# =========================
class Goods(models.Model):
    AVAILABILITY = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ManyToManyField(Category, blank=True, related_name='goods')
    furnishers = models.ManyToManyField(Profile, blank=True, related_name='furnishers')
    available_rn = models.CharField(max_length=20, choices=AVAILABILITY, default='available')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

# =========================
# 4. Purchase CourseSchedule
# =========================
class Purchase(models.Model):
    DELIVERY_TYPE = [
        ('not_needed', 'Not Needed'),
        ('standart', 'Standart'),
        ('express', 'Express'),
    ]
    list_of_goods = models.ManyToManyField(Goods, blank=True, related_name='list')
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, related_name='customer')
    consultant = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, related_name='consultant', null=True)
    delivery = models.CharField(max_length=20, choices=DELIVERY_TYPE, default='not_needed')
    date_of_purchase = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('customer', 'date_of_purchase', 'time')

    def __str__(self):
        return f"{self.customer} - {self.date_of_purchase} - {self.time}"