from rest_framework import serializers
from .models import Category,Product,Cart,CartItem

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','name','product_count']
    def get_product_count(self,obj):
        return obj.products.count()
class ProductSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.SerializerMethodField()
    Category_name = serializers.CharField(source = 'catergory.name',read_only=True)
    
    class Meta:
        model = Product
        fields = ['id','name','description','price','stock','is_in_stock','category_name','image']
    def get_is_in_stock(self,obj):
        return obj.stock > 0
    
class CartItemSeializer(serializers.ModelSerializer):
    Product=ProductSerializer(read_only = True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','subtotal']
    def get_subtotal(self,obj):
        return obj.product.price * obj.quantity
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSeializer(many = True,read_only = True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields= ['id','user','items','total_price']
    def get_total_price(self,obj):
        return sum(item.product.price*item.quantity for item in obj.items.all())

    