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


def home(request):
    return HttpResponse("Hello pcentra!")


# Handle creation of slug to be unique
def unique_slugify(new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = ''.join(random.choice(string.ascii_letters)
                       for x in range(10))
    qs_exists = URL.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = ''.join(random.choice(string.ascii_letters)
                           for x in range(10))

        return unique_slugify(new_slug=new_slug)
    return slug


class CreateShorterViewSet(APIView):
    def post(self, request):
        url = request.data['url']
        slug = unique_slugify(''.join(random.choice(string.ascii_letters)
                                      for x in range(10)))
        url_dict = {'url': url, 'slug': slug}
        serializer = URLSerializer(data=url_dict)
        if serializer.is_valid():
            serializer.save()
            # redirect to the full URL
            return redirect(url)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RedirectShorterViewSet(APIView):
    def get(self, request, short=None):
        if short:
            url = get_object_or_404(URL, slug=short)
            # hit counter for every short URL
            url.hit_counter += 1
            url.save()
            # redirect to the full URL
            return redirect(url.url)
