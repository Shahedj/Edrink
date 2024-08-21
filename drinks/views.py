from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render




@api_view(['GET', 'POST']) #descibe functionality
def drink_list(request):
    if request.method == 'GET':
    #get all the drinks 
        drinks = Drink.objects.all()
    #serialize them
        serializer = DrinkSerializer(drinks, many=True)
    #return json
        #return JsonResponse({'drinks':serializer.data})
        return Response(serializer.data)

    
    if request.method == 'POST': #add a drink into the database
          serializer = DrinkSerializer(data = request.data)
          if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
          
#get info about a drink, update and delete 
@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id):
     
     try:
        drink = Drink.objects.get(pk=id)
     except Drink.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)
     if request.method == 'GET':
           serializer = DrinkSerializer(drink)
           return Response(serializer.data)
     
     elif request.method == 'PUT':
           serializer = DrinkSerializer(drink, data=request.data)
           if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
     elif request.method == 'DELETE':
          drink.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
     


     #return HttpResponseRedirect('/drinks') 


def homepage(request):
     return render(request, "HomePage.html")
     

def listMenu(request):
    search = request.GET.get("search", "")
    if search:
        list = Drink.objects.filter(name__icontains=search)
    else:
        list = Drink.objects.all()
    
    count = list.count()
    return render(request, "ListMenu.html", {"list": list, "count": count, "search": search})


def drinkDetail(request, id):
    # Retrieve the existing drink object or return 404 if not found
    drink = get_object_or_404(Drink, pk=id)
    
    # Handle the form submission
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        image = request.FILES.get('image') if request.FILES.get('image') else drink.image

        # Validate that the necessary fields are present
        if name and description and cost:
            # Update the drink object with new data
            drink.name = name
            drink.description = description
            drink.cost = cost
            drink.image = image
            drink.save()
            return HttpResponseRedirect("/list")
    else:
        # If it's a GET request, just render the form with the current drink data
        return render(request, "DrinkDetail.html", {"data": drink})


#SAVE INTO DATABASE 
def newDrink(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        image = request.FILES.get('image')  # Use request.FILES for file uploads

        if name and description and cost and image:
            drink = Drink(name=name, description=description, cost=cost, image=image)
            drink.save()
            return HttpResponseRedirect("/list")
        else:
            # Handle the case where not all required fields are provided
            return render(request, "AddDrink.html", {"error": "All fields are required."})
    else:
        # Render an empty form for GET requests
        return render(request, "AddDrink.html")



def delete(request, id):
     try:
          deleteDrink = Drink.objects.get(pk=id)
     except:
          raise Http404("Drink does not exist.")
     deleteDrink.delete()
     return  HttpResponseRedirect("/list")