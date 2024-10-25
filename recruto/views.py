from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def say_hi(request: HttpRequest):
    try:
        name = request.GET['name']
        message = request.GET['message']
    except KeyError as e:
        print(e)
        return render(request, 'recruto/help.html', context={
            'error': True,
            'absent_name': str(e)[1:-1]
        })

    return render(request, 'recruto/index.html', context=locals())
