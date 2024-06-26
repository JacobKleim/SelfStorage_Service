from django.shortcuts import render

def view_products(request):
    boxes =[
        {
            'name':'Новосибирск',
            'address':'ул. Лермонтова д.15_тест',
        },
        {
            'name':'Иркутск',
            'address':'ул. Пушкина д.17_тест',
        },
    ]

    # logic

    return render(request, template_name="boxes_t.html", context={'boxes': boxes})

# Create your views here.
