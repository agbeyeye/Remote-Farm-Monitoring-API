from django.contrib import admin
from .models import Farm,StandardGrassDailyWaterNeed, RelativeWaterNeed,TotalGrowingPeriod,WaterNeedRecommenderInfo,SetpointSettings,FarmTemperature,Notification, Device, DeviceData



class StandardGrassDailyWaterNeedAdmin(admin.ModelAdmin):
    search_fields=['climatic_zone']
    list_display=['min_MDT','max_MDT','min_water','max_water','climatic_zone']
    list_filter=['climatic_zone','min_MDT','min_water','max_MDT','max_water']
    
    class meta:
        model=StandardGrassDailyWaterNeed

class RelativeWaterNeedAdmin(admin.ModelAdmin):
    search_fields=['crop_name']
    list_display=['crop_name','relativity_value','sign']
    list_filter=['crop_name','relativity_value','sign']
    
    class meta:
        model=RelativeWaterNeed


class TotalGrowingPeriodAdmin(admin.ModelAdmin):
    search_fields=['crop_name']
    list_display=['crop_name','min_growth_period','max_growth_period']
      
    class meta:
        model=TotalGrowingPeriod


class WaterNeedRecommenderInfoAdmin(admin.ModelAdmin): 
    search_fields=['zone','crop']
    list_display=['crop','zone','use_sys_setpoint','setpoint_value','sow_time','farm']
    list_filter=['crop','sow_time','farm']

    class meta:
        model=WaterNeedRecommenderInfo


class SetpointSettingsAdmin(admin.ModelAdmin):
    search_fields=['farm']
    list_display=['farm','use_sys_setpoint','value']

    class meta:
        model=SetpointSettings


class FarmTemperatureAdmin(admin.ModelAdmin):
    search_fields=['farm']
    list_display=['farm','value']
    
    class meta:
        model=FarmTemperature

class NotificationAdmin(admin.ModelAdmin):
    list_display=['device_name','status','farm','acknowledge','timestamp']
    search_fields=['farm','device_name','acknowledge','status']
    readonly_fields=['timestamp']

    class Meta:
        model= Notification

class FarmAdmin(admin.ModelAdmin):
    list_display=['Name','Contact','Location','Email','FarmName','climatic_zone']
    search_fields=['Name','Email','FarmName']

    class Meta:
        model= Farm

class DeviceAdmin(admin.ModelAdmin):
    list_display=['device_name','parameter','unit','zone','farm']
    search_fields=['device_name','parameter','zone','farm']

    class Meta:
        model= Device


class DeviceDataAdmin(admin.ModelAdmin):
    list_display=['device','value','timestamp']
    search_fields=['device','timestamp']

    class Meta:
        model= DeviceData

admin.site.register(DeviceData,DeviceDataAdmin)
admin.site.register(Device,DeviceAdmin)
admin.site.register(Farm,FarmAdmin)
admin.site.register(StandardGrassDailyWaterNeed,StandardGrassDailyWaterNeedAdmin)
admin.site.register( RelativeWaterNeed, RelativeWaterNeedAdmin)
admin.site.register(TotalGrowingPeriod,TotalGrowingPeriodAdmin)
admin.site.register(WaterNeedRecommenderInfo,WaterNeedRecommenderInfoAdmin)
admin.site.register(SetpointSettings, SetpointSettingsAdmin)
admin.site.register(FarmTemperature,FarmTemperatureAdmin)
admin.site.register(Notification,NotificationAdmin)

