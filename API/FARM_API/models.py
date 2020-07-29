from django.db import models
from datetime import datetime

class Farm(models.Model):
    Name=models.CharField("Full Name",max_length=15)
    Contact=models.CharField(max_length=15)
    Location=models.CharField(max_length=30)
    Email           =   models.EmailField(primary_key = True,max_length=40, blank = False )
    FarmName        =   models.CharField("Farm Name",max_length=20)
    password        =   models.CharField(max_length=30)
    climatic_zone   =   models.CharField(max_length=60, default='')

    def __str__(self):
        return self.FarmName


class Device(models.Model):
    device_name     =   models.CharField(primary_key = True , max_length=20)
    parameter       =   models.CharField(max_length=20)
    unit            =   models.CharField(max_length=15)
    zone            =   models.CharField(max_length=20)
    longitude       =   models.CharField(max_length=10,  default = '0.0')
    latitude        =   models.CharField(max_length= 10, default = '0.0')
    farm            =   models.ForeignKey(Farm, max_length=20, on_delete=models.CASCADE)

    def __str__(self):
        return self.device_name



class DeviceData(models.Model):
    device          =   models.ForeignKey(Device, max_length=20, on_delete=models.CASCADE)
    value           =   models.DecimalField(max_digits=3, decimal_places=1)
    status          =   models.CharField(max_length=20, default = "..")
    timestamp       =   models.DateTimeField(auto_now_add=True, auto_now=False)

    
#the daily water needed for a standard grass
class StandardGrassDailyWaterNeed(models.Model):
    min_MDT         =   models.DecimalField(max_digits=5, decimal_places=1)
    max_MDT         =   models.DecimalField(max_digits=5, decimal_places=1)
    min_water       =   models.DecimalField(max_digits=5, decimal_places=1)
    max_water       =   models.DecimalField(max_digits=5, decimal_places=1)
    climatic_zone   =   models.CharField(max_length=30)

    def __str__(self):
        return self.climatic_zone


#the relative water need of a crop is the daily water needed by a crop as compared to a stantard grass
class RelativeWaterNeed(models.Model):
    crop_name       =   models.CharField(max_length=40)
    relativity_value=   models.IntegerField()
    sign            =   models.CharField(max_length=2)

    def __str__(self):
        return self.crop_name

# life cycle period of crops
class TotalGrowingPeriod(models.Model):
    crop_name       =   models.CharField(max_length=40)
    min_growth_period=  models.IntegerField()
    max_growth_period=  models.IntegerField()
    
    def __str__(self):
        return self.crop_name


# settings for system water need checker
class WaterNeedRecommenderInfo(models.Model):  
    crop            =   models.CharField(max_length=60)
    zone            =   models.CharField(max_length=30, default='')
    sow_time        =   models.DateField(null=False, blank=False)
    min_daily_water =   models.DecimalField(max_digits = 4,decimal_places=1, default = 0.0)
    max_daily_water =   models.DecimalField(max_digits = 4, decimal_places=1, default = 0.0)
    use_sys_setpoint=   models.BooleanField(default=False)
    setpoint_value  =   models.DecimalField(max_digits=3, decimal_places=1,default=0.0)
    farm            =   models.ForeignKey(Farm, max_length=20, on_delete=models.CASCADE)
    

#set point settings
class SetpointSettings(models.Model):
    use_sys_setpoint=   models.BooleanField(default=False)
    value           =   models.DecimalField(max_digits=3, decimal_places=1)
    farm            =   models.ForeignKey(Farm, max_length=20, on_delete=models.CASCADE) 


#temperature values of farms
class FarmTemperature(models.Model):
    value           =   models.IntegerField()
    farm            =   models.ForeignKey(Farm, max_length=20, on_delete=models.CASCADE)

#Notification for farms  
class Notification(models.Model):
    device_name     =   models.CharField(max_length=20)
    status          =   models.CharField(max_length=10)
    farm            =   models.ForeignKey(Farm, max_length=20, on_delete=models.CASCADE)
    acknowledge     =   models.BooleanField(default=False)
    active          =   models.BooleanField(default=True)
    timestamp       =   models.DateTimeField(default = datetime.now)


"""class Controlling_Channel(models.Model):
    channel_name    =   models.CharField(max_length=30,primary_key=True)
    value           =   models.IntegerField(max_length=3)
    setVal          =   models.IntegerField(default=0)
    controller      =   models.CharField( max_length=20 )
    farm            =   models.ForeignKey(Farm, max_length=20, on_delete=models.CASCADE)

    def __str__(self):
        return self.channel_name,self.value,self.controller"""



    
