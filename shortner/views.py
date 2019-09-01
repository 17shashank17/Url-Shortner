from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import URL

def encode(n):
    symbols = "abcdefghijklmnopqestuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890=+";
    r=''
    while n != 0:
        print(symbols[n%64])
        r+=str(symbols[n%64])
        n=n//64
    r=list(r)
    r.reverse()

    return ''.join(r)

def decode(s):
    symbols = "abcdefghijklmnopqestuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890=+";
    dict={}
    for i in range(64):
        dict[symbols[i]]=i
    # print(dict)
    t=0
    for c in s:
        t = t * 64 + dict[c]
    return t
    


def shorten(request):
    if request.method == "GET":
        return render(request, 'home.html')
    elif request.method == "POST" and request.POST.get('url') != '':
        url=URL()
        url.url=request.POST.get('url')
        print('url = ', url.url)
        url.save()
        t=encode(url.id)
        print(t)
        return HttpResponse(f'<a href="{url.url}">localhost:8000/r?q={t}</a>')
    else:
        return HttpResponse('invalid')

def redirect(request):
    if request.method == "GET" and request.GET.get('q') != '':
        url = URL.objects.filter(id=decode(request.GET.get('q')))

        if len(url) == 0:
            return HttpResponse("nothing found")
        else:
            return HttpResponseRedirect(url[0].url)