from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.models import User
from .models import Profile, Category, Goods, Purchase
from datetime import datetime


# ========================
# Profile Endpoints
# ========================

@require_GET
def search_profile_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)

    profiles = Profile.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query) | 
        Q(user__username__icontains=query) | Q(role__icontains=query)
    ).distinct()
    
    result = []
    for profile in profiles:
        result.append({
            "id": profile.id,
            "username": profile.user.username,
            "role": profile.role,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "middle_name": profile.middle_name,
            "phone": profile.phone,
        })
    return JsonResponse({"profiles": result})

@require_GET
def list_profiles_view(request):
    profiles = Profile.objects.all()
    result = []
    for profile in profiles:
        result.append({
            "id": profile.id,
            "username": profile.user.username,
            "role": profile.role,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "middle_name": profile.middle_name,
            "phone": profile.phone,
        })
    return JsonResponse({"profiles": result})

@csrf_exempt
@require_POST
def create_profile_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    phone = data.get("phone", "")

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    middle_name = data.get("middle_name", "")
    
    if not (username and password and role and first_name and last_name and phone):
        return JsonResponse(
            {"error": "Missing required fields (username, password, role, first_name, last_name)"},
            status=400
        )
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)
    profile = Profile.objects.create(
        user=user,
        role=role,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name
    )
    
    return JsonResponse({
        "id": profile.id,
        "username": profile.user.username,
        "role": profile.role,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "middle_name": profile.middle_name,
        "phone": profile.phone,
    }, status=201)

# ========================
# Category Endpoints
# ========================

@require_GET
def search_category_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)
    categories = Category.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).distinct()
    result = []
    for cat in categories:
        result.append({
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
        })
    return JsonResponse({"categories": result})

@require_GET
def list_categories_view(request):
    categories = Category.objects.all()
    result = []
    for cat in categories:
        result.append({
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
        })
    return JsonResponse({"categories": result})

@csrf_exempt
@require_POST
def create_category_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    name = data.get("name")
    description = data.get("description", "")
    if not name:
        return JsonResponse({"error": "Missing required field: name"}, status=400)
    if Category.objects.filter(name=name).exists():
        return JsonResponse({"error": "Category already exists"}, status=400)
    category = Category.objects.create(name=name, description=description)
    return JsonResponse({
        "id": category.id,
        "name": category.name,
        "description": category.description,
    }, status=201)

# ========================
# Goods Endpoints
# ========================

@require_GET
def search_goods_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)
    goods = Goods.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ).distinct()
    result = []
    for g in goods:
        result.append({
            "id": g.id,
            "title": g.title,
            "description": g.description,
            "category": str(list(g.category.all())),
            "price": g.price,
        })
    return JsonResponse({"goods": result})

@require_GET
def list_goods_view(request):
    goods = Goods.objects.all()
    result = []
    for g in goods:
        result.append({
            "id": g.id,
            "title": g.title,
            "description": g.description,
            "category": str(list(g.category.all())),
            "price": g.price,
        })
    return JsonResponse({"goods": result})

@csrf_exempt
@require_POST
def create_goods_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    title = data.get("title")
    description = data.get("description")
    category_ids = data.get("category_ids")
    price = data.get("price")
    
    if not (title and description and category_ids and price):
        return JsonResponse({"error": "Missing required fields (title, description, category, price)"}, status=400)
    if Goods.objects.filter(title=title).exists():
        return JsonResponse({"error": "Goods already exist"}, status=400)
    
    try:
        categories = []
        for id in category_ids:
            categories.append(Category.objects.get(id=id))
    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=400)
    
    g = Goods.objects.create(
        title=title,
        description=description,
        category=categories,
        price=price,
    )
    
    return JsonResponse({
        "id": g.id,
        "title": g.title,
        "description": g.description,
        "category": g.category,
        "price": g.price,
    }, status=201)

# ========================
# Purchase Endpoints
# ========================

@require_GET
def search_purchase_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)
    purchases = Purchase.objects.filter(
        Q(date_of_purchase__icontains=query) | Q(time__icontains=query)
    ).distinct()
    result = []
    for purch in purchases:
        result.append({
            "id": purch.id,
            "list_of_goods": str(list(purch.list_of_goods.all())),
            "customer": purch.customer,
            "date_of_purchase": purch.date_of_purchase,
            "time": purch.time.strftime("%H:%M:%S"),
            "consultant": purch.consultant if purch.consultant else None,
            "delivery": purch.delivery,
        })
    return JsonResponse({"purchases": result})

@require_GET
def list_purchase_view(request):
    purchases = Purchase.objects.all()
    result = []
    for purch in purchases:
        result.append({
            "id": purch.id,
            "list_of_goods": str(list(purch.list_of_goods.all())),
            "customer": str(purch.customer),
            "date_of_purchase": purch.date_of_purchase,
            "time": purch.time.strftime("%H:%M:%S"),
            "consultant": str(purch.consultant) if purch.consultant else None,
            "delivery": purch.delivery,
        })
    return JsonResponse({"purchases": result})

@csrf_exempt
@require_POST
def create_purchase_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    delivery = data.get("delivery")
    customer_id = data.get("customer_id")
    list_of_goods_ids = data.get("list_of_goods_ids")
    
    # Проверяем наличие обязательных полей
    if not (delivery and customer_id):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    consultant = None
    consultant_id = int(data.get("consultant_id"))
    if consultant_id:
        try:
            consultant_id = int(consultant_id)
            consultant = Profile.objects.get(id=consultant_id)
        except (ValueError, Profile.DoesNotExist):
            return JsonResponse({"error": "Consultant not found or invalid ID"}, status=400)
    
    try:
        customer = Profile.objects.get(id=customer_id)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Customer not found"}, status=400)

    try:
        list_of_goods = []
        for id in list_of_goods_ids:
            list_of_goods.append(Goods.objects.get(id=int(id)))
    except Goods.DoesNotExist:
        return JsonResponse({"error": "Good not found"}, status=400)
    
    # Создаем запись расписания
    purchase = Purchase.objects.create(
        list_of_goods=list_of_goods,
        customer=customer,
        consultant=consultant,
        delivery=delivery
    )
    
    return JsonResponse({
        "id": purchase.id,
        "list_of_goods": str(list(purchase.list_of_goods.all())),
        "customer": str(purchase.customer),
        "date_of_purchase": purchase.date_of_purchase,
        "time": purchase.time.strftime("%H:%M:%S"),
        "consultant": str(purchase.consultant) if purchase.consultant else None,
        "delivery": purchase.delivery,
    }, status=201)