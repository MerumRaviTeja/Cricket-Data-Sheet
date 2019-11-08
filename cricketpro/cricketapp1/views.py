from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse,HttpResponse
from pprint import pprint
from pymongo import MongoClient
import json
from datetime import timedelta,datetime
client=MongoClient()
db=client['cricket']

@api_view(['GET'])
def get_one(request,player_id):
    collection=db['players']
    data = collection.find_one({"player_id":player_id},{"_id":0})
    return JsonResponse(data,safe=False)

@api_view(['GET'])
def get_first(request):
    collection=db['players']
    data = collection.find_one({},{"_id":0})
    return JsonResponse(data,safe=False)

@api_view(['GET'])
def get_particular_column(request):
    collection=db['players']
    data=collection.find({},{"_id":0},{"players_name":1})
    return JsonResponse(data,safe=False)

@api_view(['GET'])
def get_last(request):
    collection=db['players']
    data1=collection.find({},{"_id":0}).sort({"$natural":-1}).limit(1)
    li=list(data1)
    return JsonResponse(li,safe=False)

@api_view(['GET'])
def get_countrywise_sum(request):
    collection=db['players']
    data=collection.aggregate([{"$group":{"_id":"$country","count":{"$sum":1}}}])
    li=list(data)
    return JsonResponse(li,safe=False)


@api_view(['GET'])
def get_pname_capkeep(request):
    collection=db['players']
    data=collection.find({"is_keeper":True,"is_captain":True},{"_id":0})
    li=list(data)
    return JsonResponse(li,safe=False)


@api_view(['GET'])
def get_captain_name(requet):
    collection=db['players']
    data=collection.aggregate([{'$match':{'is_captain':True}},{'$group':
        {'_id':'$country','players':{'$addToSet':'$player_name'}}}])
    k=[]
    for d in data:
        d.pop("_id")
        k.append(d)
    return JsonResponse(k,safe=False)

@api_view(['GET'])
def get_rhand_country(request):
    collection=db['players']
    data=collection.aggregate([{'$match':{'batting_hand':"Right_Hand"}},{'$group':
        {'_id':'$country','players':{'$addToSet':'$player_name'}}}])
    k=[]
    for d in data:
        d.pop("_id")
        k.append(d)
    return JsonResponse(k,safe=False)

@api_view(['GET'])
def get_pdob(request):
    collection=db['players']
    from_date=datetime(1970,1,1,0,1)
    to_date=datetime(1971,12,31,0,0)
    cursor=collection.find({"dob":{"$gte":from_date,"$lt":to_date}},{"_id":0})
    data=list(cursor)
    return JsonResponse(data,safe=False)
    
@api_view(['GET'])
def get_age_range(request):
    collection=db['players']
    dt=datetime.today()
    d1=timedelta(days=365*35)
    d2=timedelta(days=365*40)
    max=dt-d1
    min=dt-d2
    data=collection.find({"dob":{"$gte":min,"$lt":max}},{"_id":0})
    li=list(data)
    return JsonResponse(li,safe=False)



def get_age(request):
    collection=db['employ']
    dt=datetime.today()
    d1=timedelta(days=365*60)
    d2=timedelta(days=365*61)
    min=(dt-d2)
    max=(dt-d1)
    cursor=collection.find({"birth_date":{"$gte":min,"$lt":max}})
    data=list(cursor)
    return JsonResponse(data,safe=False)
    

@api_view(['GET'])
def insert_new(request):
    collection=db['players']
    before=collection.find().count()
    data=collection.insert_one({"player_id":"001",
        "player_name":"k.k.pal","dob":"1971-11-14T00:00:00",
        "batting_hand":"Right_Hand","country":"India",
        "is_umpire":"true","is_keeper":"false","is_captain":"false"})
    after=collection.find().count()
    li=[before,after]
    return JsonResponse(li,safe=False)

@api_view(['GET'])
def update_one(request):
    collection=db['players']
    data=collection.update({"player_name" :"MS Dhoni"},{"$set": { "is_captain" : "false"}})
    return JsonResponse(data,safe=True)

@api_view(['GET'])
def delete_one(request):
    collection=db['players']
    data=collection.remove({"$or":[{"player_name":"k.k.pal"},{"player_id":"001"}]})
    #return HttpResponse("successfully deleted records")
    return JsonResponse(data,safe=True)

def delete_many(request):
    collection=db['players']
    data=collection.deletemany({"$or":[{"player_name":"k.k.pal"},{"player_id":"001"}]})
    li=list(data)
    return JsonResponse(li,safe=True)

