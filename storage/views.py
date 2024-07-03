from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from .models import Box, Requestion, Storehouse, UserProfile

def count(request):
    print(request.GET['EMAIL1'])
    user_mail = request.GET['EMAIL1']
    Requestion.objects.create(
        mail=user_mail,
        status='SD'
    )
    return HttpResponse('<h1>Заяка отправлена, с Вами свяжутся</h1>')


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
            "images": [image.img.url for image in storehouse.images.all()],
            #"boxes_n": [i.box_number for i in storehouse.boxes.all()],
        })
    print(store_serialized)

    boxes_all = Box.objects.all()
    boxes = []
    for box in boxes_all:
        boxes.append({
            "box_number": box.box_number,
            "box_floor": box.floor,
            "box_height": box.height,
            "box_length": box.length,
            "box_width": box.width,
            "box_price": box.price,
        })

    return render(request, template_name="boxes.html", context={
                      'storehouses': store_serialized,
                      'boxes': boxes,
                  })


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
            user_profile = UserProfile.objects.filter(user=user).first()
            if user_profile:
                return redirect('my_rent', user_id=user_profile.user_id)
        else:
            messages.error(request, 'Неверный email или пароль.')
            return render(request, 'index.html',
                          {'error_message': 'Неверный email или пароль'},
                          status=400)

    return render(request, 'index.html')


def my_rent(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    form = []
    boxes = []
    user_rents = (
        Requestion.objects.select_related("box", "box__storehouse")
        .filter(user=user_profile)
        .order_by("status")
    )

    if not user_rents:
        form.append({
            "email": user_profile.user.email,
            "password": user_profile.user.password,
            "full_name": user_profile.full_name,
            "phone_number": user_profile.phone_number,
        })
    else:
        for rent in user_rents:
            form.append({
                "full_name": rent.user.full_name,
                "email": rent.user.user.email,
                "password": rent.user.user.password,
                "phone_number": rent.user.phone_number,
            })
            boxes.append({
                "box": f"{rent.box.storehouse.city}"
                       f"{rent.box.storehouse.address}",
                "box_number": rent.box.box_number,
                "rental_period": f"{rent.created_at} - {rent.expiration_at}",
                "price": rent.price,
                "status": rent.status,
            })

    return render(request, 'my_rent.html', context={
        'users': form,
        'boxes_rent': boxes,
    })
