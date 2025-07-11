from .models import *
from django import forms



    
class egasp_Form(forms.ModelForm):

        #using modelchoicefield for dynamic rendering
        PTIDCode = forms.ModelChoiceField(
            queryset=ClinicData.objects.all(),
            to_field_name='PTIDCode',  # Specify the field you want as the value
            widget=forms.Select(attrs={'class': "form-select fw-bold", 'style': 'max-width: auto;'}),
            empty_label="Select PTID Code",
            
        )

        Laboratory_Staff = forms.ModelChoiceField(
             queryset=Clinic_Staff_Details.objects.all(),
             to_field_name='ClinStaff_Name',
             widget=forms.Select(attrs={'class': "form-select fw-bold", 'style': 'max-width: auto;'}),
             empty_label="Select Lab Staff",
             required=False,
        )

        Specimen_Code = forms.ModelChoiceField(
            queryset=SpecimenTypeModel.objects.all(),
            to_field_name='Specimen_code',  # Specify the field you want as the value
            widget=forms.Select(attrs={'class': "form-select fw-bold", 'style': 'max-width: auto;'}),
            empty_label=None,
            required=False,
            
        )

        Current_City = forms.ModelChoiceField(
            queryset=City.objects.all(),
            widget=forms.Select(attrs={'class': "form-select fw-bold", 'style': 'max-width: auto;'}),
            empty_label="Select City",
            required=False,
            
        )

        Current_Province = forms.ModelChoiceField(
            queryset=Province.objects.all(),
            widget=forms.Select(attrs={'class': "form-select fw-bold", 'style': 'max-width: auto;'}),
            empty_label="Select Province",
            required=False,
            
        )
        Permanent_City = forms.ModelChoiceField(
            queryset=City.objects.all(),
            widget=forms.Select(attrs={'class': "form-select fw-bold", 'style': 'max-width: auto;'}),
            empty_label="Select City",
            required=False,
            
        )

        Permanent_Province = forms.ModelChoiceField(
            queryset=Province.objects.all(),
            widget=forms.Select(attrs={'class': "form-select fw-bold", 'style': 'max-width: auto;'}),
            empty_label="Select Province",
            required=False,
            
        )

        class Meta:
            model = Egasp_Data
            fields ='__all__'
            widgets = {
            'Consult_Date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Number_Of_Sex_Partners': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder':'Number of sex partner/s in the past month'}),
            'Growth': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder':'specify hrs. of incubation'}),
            'Date_of_Last_Sex': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Date_Specimen_Collection': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Date_Of_Gram_Stain' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'GS_Date_Released' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Date_Received_in_lab' :forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Positive_Culture_Date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Susceptibility_Testing_Date' :forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'NoTOC_DatePerformed' :forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Confirmation_Ast_Date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Date_Requested_Clinic' :forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Date_Accomplished_Clinic': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Date_Accomplished_ARSP' :forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Date_Released' :forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Date_stocked' :forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'Notes': forms.Textarea(attrs={'class': 'textarea form-control', 'rows': '3'}),
            'ars_notes': forms.Textarea(attrs={'class': 'textarea form-control', 'rows': '3'}),
            'GS_Others': forms.Textarea(attrs={'class': 'textarea form-control', 'rows': '3'}),
            'Azm_Nd': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'azm_nd'}),
            'Azm_Nd_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Cfm_Nd': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'cfm_nd'}),
            'Cfm_Nd_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Cro_Nd':forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'cro_nd'}),
            'Cro_Nd_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Gen_Nd': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'gen_nd'}),
            'Gen_Nd_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Spe_Nd': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'spe_nd'}),
            'Spe_Nd_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Cip_Nd': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'cip_nd'}),
            'Cip_Nd_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Ctx_ND': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'ctx_nd'}),
            'Ctx_ND_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS'}),
            'Ctx_NM': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'ctx_nm'}),
            'Ctx_NM_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Fox_ND': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'fox_nd'}),
            'Fox_ND_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Fox_NM': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'fox_nm'}),
            'Fox_NM_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Cxa_ND': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'cxa_nd'}),
            'Cxa_ND_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Cxa_NM': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'cxa_nm'}),
            'Cxa_NM_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Ery_ND': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'ery_nd'}),
            'Ery_ND_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Ery_NM': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'ery_nm'}),
            'Ery_NM_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Nal_ND': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'nal_nd'}),
            'Nal_ND_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Nal_NM': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'nal_nm'}),
            'Nal_NM_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Pen_ND': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'pen_nd'}),
            'Pen_ND_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Pen_NM': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'pen_nm'}),
            'Pen_NM_RIS': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Tcy_ND': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'tcy_nd'}),
            'Tcy_ND_RIS':forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nd'}),
            'Tcy_NM': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'tcy_nm'}),
            'Tcy_NM_RIS' :forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Azm_Nm' : forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'azm_nm'}),
            'Azm_Nm_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Alert_Azm' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 80px; font-size: 12px'}),
            'Cfm_Nm' : forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'cfm_nm'}),
            'Cfm_Nm_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Alert_Cfm' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 80px; font-size: 12px'}),
            'Cro_Nm' : forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'cro_nm'}),
            'Cro_Nm_Ris_Full' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Alert_Cro' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 80px; font-size: 12px'}),
            'Gen_Nm': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'gen_nm'}),
            'Gen_Nm_Ris_Full' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Alert_Gen': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 80px; font-size: 12px'}),
            'Spe_Nm':forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'spe_nm'}),
            'Spe_Nm_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Cip_Nm': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'CIP_nm'}),
            'Cip_Nm_Ris_Full' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'width: 50px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Retested_Azm_Nm':forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px','placeholder': 'azm_nm'}),
            'Retested_Azm_Nm_Ris_Full' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Retested_Alert_Azm' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px'}),
            'Retested_Cfm_Nm' : forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px', 'placeholder': 'cfm_nm'}),
            'Retested_Cfm_Nm_Ris_Full': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Retested_Alert_Cfm' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px'}),
            'Retested_Cro_Nm': forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px', 'placeholder': 'cro_nm'}),
            'Retested_Cro_Nm_Ris_Full' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Retested_Alert_Cro': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px'}),
            'Retested_Gen_Nm' : forms.NumberInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px', 'placeholder': 'gen_nm'}),
            'Retested_Gen_Nm_Ris_Full' : forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px', 'placeholder': 'RIS_nm'}),
            'Retested_Alert_Gen': forms.TextInput(attrs={'class': 'form-control-sm', 'style': 'align-self: center; width: 90px; font-size: 12px'}),
            'Sexual_Behavior_Others': forms.TextInput(attrs={'placeholder': 'specify other Sexual Behavior'}),
            'Sti_Other': forms.TextInput(attrs={'placeholder': 'specify other STIs'}),
            'growth_span': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            # Add more fields as needed
            }
        


        def __init__(self, *args, **kwargs):
            super(egasp_Form, self).__init__(*args, **kwargs)
            self.fields['Clinic_Code'].widget.attrs['readonly'] = True  # Make Clinic_Code read-only
            self.fields['ClinicCodeGen'].widget.attrs['readonly'] = True  # Make Clinic_Code read-only
            self.fields['Clinic'].widget.attrs['readonly'] = True  # Make Clinic read-only
            self.fields['Egasp_Id'].widget.attrs['readonly'] = True  # Make Egasp_Id read-only
            # self.fields['Growth_span'].widget = forms.HiddenInput()
            self.fields['Clinic_Code'].widget = forms.HiddenInput()

             # Initialize clinic_staff field
            self.fields['Laboratory_Staff'].queryset = Clinic_Staff_Details.objects.all()
            self.fields['Laboratory_Staff'].widget.attrs.update({'class': 'form-control'})
            self.fields['ars_contact'].widget.attrs['readonly'] = True
            self.fields['ars_email'].widget.attrs['readonly'] = True

            # choice fields str set to required = False to prevent an error during saving after edit 
            # error occurs because none=yes makes some fields non editable.
            self.fields['Specimen_Quality'].required = False
            self.fields['Gs_Gram_neg_diplococcus'].required = False
            self.fields['Gs_NoGram_neg_diplococcus'].required = False
            self.fields['Gs_Not_performed'].required = False
            self.fields['Consult_Type'].required=False
            self.fields['Client_Type'].required=False
            self.fields['Sex'].required=False
            self.fields['Gender_Identity'].required=False
            self.fields['Civil_Status'].required=False
            self.fields['Current_Country'].required=False
            self.fields['Permanent_Country'].required=False
            self.fields['Nationality'].required=False
            self.fields['Travel_History'].required=False
            self.fields['Client_Group'].required=False
            self.fields['History_Of_Sex_Partner'].required=False
            self.fields['Nationality_Sex_Partner'].required=False
            self.fields['Relationship_to_Partners'].required=False
            self.fields['SB_Urethral'].required=False
            self.fields['SB_Vaginal'].required=False
            self.fields['SB_Anal_Insertive'].required=False
            self.fields['SB_Anal_Receptive'].required=False
            self.fields['SB_Oral_Insertive'].required=False
            self.fields['SB_Oral_Receptive'].required=False
            self.fields['Sharing_of_Sex_Toys'].required=False
            self.fields['Sti_None'].required=False
            self.fields['Sti_Hiv'].required=False
            self.fields['Sti_Hepatitis_B'].required=False
            self.fields['Sti_Hepatitis_C'].required=False
            self.fields['Sti_NGI'].required=False
            self.fields['Sti_Syphilis'].required=False
            self.fields['Sti_Chlamydia'].required=False
            self.fields['Sti_Anogenital_Warts'].required=False
            self.fields['Sti_Genital_Ulcer'].required=False
            self.fields['Sti_Herpes'].required=False
            self.fields['Sti_Trichomoniasis'].required=False
            self.fields['Sti_Mycoplasma_genitalium'].required=False
            self.fields['Sti_Lymphogranuloma'].required=False
            self.fields['Illicit_Drug_Use'].required=False
            self.fields['Abx_Use_Prescribed'].required=False
            self.fields['Abx_Use_Self_Medicated'].required=False
            self.fields['Abx_Use_None'].required=False
            self.fields['Abx_Use_Other'].required=False
            self.fields['Route_Oral'].required=False
            self.fields['Route_Injectable_IV'].required=False
            self.fields['Route_Dermal'].required=False
            self.fields['Route_Suppository'].required=False
            self.fields['Symp_With_Discharge'].required=False
            self.fields['Symp_No'].required=False
            self.fields['Symp_Discharge_Urethra'].required=False
            self.fields['Symp_Discharge_Vagina'].required=False
            self.fields['Symp_Discharge_Anus'].required=False
            self.fields['Symp_Discharge_Oropharyngeal'].required=False
            self.fields['Symp_Pain_Lower_Abdomen'].required=False
            self.fields['Symp_Tender_Testicles'].required=False
            self.fields['Symp_Painful_Urination'].required=False
            self.fields['Symp_Painful_Intercourse'].required=False
            self.fields['Symp_Rectal_Pain'].required=False
            self.fields['Symp_Other'].required=False
            self.fields['Outcome_Of_Follow_Up_Visit'].required=False
            self.fields['Prev_Test_Pos'].required=False
            self.fields['Result_Test_Cure_Initial'].required=False
            self.fields['Result_Test_Cure_Followup'].required=False
            self.fields['NoTOC_Result_of_Test'].required=False
            self.fields['Patient_Compliance_Antibiotics'].required=False
            self.fields['OtherDrugs_Specify'].required=False
            self.fields['OtherDrugs_Dosage'].required=False
            self.fields['OtherDrugs_Route'].required=False
            self.fields['Gonorrhea_Treatment'].required=False
            self.fields['Treatment_Outcome'].required=False
            self.fields['Primary_Antibiotic'].required=False
            self.fields['Secondary_Antibiotic'].required=False
            self.fields['Specimen_Type'].required=False
            self.fields['Specimen_Quality'].required=False
            self.fields['Diagnosis_At_This_Visit'].required=False
            self.fields['Gram_Neg_Intracellular'].required=False
            self.fields['Gram_Neg_Extracellular'].required=False
            self.fields['Gs_Presence_Of_Pus_Cells'].required=False
            self.fields['Presence_GN_Intracellular'].required=False
            self.fields['Presence_GN_Extracellular'].required=False
            self.fields['GS_Pus_Cells'].required=False
            self.fields['Epithelial_Cells'].required=False
            self.fields['GS_Negative'].required=False
            self.fields['Gs_Gram_neg_diplococcus'].required=False
            self.fields['Gs_NoGram_neg_diplococcus'].required=False
            self.fields['Gs_Not_performed'].required=False
            self.fields['Culture_Result'].required=False
            self.fields['Species_Identification'].required=False
            self.fields['Specimen_Quality_Cs'].required=False
            self.fields['Retested_Mic'].required=False
            self.fields['NAAT_ng'].required=False
            self.fields['NAAT_chl'].required=False
            self.fields['Beta_Lactamase'].required=False
            self.fields['PPng'].required=False
            self.fields['TRng'].required=False
            self.fields['For_possible_WGS'].required=False
            self.fields['Laboratory_Staff'].required=False
            

                 

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['PTIDCode'].queryset = ClinicData.objects.all() # Always load the latest ClinicData instances into the PTIDCode field



class Clinic_Form(forms.ModelForm):
    class Meta:
        model = ClinicData
        fields = ['PTIDCode', 'ClinicCode', 'ClinicName']



#to handle many to many relationship saving
def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


#Breakpoints data
class BreakpointsForm(forms.ModelForm):
     class Meta:
          model = BreakpointsTable
          fields = '__all__'
          widgets = { 
               'Potency': forms.NumberInput(attrs={'min': 0, 'max': 1000}),
                     }
          
     def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Replace None with an empty string or another default value
        for field_name in self.fields:
            value = getattr(instance, field_name)
            if value is None:
                setattr(instance, field_name, '')

        if commit:
            instance.save()
            self.save_m2m()
        return instance

class Breakpoint_uploadForm(forms.ModelForm):
    class Meta:
          model = Breakpoint_upload
          fields = ['File_uploadBP']

    #ensure only csv and excel are uploaded
    def clean_file_upload(self):
            file = self.cleaned_data.get('File_uploadBP') #make sure this matches the model 
            if file:
                if not file.name.endswith('.csv') and not file.name.endswith('.xlsx'):
                    raise forms.ValidationError('File must be a CSV or Excel file.')
            return file

#for antibiotic entry form
class AntibioticEntryForm(forms.ModelForm):
        ab_Abx_code = forms.ModelChoiceField(
            queryset=BreakpointsTable.objects.all(),
            to_field_name='Antibiotic',
            widget=forms.Select(attrs={'class': "form-select fw-bold", 'style': 'max-width: auto;'}),
            empty_label="Select Antibiotic",
            required=False,
        )
        
        class Meta:
            model = AntibioticEntry
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(AntibioticEntryForm, self).__init__(*args, **kwargs)
            self.fields['ab_EgaspId'].widget.attrs['readonly'] = True  # Make Egasp_id read-only


class SpecimenTypeForm(forms.ModelForm):
    class Meta:
        model = SpecimenTypeModel  # Ensure the model is specified
        fields = ['Specimen_name', 'Specimen_code']  # Include the fields you want in the form


class ContactForm(forms.ModelForm):
    class Meta:
        model = Clinic_Staff_Details
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['ClinStaff_Telnum'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '09171234567',  # Philippine phone number format
            'readonly': False  # Ensure it's not blocking JavaScript updates
        })

#for locations
class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ['provincename']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Province Name'})
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["cityname", "province"]
        widgets = {
            "cityname": forms.TextInput(attrs={"class": "form-control"}),
            "province": forms.Select(attrs={"class": "form-control"}),
        }

class LocationUploadForm(forms.ModelForm):
    class Meta:
        model = LocationUpload
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }
