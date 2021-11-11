from django.shortcuts import render
from django.http import HttpResponse
from .serializers import URLSerializer
from .models import URL
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
import random
import string
from django.db.models import F


def home(request):
    return HttpResponse("Hello pcentra!")


# Handle creation of slug to be unique
def unique_slugify():
    slug = ''.join(random.choice(string.ascii_letters)
                   for x in range(10))
    qs_exists = URL.objects.select_for_update().filter(slug=slug).exists()
    first_exists = URL.objects.select_for_update().filter(id=1).exists()
    if first_exists:
        latest = URL.objects.order_by('id')[0]
    else:
        latest = 0
    while qs_exists:
        slug = "{key}{randstr}".format(
            key=latest.id + 1, randstr=''.join(random.choice(string.ascii_letters)
                                               for x in range(10)))
        qs_exists = URL.objects.filter(slug=slug).exists()
    return slug


class CreateShorterViewSet(APIView):
    def post(self, request):
        url = request.data['url']
        slug = unique_slugify()
        url_dict = {'url': url, 'slug': slug}
        serializer = URLSerializer(data=url_dict)
        if serializer.is_valid():
            serializer.save()
            # redirect to the full URL
            # return redirect(url)
            return Response({"status": "created successfully", "data": 'http://127.0.0.1:8000/s/'+slug}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RedirectShorterViewSet(APIView):
    def get(self, request, short=None):
        if short:
            url = get_object_or_404(URL, slug=short)
            # hit counter for every short URL
            url.hit_counter = F("hit_counter") + 1
            url.save(update_fields=["hit_counter"])
            # redirect to the full URL
            return redirect(url.url)
