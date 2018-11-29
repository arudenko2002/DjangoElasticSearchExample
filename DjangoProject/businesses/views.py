from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
import json

def index(request):
    route = request.get_full_path().split("/")[1]
    if 'businesses' != route:
        return HttpResponse('{"code":404,"message":{"error":"Not found"}}')
    page_value=0
    if "page" in request.GET:
        page = request.GET["page"]
        try:
            page_value = int(page)
            if page_value < 0:
                return HttpResponse('{"code":400,"message":{"error","Invalid request"}}')
        except ValueError:
            return HttpResponse('{"code":400,"message":{"error","Invalid request"}}')
        
    size_value=10
    if "size" in request.GET:
        size = request.GET["size"]
        try:
            size_value = int(size)
            if size_value < 0:
                return HttpResponse('{"code":400,"message":{"error","Invalid request"}}')
        except ValueError:
            return HttpResponse('{"code":400,"message":{"error","Invalid request"}}')

    q=""
    if "q" in request.GET:
        q = request.GET["q"]
        
    result = receiveTotalCheckins(q,page_value,size_value)
    return HttpResponse(result)

def requestURL(q,page_value,size_value):
        request=""
        if len(q)>0:
            request=getIndexContentQueue() % (page_value*size_value,size_value,q)
            #print(request)
        else:
            request=getIndexContent() % (page_value*size_value,size_value)
            #print(request)
        host="ec2-54-162-18-40.compute-1.amazonaws.com"
        port=9200
        index="alexey2_index"
        url="%s:%s/%s/business/_search" % ("http://"+host,port,index)
        return requests.request(method='get', url=url,data=request).text
        
def getIndexContentQueue():
        request='{ \
            "from" : %s, "size" : %s, \
            "_source": [ "name", "business_id","full_address","total_checkins" ], \
            "query":{ \
                "multi_match" : { \
                "query":      "%s", \
                "type":       "best_fields", \
                "fields":     [ "name", "full_address" ], \
                "tie_breaker": 0.5 \
                } \
            }, \
            "aggs": { \
                "total": { \
                    "sum": { \
                        "field": "total_checkins" \
                    } \
                } \
            } \
            ,"sort": [ \
                 { "_score": { "order": "desc" }}, \
                { "total_checkins": { "order": "desc"} } \
            ] \
        }'
        return request
    
def getIndexContent():
        request='{ \
            "from" : %s, "size" : %s, \
            "_source": [ "name", "business_id","full_address","total_checkins" ], \
            "query":{ \
               "match_all": {} \
            }, \
            "aggs": { \
                "total": { \
                    "sum": { \
                        "field": "total_checkins" \
                    } \
                } \
            } \
            ,"sort": [ \
                 { "_score": { "order": "desc" }}, \
                { "total_checkins": { "order": "desc"} } \
            ] \
        }'
        return request
    
def getOutput(datastr):
        result={}
        data = json.loads(datastr)
        result["total"]=int(data['aggregations']['total']['value'])
        result['businesses']=[]
        for ii in data['hits']['hits']:
            result['businesses'].append(ii['_source'])
        return str(result)
    
def receiveTotalCheckins(q="",page_value=0,size_value=10):

        datastr = requestURL(q,page_value,size_value)
        #print(datastr)
        if 'error' in datastr:
            print("Error response="+datastr)
            return datastr
        
        data = getOutput(datastr)
        return data