from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db.models import Count

from .models import UserProfile, Storehouse, Requestion


def view_products(request):
    storehouses = Storehouse.objects.prefetch_related('images').annotate(
        boxes_count=Count('boxes'))
    print(storehouses)
    store_serialized = []
    for storehouse in storehouses:
        store_serialized.append({
            "id": f"{storehouse.id}",
            "city": storehouse.city,
            "address": storehouse.address,
            "description": storehouse.description,
            "road": storehouse.road,
            "contact_phone": storehouse.contact_phone,
            "temperature": storehouse.temperature,
            "boxes_count": storehouse.boxes_count,
            "images": [image.img.url for image in storehouse.images.all()]
        })

    return render(request, template_name="boxes.html",
                  context={'storehouses': store_serialized})


def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('EMAIL_CREATE')
        password = request.POST.get('PASSWORD_CREATE')
        password_confirm = request.POST.get('PASSWORD_CONFIRM')

        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают')
            return redirect('start_page')

        try:
            user = User.objects.create_user(
                username=email, email=email, password=password)
            user.save()

            user_profile = UserProfile.objects.create(
                user=user, phone_number='', full_name='')
            user_profile.save()
            messages.success(request, 'Пользователь успешно создан')
            return redirect('start_page')
        except Exception as e:
            messages.error(request, f'Ошибка при создании пользователя: {e}')
            return render(
                request, 'index.html',
                {'error_message': 'Ошибка при создании пользователя'},
                status=400)

    return render(request, 'index.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('EMAIL')
        password = request.POST.get('PASSWORD')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('my_rent')
        else:
            messages.error(request, 'Неверный email или пароль.')
            return render(request, 'index.html',
                          {'error_message': 'Неверный email или пароль'},
                          status=400)

    return render(request, 'index.html')


def my_rent(request):
    user_a = UserProfile.objects.filter(user=request.user)
    user = user_a[0]
    user_rents = (
        Requestion.objects.select_related("box", "box__storehouse")
        .filter(user=user)
        .order_by("status")
    )
    user_rent = []
    for rent in user_rents:
        user_rent.append({
            "full_name": rent.user.full_name,
            "email": rent.user.user.email,
            "password": rent.user.user.password,
            "phone_number": rent.user.phone_number,
            "box": f"{rent.box.storehouse.city} {rent.box.storehouse.address}",
            "box_number": rent.box.box_number,
            "rental_period": f"{rent.created_at} - {rent.expiration_at}",
            "price": rent.price,
            "status": rent.status,
        })








    return render(request, 'my-rent.html', context={'user':user_rent[0]})
