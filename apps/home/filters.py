import django_filters
from .models import Egasp_Data
from django_filters import DateFromToRangeFilter

class dataFilter(django_filters.FilterSet):
    Date_of_Entry = DateFromToRangeFilter()
    
    class Meta:
        model = Egasp_Data
        fields = {  'Egasp_Id': ['exact'], 
                    'Laboratory': ['icontains'],
                    'Clinic':['icontains'],
                    'Consult_Date':['icontains'],
                    'Consult_Type':['icontains'],
                    'Uic_Ptid':['exact'], 
                    'Clinic_Code':['icontains'], 
                    'First_Name':['icontains'], 
                    'Last_Name':['icontains'], 
                    'Birthdate':['icontains'], 
                    'Sex':['icontains'],
                    'Date_of_Entry':['exact']
                    }
   
