# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    arg1=""
    if "p" in request.GET:
        arg1 = request.GET["p"]
    arg2=""
    if "q" in request.GET:
        arg2 = request.GET["q"]
        
    result = [{"aa":"11","bb":"22","cc":"33","dd":"44","ee":"55"},{"aa":"11","bb":"22","cc":"33","dd":"44","ee":"55"},{"aa":"11","bb":"22","cc":"33","dd":"44","ee":"55"}]
    header="<h><B>Head of the Table: "+arg1+":"+arg2+"</B></h>"
    style ="<style>" \
      "table {" \
      " border-collapse: collapse;" \
      "}" \
      "th, td {" \
      " border: 1px solid orange;" \
      " padding: 10px;" \
      " text-align: left;" \
      "}" \
      "</style>" 
  
    title = "<table>"   \
      "<tr>" \
      "  <th>AAA</th>" \
      "  <th>BBB</th>" \
      "  <th>CCC</th>" \
      "  <th>DDD</th>" \
      "  <th>EEE</th>" \
      "</tr>"
    body=""
    for line in result:
      body = body +"<tr>"
      #for el in line:
      body = body + "<td>"+line["aa"]+"</td>" + "<td>"+line["bb"]+"</td>" + "<td>"+line["cc"]+"</td>" + "<td>"+line["dd"]+"</td>" + "<td>"+line["ee"]+"</td>"
      body = body + "</tr>" 
    body = body + "</table>"
    #return HttpResponse("Hello, world. You're at the elastic search index.")
    return HttpResponse(header+style + title +body)