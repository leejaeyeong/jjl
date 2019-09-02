from django.shortcuts import render
import sys
from .models import Home
from django.utils import timezone
import datetime
import math
# Create your views here.

def home(request) :
    return render(request,'home.html')

def total(request) :
    return render(request,'month_cal.html')

def totalList(request) :
    return throw(request)

def throw(request) :
    if request.method == 'POST':
        if request.POST['state'] == "right" :
            if request.POST['month'] == 12 :
                month = 1
            else : 
                month = int(request.POST['month']) + 1
        else :
            if request.POST['month'] == 1 : 
                month = 12 
            else :
                month = int(request.POST['month']) - 1
    else : 
        dt = datetime.datetime.now()
        month = dt.month

    totalH = 0
    totalM = 0
    homes = Home.objects.all().order_by('date').filter(date__month=month)
    #homes = Home.objects.all().order_by('date')
    for k in homes :
        totalH = totalH + k.hour
        totalM = totalM + k.minute
    
    totalH = totalH + totalM//60
    totalM = totalM%60
    return render(request,'totalList.html', {'homes': homes, 'totalH':totalH, 'totalM':totalM, 'month':month, 'salary': math.ceil(7770*(totalH+totalM/60))})

def calculate(request) :
    data = request.POST['data']
    data = data.split('\r\n')
    h_total = 0
    m_total = 0
    overCnt = 0

    for x in range(len(data)) :
        workList = data[x]
        if workList =="" :
            break
        else :
            workList = workList.split()
    
            if len(workList[1]) == 2 :
                h_start = int(workList[1][0])
            elif len(workList[1]) == 3 :
                h_start = int(workList[1][0:2])
    
            if len(workList[4]) == 2 :
                h_end = int(workList[4][0])
            elif len(workList[4]) == 3 :
                h_end = int(workList[4][0:2])
    
            h_total = h_total + h_end - h_start
            
            m_start =  int(workList[2][0:2])
            m_end = int(workList[5][0:2])
            
            if m_end < m_start :
                m_total = m_total + 60 + m_end - m_start
                overCnt = overCnt + 1
            else :
                m_total = m_total + m_end - m_start

    result = h_total - overCnt + m_total//60
    return render(request,'result.html', {'h_result': result , 'm_result': m_total%60 , 'pay': (result + m_total%60//60)*7800 })
    
def insert(request) :
    return render(request,'insert.html')

def insertTime(request) :
    dt = datetime.datetime.now()
    month = dt.month
    date = request.POST['date']
    stT = request.POST['startTime']
    edT = request.POST['endTime']
    
    home = Home()
    stT = stT + ":00"
    edT = edT + ":00"
    home.startH = stT
    home.endH = edT
    stT = stT.split(':')
    edT = edT.split(':')

    startH = int(stT[0])
    endH = int(edT[0])
    startM = int(stT[1])
    endM = int(edT[1])

    if startH > endH :
        endH = endH + 24 
    Hour = endH - startH

    if startM > endM :
        Hour = Hour - 1
        endM = endM + 60
    Minute = endM - startM

    home.hour = int(Hour)
    home.minute = int(Minute)
    home.date = date
    home.save()

    homes = Home.objects.order_by('date').filter(date__month=month)
    totalH = 0
    totalM = 0
    
    for k in homes :
        totalH = totalH + k.hour
        totalM = totalM + k.minute

    totalH = totalH + totalM//60
    totalM = totalM%60
    
    return render(request,'totalList.html', {'homes': homes, 'totalH': totalH, 'totalM': totalM, 'month':month, 'salary': math.ceil(7770*(totalH+totalM/60))})


def modify(request,home_id) :
    home = Home.objects.filter(id=home_id)
    return render(request,'modify.html', {'home' : home})
  
  
def modifyapplication(request,home_id) :
    dt = datetime.datetime.now()
    month = dt.month
    date = request.POST['date']
    stT = request.POST['startTime']
    edT = request.POST['endTime']
    
    home = Home.objects.filter(id=home_id)
    stT = stT + ":00"
    edT = edT + ":00"
    home.startH = stT
    home.endH = edT
    stT = stT.split(':')
    edT = edT.split(':')

    startH = int(stT[0])
    endH = int(edT[0])
    startM = int(stT[1])
    endM = int(edT[1])

    if startH > endH :
        endH = endH + 24 
    Hour = endH - startH

    if startM > endM :
        Hour = Hour - 1
        endM = endM + 60
    Minute = endM - startM

    home.update(hour = int(Hour))
    home.update(minute = int(Minute))
    home.update(date = date)
    
    homes = Home.objects.order_by('date').filter(date__month=month)
    totalH = 0
    totalM = 0
    for k in homes :
        totalH = totalH + k.hour
        totalM = totalM + k.minute
    
    totalH = totalH + totalM//60
    totalM = totalM%60
    return render(request,'totalList.html', {'homes': homes, 'totalH': totalH, 'totalM': totalM, 'month':month, 'salary': math.ceil(7770*(totalH+totalM/60))})
    #return redirect('/totalList/')
    