from django.http import HttpResponse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import DepositOptionSerializer, DepositProductSerializer, SavingProductSerializer, SavingOptionSerializer
from .models import DepositProducts, SavingProducts, DepositOptions, SavingOptions

def deposit(request):
    res = requests.get('https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth=72624f4493711e1a4b021f735bffa37e&topFinGrpNo=020000&pageNo=1')
    baselist = res.json()['result']['baseList']
    optionlist = res.json()['result']['optionList']

    for li in baselist:
        save_data = {
            'fin_prdt_cd': li.get('fin_prdt_cd'),
            'fin_co_no': li.get('fin_co_no'),
            'kor_co_nm': li.get('kor_co_nm'),
            'fin_prdt_nm': li.get('fin_prdt_nm'),
            'etc_note' : li.get('etc_note'),
            'join_deny' : li.get('join_deny'),
            'join_member' : li.get('join_member'),
            'join_way' : li.get('join_way'),
            'spcl_cnd' : li.get('spcl_cnd'),
            'mtrt_int': li.get('mtrt_int'),
        }

        serializer = DepositProductSerializer(data=save_data)
        if serializer.is_valid():
            serializer.save()

    for li in optionlist:
        save_data = {
            'product' : li.get('product'),
            'fin_prdt_cd' : li.get('fin_prdt_cd'),
            'intr_rate_type_nm' : li.get('intr_rate_type_nm'),
            'intr_rate' : li.get('intr_rate'),
            'intr_rate2' : li.get('intr_rate2'),
            'save_trm' : li.get('save_trm'),
        }

        serializer = DepositOptionSerializer(data = save_data)

        if serializer.is_valid(raise_exception=True):
            product = DepositProducts.objects.get(fin_prdt_cd = save_data.get('fin_prdt_cd'))
            serializer.save(product=product)

    return Response(serializer.data)

def savings(request):
    res = requests.get('https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth=72624f4493711e1a4b021f735bffa37e&topFinGrpNo=020000&pageNo=1')
    baselist = res.json()['result']['bas    eList']
    optionlist = res.json()['result']['optionList']


    for li in baselist:
        save_data = {
            'fin_prdt_cd': li.get('fin_prdt_cd'),
            'fin_co_no': li.get('fin_co_no'),
            'kor_co_nm': li.get('kor_co_nm'),
            'fin_prdt_nm': li.get('fin_prdt_nm'),
            'etc_note' : li.get('etc_note'),
            'join_deny' : li.get('join_deny'),
            'join_member' : li.get('join_member'),
            'join_way' : li.get('join_way'),
            'spcl_cnd' : li.get('spcl_cnd'),
            'mtrt_int': li.get('mtrt_int'),
        }

        serializer = SavingProductSerializer(data=save_data)
        if serializer.is_valid():
            serializer.save()

    for li in optionlist:
        save_data = {
            'product' : li.get('product'),
            'fin_prdt_cd' : li.get('fin_prdt_cd'),
            'intr_rate_type_nm' : li.get('intr_rate_type_nm'),
            'intr_rate' : li.get('intr_rate'),
            'intr_rate2' : li.get('intr_rate2'),
            'save_trm' : li.get('save_trm'),
            'rsrv_type_nm' : li.get('rsrv_type_nm'),
        }

        serializer = SavingOptionSerializer(data = save_data)

        if serializer.is_valid(raise_exception=True):
            product = SavingProducts.objects.get(fin_prdt_cd = save_data.get('fin_prdt_cd'))
            serializer.save(product=product)

    return Response(serializer.data)

@api_view(['GET'])
def deposit(request):
    deposit = DepositProducts.objects.all()
    serializer = DepositProductSerializer(deposit, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def depositOptions(request):
    deposit = DepositOptions.objects.all()
    serializer = DepositOptionSerializer(deposit, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Saving(request):
    deposit = SavingProducts.objects.all()
    serializer = SavingProductSerializer(deposit, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def SavingOption(request):
    deposit = SavingOptions.objects.all()
    serializer = SavingOptionSerializer(deposit, many=True)
    return Response(serializer.data)
