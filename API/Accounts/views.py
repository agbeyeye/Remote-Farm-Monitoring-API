from django.shortcuts import render
from FARM_API.models import Farm,Device,DeviceData
from django.http import JsonResponse, response,HttpResponse
def homeView(request):
    # farm = Farm.objects.all()[0]
    # dic={}
    # devices = Device.objects.filter(farm = farm )
    # data = DeviceData.objects.all()
    template = "index.html"
    return render(request, template)#,{"devices":devices,"data":data})


def chartView(request):
    device = Device.objects.get(device_name = "North-East Sensor")
    devicedata= device.devicedata_set.last()
    value={}
    value['val'] = devicedata.value
    value['status']=devicedata.status
    #data =  DeviceData.objects.filter(device = "North-East Sensor")[0]
    #data = {"value":12, "timestamp":"12/11/2014"}
    return JsonResponse(value, safe=False)

def login(request):
    try:
        if request.POST:
            
            a = request.POST['username']
            b = request.POST['pass']
            print(a,b)
            try:
                farm = Farm.objects.get( password=b)
                if farm:
                    devices = Device.objects.filter(farm = farm )
                    template = "farmerDashboard.html"
                    return render(request, template,{"devices":devices})
            except:
                template = "login.html"
                return render(request, template)
        else:
            template = "login.html"
            return render(request, template)
    except:
        template = "login.html"
        return render(request, template)

def farmerDashboard(request):
    a = request.POST['username']
    b = request.POST['pass']
    print(a,b)
    try:
        farm = Farm.objects.get(Email = a, password=b)
        print(farm.FarmName)
        if farm:
            devices = Device.objects.filter(farm = farm )
            template = "farmerDashboard.html"
            return render(request, template,{"devices":devices},{"farmName":farm.FarmName})
    except:
        template = "login.html"
        return render(request, template)

    # farm = Farm.objects.all()[0]
    # dic={}
    # devices = Device.objects.filter(farm = farm )
    # data = DeviceData.objects.all()
    # template = "farmerDashboard.html"
    # return render(request, template)#,{"devices":devices,"data":data})


def getDeviceValueStatus(request):#,devicename):
    devices = Device.objects.all()
    count=0
    devicedata_dic={}
    for device in devices: 
        devicedata= device.devicedata_set.last()
        data={}
   
        data['dev']=device.device_name
        data['value'] = devicedata.value
        data['status']=devicedata.status
        devicedata_dic[count]=data
        count+=1
    return JsonResponse(devicedata_dic,safe=False)


def dailyWaterNeed(request):#,devicename):
    devices = Device.objects.all()
    count=0
    c={}
    for device in devices: 
        devicedata= device.devicedata_set.last()
        data={}
   
        data['dev']=device.device_name
        data['value'] = devicedata.value
        data['status']=devicedata.status
        c[count]=data
        count+=1
    return JsonResponse(c,safe=False)