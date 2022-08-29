#TO BUILD API METHODS
from django.shortcuts import render

#allow other domains to access api methods
from django.views.decorators.csrf import csrf_exempt

#JSON data format parser and response
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

# importing created models + serializer classes
from ProductsApp.models import Products
from ProductsApp.serializers import ProductSerializer


from django.core.files.storage import default_storage

@csrf_exempt #this removes the need for csrf tokens, 
#meaning requests can come from other domains besides just your website 

# build product api(CRUD operations), id = 0 as default (used for item deletion)
def productApi(request, id=0):
    #this is for retrieving all data from db
    if request.method == 'GET':
        products = Products.objects.all()
        # many= true tells serializer we may have <1 items
        products_serializer = ProductSerializer(products, many= True)
        #safe =false means if there are issues doing this, we are fine still
        return JsonResponse(products_serializer.data, safe =False)

    # this is for addding entries to db
    elif request.method == 'POST':
        #change product_data format to data that's easy to work with
        product_data = JSONParser().parse(request)
        products_serializer=ProductSerializer(data = product_data)
        if products_serializer.is_valid():
            products_serializer.save()
            return JsonResponse("Added Product to DB Successfully", safe = False)
        return JsonResponse("Failed to Add Product", safe = False)

    #this is for updating entries in db
    elif request.method == 'PUT':
        product_data= JSONParser().parse(request)
        # find existing record via product id
        product = Products.objects.get(ProductID = product_data['ProductID'])
        products_serializer = ProductSerializer(product, data = product_data) # update with new vals
        if products_serializer.is_valid():
            products_serializer.save()
            return JsonResponse("Updated Product in DB Successfully", safe = False)
        return JsonResponse("Failed to Update Product", safe = False)
    #Delete 
    elif request.method == 'DELETE':
        product = Products.objects.get(ProductID = id)
        product.delete()
        return JsonResponse("Product Deleted successfully", safe=False)
    #Testing: COUNT Entries in Database
    elif request.method == 'COUNT':
        num = Products.objects.count()
        return num
 
@csrf_exempt
def SaveFile(request):
    file = request.FILES['file']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe = False)

