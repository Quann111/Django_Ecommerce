from django.db import models
# Create your models here.
class Category(models.Model):
    Category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200 , blank = True)
    
    def save (self ,*args, **kwargs):
        self.slug = models.SlugField(self.Category_name)
        super(Category, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.Category_name}"

class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.variant_name

class ColorVariant(models.Model):
    color_name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.color_name} {self.color_code}"

class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.size_name
    
class Product(models.Model):
    
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Product_name = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='static/products')
    Price = models.CharField(max_length=20)
    Description = models.TextField()
    Stock = models.IntegerField(default=100)
    
    Quantity_type = models.ForeignKey(QuantityVariant, blank=True, null=True, on_delete=models.PROTECT)
    Color_type = models.ForeignKey(ColorVariant, blank=True, null=True, on_delete=models.PROTECT)
    Size_type = models.ForeignKey(SizeVariant, blank=True, null=True, on_delete=models.PROTECT)

    
    def __str__(self):
        return f"{self.Product_name} "        

class ProductImage (models.Model):
    product = models.ForeignKey(Product , on_delete= models.PROTECT)
    image = models.ImageField(upload_to='static/products')
                   