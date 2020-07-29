from .models import Notification, Farm
from datetime import datetime


def register_notification(device, status,farm):
    device_n = Notification.objects.filter(device_name = device, acknowledge = False)

    if not device_n:
        Notification.objects.create(device_name= device, status = status,farm = farm, acknowledge = False)

def notification_garbage_collector():
    devices     =   Notification.objects.all()
    for dev in devices:
        if dev.acknowledge:
            dev.delete()

def get_notification(farmId, timestamp):
    count           =   0
    notification_dic= {}
    alarm_list=[]
    try:
        date_time_obj = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fz')
        notification_dic['success'] = 'True'
        farm            =   Farm.objects.get(farm_Id = farmId)
        new_notifications =   Notification.objects.filter(farm = farm, timestamp__gt=date_time_obj)
        if new_notifications:
            for notif in new_notifications:
                if notif.timestamp !=date_time_obj:
                    notif_dic = {}
                    notif_dic['id'] = notif.id
                    notif_dic['device'] = notif.device_name
                    notif_dic['status'] = notif.status
                    notif_dic['timestamp'] = notif.timestamp
                    alarm_list.append(notif_dic)
            notification_dic["data"] = alarm_list
        else:
            notification_dic['data']=[]
    except:
        notification_dic['success'] = 'False'
    
    return notification_dic

def acknowledge_alarm(farmId,alarmId):
    response = {}
    try:
        farm   =   Farm.objects.get(farm_Id = farmId)
        device_alarm = Notification.objects.get(farm = farm, id = alarmId)
        if device_alarm:
            device_alarm.acknowledge = True
            device_alarm.save()
            response['success'] = True
    except:
        response['success'] = False
    
    return response

