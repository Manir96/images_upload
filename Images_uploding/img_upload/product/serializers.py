from rest_framework import serializers
from product.models import Product

class ProductSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Product
        fields = ['name', 'product_image',]
































# from rest_framework import serializers
# from . models import Product


# class ProductSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     product_image = serializers.ImageField()
    
# def create(self, validated_data):
#     return Product.objects.create(validated_data)
    
# def update(self, instance, validated_data):
#     instance.name = validated_data.get('name', instance.name)
#     instance.product_image = validated_data.get('product_image', instance.email)
#     instance.save()
#     return instance
    
# # class ProductSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Product
# #         fields = '_all_'

# class SnippetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['name', 'product_image',]