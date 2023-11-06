from django.shortcuts import get_object_or_404, render
from .models import Product,Reviw
from .serializer import ProductSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Avg
# Create your views here.

@api_view(['GET'])
def get_products(request):
    filter = ProductFilter(request.GET  ,queryset =Product.objects.all().order_by('id'))
    count= filter.qs.count()
    resPerPage = 2
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    queryset = paginator.paginate_queryset(filter.qs, request)
    serializer = ProductSerializer(queryset , many = True)
    return Response({
        'count':count,
        'resPerPage':resPerPage,

        'products': serializer.data
        })


@api_view(['GET'])
def get_product(request , pk):
    product  = get_object_or_404(Product , pk = pk)
    serializer = ProductSerializer (product)
    return Response({'product' : serializer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data = data)
    if serializer.is_valid():
        serializer.save(user = request.user)
        return Response({'product': serializer.data})
    return Response(serializer.errors)

    # data =request.data
    # serializer = ProductSerializer(data , many=False)
    # if serializer.is_valid():
    #     product = Product.objects.create(**data , user= request.user)
    #     res = ProductSerializer(product , many = False)
    #     return Response(res.data)
    # return Response(serializer.errors)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response({'details ':'you can`t edit this product'})
    
    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.category = request.data['category']
    product.brand = request.data['brand']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    product.save()

    serializer = ProductSerializer(product, many=False)

    return Response({ "product": serializer.data })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_product(request, pk):
    
    product = get_object_or_404(Product , id = pk)
    if product.user != request.user:
        return Response ({'detalis': 'you can`t delete this product'})
    
    product.delete()
    return Response({'details':'product deleted'}, status= status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request , pk):
    user = request.user
    product = get_object_or_404(Product,id = pk)
    data  = request.data

    review = product.reviews.filter(user= user)
    if data['rating'] <= 0 or data['rating'] > 5 :
        return Response({'datails' : "you should give valid ration betwwen 1 an 5"})
    elif review.exists():
        new_review = {'rating' : data['rating'] , 'comment':data['comment']}
        review.update(**new_review) 
        rating= product.reviews.aggregate(avg_ratings =Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        ser = ProductSerializer(product)
        return Response({'details':'review updated'})
    else:
        Reviw.objects.create(
            user = user ,
            product = product,
            rating = data['rating'],
            comment = data['comment']
        )
        rating= product.reviews.aggregate(avg_ratings =Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details':'review saved'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    user =request.user
    product = get_object_or_404(Product , id =pk)
    review = product.reviews.filter(user =user)
    if review.exists():
        review.delete()
        rating= product.reviews.aggregate(avg_ratings =Avg('rating'))
        print('rating',rating)
        if rating['avg_ratings'] is None:
            rating['avg_ratings'] =0

        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details':'review deleted'})
    else:
        return Response ({'details':'review not found'})
