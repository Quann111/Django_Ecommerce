from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    total_items = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user} {self.total_items} "

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} {self.product}{self.time} "

# @receiver(pre_save, sender=CartItem)
# def correct_price(sender, instance, **kwargs):
#     cart_item =kwargs['instance']
    
#     # tính tiên 1 giỏ hàng
#     price_of_product = Product.objects.get(id=cart_item.product.id)
#     cart_item.price = cart_item.quantity * float(price_of_product.Price)
    
#     # # truyền dữ liệu về bảng CartItem
#     # total_cart_items = CartItem.objects.filter(user=cart_item.user)
#     # cart = Cart.objects.get(id=cart_item.cart.id)
#     # cart.total_price = cart_item.price
    
#     # #truyền dữ liệu vào bảng Cart số sản phẩm đã mua
#     # cart_items_count = CartItem.objects.filter(cart=cart).count()
#     # cart.total_items = cart_items_count
#     # cart.save()


@receiver(pre_save, sender=CartItem)
def correct_price(sender, instance, **kwargs):
    cart_item = instance

    # Tính toán giá tiền cho mỗi CartItem
    price_of_product = Product.objects.get(id=cart_item.product.id)
    cart_item.price = cart_item.quantity * float(price_of_product.Price)

    # Truy vấn tất cả các CartItem của người dùng
    cart_items = CartItem.objects.filter(user=cart_item.user)

    total_price = sum(item.price for item in cart_items)
    # Lấy hoặc tạo một Cart cho người dùng
    cart, _ = Cart.objects.get_or_create(user=cart_item.user, ordered=False)

    # Cập nhật total_price của Cart
    cart.total_price = total_price
    cart.save()
    
# @receiver(pre_save, sender=CartItem)
# def update_total_items(sender, instance, **kwargs):
#     cart_item = instance

#     # Lấy tất cả các CartItem của người dùng
#     cart_items = CartItem.objects.filter(user=cart_item.user)

#     # Tính tổng quantity
#     total_items = cart_items.aggregate(total_items=models.Sum('quantity'))['total_items']

#     # Lấy hoặc tạo một Cart cho người dùng
#     cart, _ = Cart.objects.get_or_create(user=cart_item.user, ordered=False)

#     # Cập nhật total_items của Cart
#     cart.total_items = total_items
#     cart.save()
    
    