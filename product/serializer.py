from rest_framework import serializers
from .models import Product,Reviw

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Reviw
        fields = '__all__'






class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(method_name= 'get_review' ,read_only = True)
    class Meta:
        model = Product
        fields = ('id','name','description','price','prand','category','ratings','stock','user','createdAt','reviews')

        extra_kwargs ={
            "name" : {'required':True , 'allow_blank':True},
            "description" : {'required':True , 'allow_blank':True}
        }

    def get_review(self,obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews  , many = True)
        return serializer.data