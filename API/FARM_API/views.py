from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from . models import TotalGrowingPeriod, DeviceData,Farm, RelativeWaterNeed,SetpointSettings,FarmTemperature,WaterNeedRecommenderInfo,StandardGrassDailyWaterNeed,Notification, Device
import json
from . serializer import DeviceDataSerializer
from datetime import date
from datetime import datetime
from decimal import Decimal
from . import Notification_service

#create config file for the remote device
def get_ConfigFile(email): 
    #object to hold configuration structure
    config_file     =   {}
    #save farm name in a dictionary
    farm_dic        =   {}
    #save zones 
    zone_file       =   {}

    controllers_file=   {}
    #list of zones
    zone_list       =   []
    
    c_email        =   email
    c_farm          =   Farm.objects.get(Email= c_email)  
    farm_dic['FarmName'] = str(c_farm.FarmName)
    zones           =   Device.objects.filter(farm = c_farm).values_list('zone')
    zones           =   list(dict.fromkeys(zones))
    count = 0
    #for each zone get devices 
    for c_zone in zones:
        zone_dic={}
        device_list =   []
        devices     =   Device.objects.filter(zone = c_zone[0],farm = c_farm)

        #for each device get device info
	
        for c_device in devices:
            device_dic = {}
            device_dic['name']      =   str(c_device.device_name)
            device_dic['parameter'] =   str(c_device.parameter)
            device_dic['unit']      =   str(c_device.unit)
            device_dic['latitude']  =   c_device.latitude
            device_dic['longitude'] =   c_device.longitude

            device_list.append(device_dic)
        
        zone_dic['zoneName']        =   c_zone
        zone_dic['devices']         =   device_list
        zone_list.append(zone_dic)
        count+=1
    farm_dic['zones']       =   zone_list

    config_file['success']  =   "True"
    config_file['data']     =   farm_dic
    
    return config_file

    """controllers     =   Controlling_Channel.objects.filter(farm = c_farm).values_list('controller')
    controllers     =   list(dict.fromkeys(controllers))
    for c_controller in controllers:
        channel_names = Controlling_Channel.objects.filter(controller = c_controller, farm = c_farm).values_list('channel_name')
        controllers_file[channel_names] = channel_names
    config_file['Controllers']  =   controllers_file"""
       
# login by remote device
def Login(request):
    loginInfo       =   request.body
    loginInfo       =   eval(bytes.decode(loginInfo))
    username        =   loginInfo['username']
    pword           =   loginInfo['password']
    farm            =   Farm.objects.filter(Email=username, password=pword)
    if not farm:
        config_file={"success":'False'}
        config_file['Error']   = "Invalid  Email or password"
        return JsonResponse(config_file)
        
    else:
        config_json = get_ConfigFile(username)
        return JsonResponse(config_json)

#manual soil moisture monitor
def moistureStatusMonitor(farm,moisture_value,zone):
    data            =   WaterNeedRecommenderInfo.objects.get(farm=farm,zone = zone)
    setvalue        =   data.setpoint_value
    status          =   'ok'
    
    if float(moisture_value) < float(setvalue):
        status    =   'low'
    
    return status


# system soil moisture monitor
def dailyWaterComputation(farm,temperature):
    # initialization
    status=[]
    min_water       =   0
    max_water       =   0
    max_water_need  =   0   
    min_water_need  =   0

    # get the temperature value of the farm
    #temp_obj        =   FarmTemperature.objects.get(farm = farm)
    farm_temp       =   temperature

    #get the climatic zone, crop, sow time of crop of the farm
    climatic_obj    =   WaterNeedRecommenderInfo.objects.get(farm = farm)
    farm_climate    =   farm.climatic_zone
    crop_name       =   climatic_obj.crop
    sow_time        =   climatic_obj.sow_time
    useSystemSetting=   climatic_obj.use_sys_setpoint
    setpoint_value  =   climatic_obj.setpoint_value
    #get the soil moisture value of the farm
    #sensor_read_obj =   DeviceData.objects.get(device_name = device_name)
    #sensor_value    =   sensor_read_obj.value

    #get crop growth cycle   
    cropCycle_obj   =   TotalGrowingPeriod.objects.get(crop_name= crop_name)
    min_duration    =   cropCycle_obj.min_growth_period
    max_duration    =   cropCycle_obj.max_growth_period
    averg_duration  =   (min_duration+max_duration)/2
    delta           =   date.today() - sow_time
    crop_age        =   delta.days

    #get exact grass data that suit farm climatic zone and temp range
    grass_obj       =   StandardGrassDailyWaterNeed.objects.get(climatic_zone = farm_climate, min_MDT__lte=farm_temp, max_MDT__gte=farm_temp)
    
    # identify suitable water need for obtained temperature and climatic zone
    #for rec in grass_obj:
        # compare farm temperature with grass temperatures
        #if farm_temp >= rec.min_MDT and farm_temp<= rec.max_MDT: 
    if grass_obj:
            #get minimum water need for grass at specified min temp and climatic zone 
            min_water           =   grass_obj.min_water
            # maximum water need for grass at specified max temp and climatic zone
            max_water           =   grass_obj.max_water 
            # water need value of crop relative with standard grass
            water_range_obj     =   RelativeWaterNeed.objects.get(crop_name = crop_name)
            # relative water need of crop in %
            relative_water      =   water_range_obj.relativity_value
            #sing of relative value
            sign                =   water_range_obj.sign
            
            # if value is positive
            if sign == '0':
                min_water_need  =  min_water + (min_water*relative_water)/100
                max_water_need  =  max_water + (max_water*relative_water)/100

            #if value is negative 
            elif sign == '1':
                min_water_need  =  min_water - (min_water*relative_water)/100
                max_water_need  =  max_water - (max_water*relative_water)/100

            # check growth stage of crop  
            if float(crop_age)  <  (averg_duration/2):
                min_water_need  =   min_water_need/2
                max_water_need  =   max_water_need/2

            if useSystemSetting:
                climatic_obj.setpoint_value = min_water_need

            climatic_obj.min_water_need = min_water_need
            climatic_obj.max_water_need = max_water_need
            climatic_obj.save()

            
            

            #print (min_water_need, max_water_need)
            # compare actual soil moisture of farm to computed water need
            # if moisutre is within water need range
            # if moisture_value >= min_water_need and moisture_value <= max_water_need:
            #     status.append("ok")

            # # if moisture is less than minimum water need
            # elif moisture_value <min_water_need:
            #     status.append("low")

            # # if moisture is above maximum water need
            # elif moisture_value > max_water_need:
            #     status.append("high")
            # status.append(str(min_water_need)+" - "+str(max_water_need))
            # #print(status)
            # return status

#  standard info of crop (cultivation cycle and water need)       
def crop_info(request):
    data            =   request.body
    data            =   eval(bytes.decode(data))
    farmId          =   data['username']
    farm            =   Farm.objects.get(farm_Id = farmId)
    climatic_obj    =   WaterNeedRecommenderInfo.objects.get(farm = farm)
    farm_climate    =   climatic_obj.climatic_zone
    crop_name       =   climatic_obj.crop
    water_range_obj =   RelativeWaterNeed.objects.get(crop_name = crop_name)
    # relative water need of crop in %
    relative_water  =   water_range_obj.relativity_value
    #sing of relative value
    sign            =   water_range_obj.sign
    grass_obj       =   StandardGrassDailyWaterNeed.objects.filter(climatic_zone = farm_climate)
    crop_info_dic   =   {}
    daily_water_dic   =   {}
    crop_info_dic['crop_name'] = crop_name
    # identify suitable water need for obtained temperature and climatic zone
    for rec in grass_obj:
            temp_range          =   str(rec.min_MDT)+" - "+str(rec.max_MDT)
            #get minimum water need for grass at specified min temp and climatic zone 
            min_water           =   rec.min_water
            # maximum water need for grass at specified max temp and climatic zone
            max_water           =   rec.max_water 
                                   
            # if value is positive
            if sign == '0':
                min_water_need  =  min_water + min_water*relative_water
                max_water_need  =  max_water + max_water*relative_water

            #if value is negative 
            elif sign == '1':
                min_water_need  =  min_water - min_water*relative_water
                max_water_need  =  max_water - max_water*relative_water

            water_range         =   str(min_water_need)+" - "+str(max_water_need)

            # dictionary with the crop temp range and water range
            daily_water_dic[temp_range] = water_range

    crop_info_dic["daily_water"] = daily_water_dic

    return JsonResponse(crop_info_dic)

#set moisture threshold
def set_setpoints(request):
    data        =   request.body
    data        =   eval(bytes.decode(data))
    use_systemSetpoint   =   data['use_sys_setpoint']
    farm_Id  =   data['farm_Id']
    farm    =   Farm.objects.get(farm_Id= farm_Id)
    setpoint_data   =   SetpointSettings.objects.filter(farm=farm)
    if not setpoint_data:
        if not use_systemSetpoint:
            value   =   data['value']
            SetpointSettings.objects.create(use_sys_setpoint = use_systemSetpoint, value= value, farm= farm)
        elif use_systemSetpoint:
            SetpointSettings.objects.create(use_sys_setpoint = use_systemSetpoint, value= 0, farm= farm)
    elif setpoint_data:
        if not use_systemSetpoint:
            setpoint_data.value   =   data['value']
            setpoint_data.use_sys_setpoint = use_systemSetpoint
        elif use_systemSetpoint:
            setpoint_data.use_sys_setpoint = use_systemSetpoint
        setpoint_data.save()
        
# send parameter data to remote device 1.1
def DataRequest(request,farmId):
    
    c_farm          =   Farm.objects.get(farm_Id=farmId)
    data            =   DeviceData.objects.filter(farm=c_farm)
    serializer      =   DeviceDataSerializer(data,many=True)
    return JsonResponse(serializer.data,safe=False)

# Data to mobile device 1.2
def DataToRemoteDevice(request):
    #try:
        datas       =   request.body
        datas       =   eval(bytes.decode(datas))
        email       =   datas['username']
        data = {}
        status      =   []
        farm_dic    =   {}
        device_list =   []
        #c_farmId        =   farmId
        c_farm          =   Farm.objects.get(Email= email)  
        data['success'] = "True"
        devices           =   Device.objects.filter(farm = c_farm)
        #devices           =   list(dict.fromkeys(devices))
        count = 0
        setpoint_obj    =   SetpointSettings.objects.get(farm = c_farm)

        #for each device get device info
        for c_device in devices:
            device= c_device.devicedata_set.last()
            # if setpoint_obj.use_sys_setpoint:
            #     status  =   systemMoistureStatusMonitor(c_farm,float(value.value))
            # else:
            #     status  =   manualMoistureStatusMonitor(c_farm, float(value.value))

            device_dic = {}
        
            device_dic['device_name']         =   str(c_device.device_name)
            device_dic['parameter'] =   str(c_device.parameter)
            device_dic['value']      =  str(device.value)
            device_dic['unit']      =   str(c_device.unit)
            device_dic['status']    =   device.status
            #device_dic['setpoint']  =   status[1]
            device_dic['zone']      =   str(c_device.zone)

           
            #farm_dic[device_name]=device_dic
            device_list.append(device_dic)
        data["data"]=device_list
        temp_obj = FarmTemperature.objects.get(farm = c_farm)
        data["temperature"] = temp_obj.value
        print('data sent...')
        return JsonResponse(data,safe=False)
    #except:
        #return JsonResponse({"success":"False"})

#update device data
def updateDeviceDataModel(request):
    data_from_farm    =   request.body
    data_from_farm  =   eval(bytes.decode(data_from_farm))
    #a = eval(data_from_farm)
    #print(data_from_farm['farm_Id'])
    #print(data_from_farm['DeviceData'])
    farm_Name     =   data_from_farm['farm_Id']
    Data          =   data_from_farm['DeviceData']
    c_farm        =   Farm.objects.get(FarmName=farm_Name)
    if c_farm:
        for devices in Data:
            device_name = devices['device_name']

            status= moistureStatusMonitor(farm = c_farm, moisture_value= devices['value'],zone= devices['zone'])
            if status == "low" or status == "high":
                print("notification has occured")
                Notification_service.register_notification(device=device_name,status=status,farm= c_farm)

            
            try:
                c_device    = Device.objects.get(device_name=device_name)
                #c_device    = DeviceData.objects.get(device_name=device_name)
                if c_device:
                    device_Data     = DeviceData(value = devices['value'], status = status, device= c_device)
                    device_Data.save()
                    #print('device exist')
                
            except Device.DoesNotSave:#else:
                new_device    =    Device(device_name= device_name,parameter=devices['parameter'],unit=devices['unit'],zone=devices['zone'],longitude= devices['longitude'], latitude=devices['latitude'],farm=c_farm)
                new_device.save()
                device_Data     = DeviceData(value = devices['value'], status = status, device= new_device)
                device_Data.save()
                #print('new record')
    
    return HttpResponse("done")

#send alarms to remote device
def send_notification(request):
    data            =   request.body
    data            =   eval(bytes.decode(data))
    farmId          =   data['username']
    latest_timestamp=   data['timestamp']
    #obtain the latest timestamp of the last notification
    index =len(latest_timestamp)-2 
    number = int(latest_timestamp[index])+1
    list_t=list(latest_timestamp)
    list_t[index]= str(number)
    latest_timestamp="".join(list_t)
    print (number)
    print(latest_timestamp)

    return JsonResponse(Notification_service.get_notification(farmId,latest_timestamp))
    
#acknowledge alarms
def alarm_acknowledgement(request):
    data          =   request.body
    data          =   eval(bytes.decode(data))
    farmId        =   data['username']
    alarmId        =   data['alarmId']
    ack_status    =   data['ack']
    if ack_status == 'True':
        return JsonResponse(Notification_service.acknowledge_alarm(farmId,alarmId))

def homeView(request):
    # farm = Farm.objects.all()[0]
    # dic={}
    # devices = Device.objects.filter(farm = farm )
    # data = DeviceData.objects.all()
    # template = "farmerDashboard.html"
    # return render(request, template,{"devices":devices,"data":data})
    pass


def chartView(request):
    #data =  DeviceData.objects.filter(device = "North-East Sensor")
    data = {"value":12, "timestamp":"12/11/2014"}
    return JsonResponse(data)
    
def getFarmTemperature(request):
    data        =  request.body
    data        =  eval(bytes.decode(data))
    farmId      =  data['farmId']
    temp        =  data['temp'] 
    try:
        farm       =   Farm.objects.get(Email = farmId)
        obj, created = FarmTemperature.objects.get_or_create(farm=farm, value=temp)
        dailyWaterComputation(farm, temp)
    except:
        return "error"
    

#user settings  
def loadRecommenderInfo():
    pass
