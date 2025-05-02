from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def profile_view(request):
    if request.method == 'GET':
        return JsonResponse({"username": "fake_sad_alex", "type": "customer"})
    elif request.method == 'POST':
        return JsonResponse({"status": "profile updated"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def goods_list_view(request):
    if request.method == 'GET':
        return JsonResponse({
            "courses": [
                {"id": 1, "title": "Circle table"},
                {"id": 2, "title": "Plastic Chair"},
                {"id": 3, "title": "Wood chair"},
                {"id": 4, "title": "Double bed"},
                {"id": 5, "title": "Simple bed"},
            ]
        })
    elif request.method == 'POST':
        return JsonResponse({"status": "goods list updated"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def categories_list_view(request):
    if request.method == 'GET':
        return JsonResponse({
            "categories": [
                {"id": 1, "name": "Chairs"},
                {"id": 2, "name": "Beds"},
                {"id": 3, "name": "Tables"},
                {"id": 4, "name": "Armchairs"},
                {"id": 5, "name": "Sofas"},
            ]
        })
    elif request.method == 'POST':
        return JsonResponse({"status": "categories updated"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
