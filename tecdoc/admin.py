from django.contrib import admin
from tecdoc.models import Supplier, Part, Manufacturer, CarModel, CarType, PartAnalog, PartCross


# Register your models here.



class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'dataversion', 'title', 'matchcode', 'nbrofarticles', 'hasnewversionarticles')
    list_display_links = ('id', 'dataversion', 'title', 'matchcode', 'nbrofarticles', 'hasnewversionarticles')
    search_fields = ('title', 'matchcode')


class PartAdmin(admin.ModelAdmin):
    list_display = (
        'supplier', 'part_number', 'clean_part_number', 'title', 'state', 'state_title', 'description',
        'flagaccessory', 'flagmaterialcertification', 'flagremanufactured', 'flagselfservicepacking', 'foundby',
        'hasaxle', 'hascommercialvehicle', 'hascvmanuid', 'hasengine', 'haslinkitems', 'hasmotorbike',
        'haspassengercar', 'isvalid', 'lotsize1', 'lotsize2', 'packingunit', 'quantityperpackingunit')
    list_display_links = ('supplier', 'part_number', 'clean_part_number', 'title')
    search_fields = ('supplier__title', 'part_number', 'clean_part)number')


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'can_display', 'description', 'link', 'axle', 'commercial_vehicle', 'cv_manufacturer', 'engine',
        'motorbike', 'passenger_car', 'transporter', 'valid_for_current_country', 'vgl', 'link_item_type', 'match_code')
    list_display_links = (
        'id', 'title', 'can_display', 'description', 'link', 'axle', 'commercial_vehicle', 'cv_manufacturer', 'engine',
        'motorbike', 'passenger_car', 'transporter', 'valid_for_current_country', 'vgl', 'link_item_type', 'match_code')
    search_fields = ('id', 'title', 'description')


class CarModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'manufacturer', 'title', 'can_display', 'description', 'link', 'axle', 'commercial_vehicle',
        'cv_manufacturer_id', 'engine',
        'motorbike', 'passenger_car', 'transporter', 'valid_for_current_country', 'link_item_type')
    list_display_links = (
        'id', 'manufacturer', 'title', 'can_display', 'description', 'link', 'axle', 'commercial_vehicle',
        'cv_manufacturer_id', 'engine',
        'motorbike', 'passenger_car', 'transporter', 'valid_for_current_country', 'link_item_type')
    search_fields = ('id', 'manufacturer__title', 'title', 'description')



class CarTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_manufacturer', 'model', 'description', 'construction_interval', 'can_display', 'link', 'axle',
        'commercial_vehicle', 'cv_manufacturer_id', 'engine', 'motorbike', 'passenger_car', 'transporter',
        'valid_for_current_country', 'link_item_type')
    list_display_links = (
        'id', 'get_manufacturer', 'model', 'description', 'construction_interval', 'can_display', 'link', 'axle',
        'commercial_vehicle', 'cv_manufacturer_id', 'engine', 'motorbike', 'passenger_car', 'transporter',
        'valid_for_current_country', 'link_item_type')
    search_fields = ('id', 'model__title', 'title', 'description', 'model__manufacturer__title')

class PartAnalogAdmin(admin.ModelAdmin):
    list_display =('supplier', 'part_number', 'oenbr', 'manufacturer', 'isadditive')
    list_display_links = ('supplier', 'part_number', 'oenbr', 'manufacturer', 'isadditive')
    search_fields = ('oenbr', 'part_number')


class PartCrossAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'part_number', 'oenbr', 'manufacturer')
    list_display_links = ('supplier', 'part_number', 'oenbr', 'manufacturer')
    search_fields = ('oenbr', 'part_number')

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarType, CarTypeAdmin)
admin.site.register(PartAnalog, PartAnalogAdmin)
admin.site.register(PartCross, PartCrossAdmin)