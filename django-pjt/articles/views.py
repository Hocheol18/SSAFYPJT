from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleListSerializer, ArticleSerializer
from .models import Article

import requests
from datetime import datetime


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        print(serializer.data)
        return Response(serializer.data)

@api_view(['POST'])
def exchange(request, article_pk1, article_pk2, article_much1):
    now_time = datetime.now()
    exchange = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=tMkJFHpFPPdc4cSKbv448Q6CM0fnGqSY&searchdate={now_time.year}{now_time.month}{now_time.day-3}&data=AP01'
    response = requests.get(exchange)
    data = response.json()

    country = ['미국 달러', '유로', '위안화', '일본 옌', '한국 원']

    box = {}
    res = {}

    ans = 0
    for i in data:
        if i['cur_nm'] == country[article_pk1]:
            if float(i['tts'].replace(",", "")) == 0.0 or float(i['ttb'].replace(",", "")) == 0.0:
                number = 1
            else:
                number = float(i['tts'].replace(",", ""))
            box[f'{article_pk1}'] = float(article_much1)*number
        elif i['cur_nm'] == country[article_pk2]:
            if float(i['tts'].replace(",", "")) == 0.0 or float(i['ttb'].replace(",", "")) == 0.0:
                number = 1
            else:
                number = float(i['ttb'].replace(",", ""))
            box[f'{article_pk2}'] = number
    print(box)
    ans = box[f'{article_pk1}']/box[f'{article_pk2}']
    if article_pk1 == 3:
        ans /= 100
            
    res = {'country': country[article_pk1], 'price': round(ans,2)}

    return JsonResponse(res, status=status.HTTP_200_OK)