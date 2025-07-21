# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from apps.home import views



urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('crf/', views.crf_data,name='crf_data'),
    path('show/', views.show_data,name='show_data'),
    path('edit/<int:id>/',views.edit_data,name='edit_data'),
    path('delete/<int:id>/',views.delete_data,name='delete_data'),
    path('generate-pdf/<int:id>/', views.generate_pdf, name='generate_pdf'),
    path('clinic-add/', views.add_dropdown,name='add_dropdown'),
    path('clinic-view', views.clinic_view,name='clinic_view'),
    path('clinic-delete/<int:id>/',views.delete_dropdown,name='delete_dropdown'),
    path("search/", views.search, name="search"),
    path('clinic-code/', views.get_clinic_code, name='get_clinic_code'),
    path('breakpoints-view/', views.breakpoints_view, name='breakpoints_view'),
    path('breakpoints-delete/<int:id>', views.breakpoints_del, name='breakpoints_del'),
    path('breakpoints-add/', views.add_breakpoints, name='add_breakpoints'), 
    path('breakpoints-edit/<int:pk>/', views.add_breakpoints, name='edit_breakpoints'),  
    path('breakpoints-upload/', views.upload_breakpoints, name='upload_breakpoints'),
    path('breakpoints-deleteAll/', views.delete_all_breakpoints, name='delete_all_breakpoints'),
    path('breakpoints-export/', views.export_breakpoints, name='export_breakpoints'),
    path('test_results-view/', views.abxentry_view, name='abxentry_view'),
    path('specimens/', views.specimen_list, name='specimen_list'),
    path('specimens-add/', views.add_specimen, name='add_specimen'),
    path('specimens-edit/<int:pk>/', views.edit_specimen, name='edit_specimen'),
    path('specimens-delete/<int:pk>/', views.delete_specimen, name='delete_specimen'),
    path('generate_gs/<int:id>/', views.generate_gs, name='generate_gs'),
    path('antibioticentry-export/', views.export_Antibioticentry, name='export_Antibioticentry'),
    path('contact/add/', views.add_contact, name='add_contact'),
    path('contact/delete/<int:id>/', views.delete_contact, name='delete_contact'),
    path('contact/view/', views.contact_view, name='contact_view'),
    path('contact/edit/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('get_clinic_staff_details/', views.get_clinic_staff_details, name='get_clinic_staff_details'),
    path("add-location/", views.add_location, name="add_location"),
    path('upload-location/', views.upload_locations, name='upload_locations'),
    path('view-location/', views.view_locations, name='view_locations'),
    path('delete_cities/', views.delete_cities, name='delete_cities'),
    path('delete_city/<int:id>/', views.delete_city, name='delete_city'),
    path('download_combined_table/', views.download_combined_table, name='download_combined_table'),
    path('get-cities/', views.get_cities_by_province, name='get_cities_by_province'),
    

   
     
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
 
    

]
