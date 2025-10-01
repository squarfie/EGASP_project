from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


# Create your models here.
#For province and Cities

class Province(models.Model):
    provincename = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.provincename

class City(models.Model):
    cityname = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities")


    class Meta:
        unique_together = ("province", "cityname")

    def __str__(self):
        return f"{self.cityname}"

    

# Model for Province File Upload
class LocationUpload(models.Model):
    file = models.FileField(upload_to='uploads/locations/', null=True, blank=True)

    class Meta:
        db_table = "LocationUpload"


####   Clinical Data TAB
class Egasp_Data(models.Model):
    Common_Choices = (
        ('',''),
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('No Answer', 'No Answer'),
        ('n/a','n/a')
    )
    SpeciesChoices =(
        ('n/a','n/a'),
        ('Neisseria gonorrhoeae', 'Neisseria gonorrhoeae'),
        ('No Neisseria gonorrhoeae isolated','No Neisseria gonorrhoeae isolated'),
        ('Other','Other'))
    ConsultTypeChoices =(
        ('', ''),
        ('Initial Visit', 'Initial Visit'),
        ('Follow Up', 'Follow-up'),
        ('No Answer', 'No Answer'))
    ClientTypeChoice =(
        ('', ''),
        ('Referral', 'Referral'),
        ('Walk-in', 'Walk-in'),
        ('No Answer', 'No Answer'))
    SexatbirthChoice=(
        ('',''),
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    GenderChoice=(
        ('',''),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender Male', 'Transgender Male'),
        ('Transgender Female', 'Transgender Female'),
        ('Other', 'Other'),
        ('Unknown', 'Unknown')
    )
    Civil_StatusChoice=(
        ('', ''),
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Live-in Partner', 'Live-in Partner'),
        ('No Answer', 'No Answer')
    )
    Nationality_Choice=(
        ('',''),
        ('Filipino', 'Filipino'),
        ('Other', 'Other'),
        ('No Answer', 'No Answer'))
    
    TravelHistory_Choice=(
        ('',''),
        ('Within Country', 'Within the Country'),
        ('Outside Country', 'Outside the Country'),
        ('Both','Both'),
        ('No Travel','No Travel History')
    )
    Client_Risk_Choice=(
        ('n/a','n/a'),
        ('MSM', 'MSM'),
        ('Transgender','Transgender'),
        ('Heterosexual','Heterosexual'),
        ('PWID', 'PWID'),
        ('PDL', 'PDL'),
        ('OFW/Partner of OFW', 'OFW/Partner of OFW'),
        ('Female Partner of MSIM or PWID', 'Female Partner of MSIM or PWID' ),
        ('Registered Sex Worker', 'Registered Sex Worker'),
        ('Freelance Sex Worker', 'Freelance Sex Worker'),
        ('General Population', 'General Population')
    )
    Sex_PartnerChoice=(
        ('',''),
        ('with Both sex','with Both sex'),
        ('with Male', 'with Male'),
        ('with Female', 'with Female'),
        ('Unknown', 'Unknown')
    )

    NationalityofPartner_Choice=(
        ('',''),
        ('Filipino', 'Filipino'),
        ('Filipino and', 'Filipino and'),
        ('No Answer', 'No Answer'),
    )
    Relationship_to_partnerChoice=(
        ('n/a','n/a'),
        ('Spouse/live-in partner', 'Spouse/live-in partner'),
        ('Regular non-spouse', 'Regular non-spouse'),
        ('Casual', 'Casual')
    )
    Illicit_Drug_Use_Choices=(
        ('',''),
        ('Drug Use, Current', 'Drug Use, Current'),
        ('Drug Use, past 30 days', 'Drug Use, >past(30 days)'),
        ('No Drug Use', 'No Drug Use'),
        ('No Answer', 'No Answer')
    )
    Symp_Gonorrhoea_Choice=(
        ('',''),
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Unknown', 'Unknown')
        )
    Outcome_Followup_Choice=(
        ('',''),
        ('Returned to Clinic with Symptoms', 'Returned to Clinic with Symptoms'),
        ('Returned to Clinic without Symptoms', 'Returned to Clinic without Symptoms' ),
        ('No follow-up visit', "No follow-up visit"),
        ('No follow-up visit(Foreigner)', "No follow-up visit(Foreigner)"),
        ('No Answer', 'No Answer')
                             )
    Result_TestCure_Choice=(
        ('',''),
        ('Positive','Positive'),
        ('Negative','Negative'),
        ('No TOC Performed', 'No TOC Performed'),
        ('No Answer', 'No Answer'),
        ('N/A', 'N/A')
    )
    NoTOC_ResultofTest=(
        ('',''),
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('No Answer', 'No Answer')
                       )
    Gonnorhea_Treatment_Choice=(
        ('',''),
        ('Medications Prescribed and Provided by Clinic', 'Medications Prescribed and Provided by Clinic'),
        ('Prescribed Medications Only','Prescribed Medications Only' ),
        ('Referred to physician', 'Referred to physician'),
        ('None given', 'None given'),
        ('No Answer', 'No Answer')
    )
    Treatment_Outcome_Choice=(
        ('',''),
        ('Treatment Completed', 'Treatment Completed'),
        ('Partial Treatment Completed','Partial Treatment Completed'),
        ('No Treatment-patient refused', 'No Treatment-patient refused'),
        ('No Treatment-patient didnt come back', 'No Treatment-patient didnt come back' ),
        ('No Answer', 'No Answer')
    )
    Primary_Antibiotics=(
        ('None', 'None'),
        ('CRO IM 250mg', 'Ceftriaxone IM 250mg'),
        ('CRO IM 500mg', 'Ceftriaxone IM 500mg'),
        ('CRO IM 1g', 'Ceftriaxone IM 1g'),
        ('CFM PO 400mg','Cefixime PO 400mg'),
        ('CFM PO 800mg', 'Cefixime PO 800mg'),
        ('AZM PO 1g', 'Azithromycin PO 1g'),
        ('AZM PO 2g', 'Azithromycin PO 2g'),
        ('Other', 'Other'),
        ('Unknown', 'Unknown'),
    )
    Secondary_Antibiotics=(
        ('None','None'),
        ('AZM PO 1g','Azithromycin PO 1g' ),
        ('AZM PO 2g', 'Azithromycin PO 2g'),
        ('DOX PO 100mg', 'Doxycycline PO 100mg'),
        ('TCY PO 500mg', 'Tetracycline PO 500mg'),
        ('Other', 'Other'),
        ('Unknown', 'Unknown')
    )

    OtherDrugsRoute_Choices=(
        ('',''),
        ('Oral', 'Oral'),
        ('Injectable(IV/IM)',"Injectable(IV/IM)"),
        ('Dermal','Dermal'),
        ('Suppository', 'Suppository'),
        ('No Answer', 'No Answer'),
        ('N/A', 'N/A'),
    )
    Pus_cellsChoice=(
        ('',''),
        ('n/a','n/a'),
        ('Negative','Negative'),
        ('Rare','Rare'),
        ('1+','1+'),
        ('2+','2+'),
        ('3+','3+'),
        ('4+','4+'),
    )
    Sp_TypeChoice=(
        ('n/a','n/a'),
        ('Genital Male Urethral','Genital Male Urethral'),
        ('Female Cervical','Female Cervical'),
        ('Pharynx','Pharynx'),
        ('Rectum','Rectum'),
        ('Other','Other'),

    )
    Sp_QualChoice=(
        ('',''),
        ('Acceptable','Acceptable'),
        ('Contaminated','Contaminated'),
        ('Non-viable','Non-viable'),
        ('Improperly Transported','Improperly Transported'),
        ('N/A','N/A'),
    )
    Diagnosis_Choice=(
        ('',''),
        ('Susp gonococcal urethritis','Suspected gonococcal urethritis'),
        ('Susp non-gonococcal urethritis','Suspected non-gonococcal urethritis'),
        ('Other','Other'),
        ('Unknown','Unknown'),
    )
    CultureResult_Choice=(
        ('n/a','n/a'),
        ('Positive','Positive'),
        ('Negative','Negative'),
    )
    OtherInfo_Choice=(
        ('n/a','n/a'),
        ('Positive','+'),
        ('Negative','-'),
        ('No Answer','NA'),
        ('Not Tested','NT'),
        
    )
    
    Country_Choice=(
        ('Philippines','Philippines'),
        ('Other','Other'),
    )
    NAATng_Choice=(
        ('n/a','n/a'),
        ('NG Detected','NG Detected'),
        ('NG non Detected','NG non Detected'),
        ('Invalid','Invalid'),
        ('NAAT not performed','NG not performed'),
    )
    NAATchl_Choice=(
        ('n/a','n/a'),
        ('Chlamydia Detected','Chlamydia Detected'),
        ('Chlamydia non Detected','Chlamydia non Detected'),
        ('Invalid','Invalid'),
        ('NAAT not performed','NG not performed'),
    )

    Country_Choice=(
        ('Philippines','Philippines'),
        ('Other','Other'),
    )
    # DEMOGRAPHIC DATA
    Date_of_Entry =models.DateTimeField(auto_now=True)
    ID_Number = models.CharField(max_length=100, blank=True, default="")
    Egasp_Id = models.CharField(max_length=25,blank=True, unique=True )
    PTIDCode = models.CharField(max_length=100, blank=True)
    Laboratory = models.CharField(max_length=100,blank=True,default='Research Institute for Tropical Medicine')
    Clinic = models.CharField(max_length=100,blank=True,)
    Consult_Date = models.DateField(blank=True, null=True)
    Consult_Type = models.CharField(max_length=100, choices=ConsultTypeChoices, default="")
    Client_Type = models.CharField(max_length=100, choices=ClientTypeChoice, default="")
    Uic_Ptid = models.CharField(max_length=100,blank=True)
    Clinic_Code = models.CharField(max_length=100,blank=True,)
    ClinicCodeGen = models.CharField(max_length=100, blank=True)
    First_Name = models.CharField(max_length=100,blank=True,)
    Middle_Name = models.CharField(max_length=100,blank=True, )
    Last_Name = models.CharField(max_length=100,blank=True,)
    Suffix = models.CharField(max_length=100,blank=True, )
    Birthdate = models.DateField(null=True, blank=True)
    Age = models.CharField(max_length=20,blank=True,)
    Sex = models.CharField(max_length=10,choices=SexatbirthChoice,default="")
    Gender_Identity = models.CharField(max_length=100, choices=GenderChoice, default="")
    Gender_Identity_Other = models.CharField(max_length=100,blank=True, default="n/a" )
    Occupation = models.CharField(max_length=100, blank=True,)
    Civil_Status = models.CharField(max_length=100, choices=Civil_StatusChoice, default="")
    Civil_Status_Other = models.CharField(max_length=100, blank=True, default="n/a")

    Current_Province = models.CharField(max_length=100, null=True, blank=True)
    Current_City = models.CharField(max_length=100, null=True, blank=True)
    Permanent_Province = models.CharField(max_length=100, null=True, blank=True)
    Permanent_City = models.CharField(max_length=100, null=True, blank=True)


    Current_Province_fk = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name="current_province")
    Current_City_fk = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="current_city")
    Permanent_Province_fk = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name="permanent_province")
    Permanent_City_fk = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="permanent_city")

    Permanent_Country = models.CharField(max_length=100, choices=Country_Choice, default='Philippines')
    Current_Country =models.CharField(max_length=100, choices=Country_Choice, default='Philippines')
    PermAdd_same_CurrAdd = models.BooleanField(default=False)   
    Other_Country = models.CharField(max_length=100, blank=True, default='n/a')
    Nationality = models.CharField(max_length=100, choices=Nationality_Choice, default="")
    Nationality_Other = models.CharField(max_length=100,blank=True,default="n/a")
    Travel_History = models.CharField(max_length=100,choices=TravelHistory_Choice, default="")
    Travel_History_Specify= models.CharField(max_length=100,blank=True, default="n/a")

    ## BEHAVIORAL DATA
    Client_Group = models.CharField(max_length=100,choices=Client_Risk_Choice, default="")
    Client_Group_Other = models.CharField(max_length=100,blank=True,default="n/a" )
    History_Of_Sex_Partner = models.CharField(max_length=100, choices=Sex_PartnerChoice, default="")
    Nationality_Sex_Partner = models.CharField(max_length=100, choices=NationalityofPartner_Choice, default="")
    Date_of_Last_Sex = models.DateField(null=True, blank=True)
    Nationality_Sex_Partner_Other = models.CharField(max_length=100,blank=True,default="n/a")
    Number_Of_Sex_Partners= models.CharField(max_length=100,blank=True,)
    Relationship_to_Partners = models.CharField(max_length=100, choices=Relationship_to_partnerChoice, default="")
    SB_Urethral = models.CharField(max_length=100, choices=Common_Choices, default="")
    SB_Vaginal = models.CharField(max_length=100, choices=Common_Choices, default="")
    SB_Anal_Insertive = models.CharField(max_length=100, choices=Common_Choices, default="")
    SB_Oral_Insertive = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sharing_of_Sex_Toys = models.CharField(max_length=100, choices=Common_Choices, default="")
    SB_Oral_Receptive = models.CharField(max_length=100, choices=Common_Choices, default="")
    SB_Anal_Receptive = models.CharField(max_length=100, choices=Common_Choices, default="")
    SB_Others = models.CharField(max_length=100,blank=True, default="n/a" )
    Sti_None = models.CharField(max_length=100,choices=Common_Choices, default="")
    Sti_Hiv = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Hepatitis_B = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Hepatitis_C = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_NGI = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Syphilis = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Chlamydia = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Anogenital_Warts = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Genital_Ulcer = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Herpes= models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Other = models.CharField(max_length=100,blank=True, default="n/a")
    Sti_Trichomoniasis = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Mycoplasma_genitalium = models.CharField(max_length=100, choices=Common_Choices, default="")
    Sti_Lymphogranuloma = models.CharField(max_length=100, choices=Common_Choices, default="")
    
    Illicit_Drug_Use = models.CharField(max_length=100, choices=Illicit_Drug_Use_Choices, default="")
    Illicit_Drug_Specify = models.CharField(max_length=100,blank=True,default="n/a")
    Abx_Use_Prescribed = models.CharField(max_length=100, choices=Common_Choices, default="")
    Abx_Use_Prescribed_Specify = models.CharField(max_length=100,blank=True,default="n/a")
    Abx_Use_Self_Medicated = models.CharField(max_length=100, choices=Common_Choices, default="")
    Abx_Use_Self_Medicated_Specify = models.CharField(max_length=100,blank=True,default="n/a")
    Abx_Use_None = models.CharField(max_length=100, choices=Common_Choices, default="")
    Abx_Use_Other = models.CharField(max_length=100, choices=Common_Choices, default="")
    Abx_Use_Other_Specify = models.CharField(max_length=100,blank=True,default="n/a")
    
    #ROUTE OF ADMINISTRATION
    Route_Oral = models.CharField(max_length=100, choices=Common_Choices, default="")
    Route_Injectable_IV= models.CharField(max_length=100, choices=Common_Choices, default="")
    Route_Dermal= models.CharField(max_length=100, choices=Common_Choices, default="")
    Route_Suppository= models.CharField(max_length=100, choices=Common_Choices, default="")
    Route_Other= models.CharField(max_length=100,blank=True,default="n/a" )

    #MEDICAL HISTORY
    Symp_With_Discharge = models.CharField(max_length=100, choices=Symp_Gonorrhoea_Choice, default="")
    Symp_No = models.CharField(max_length=100, choices=Common_Choices, default="")
    Symp_Discharge_Urethra = models.CharField(max_length=100, choices=Common_Choices, default="")
    Symp_Discharge_Vagina = models.CharField(max_length=100, choices=Common_Choices, default="")
    Symp_Discharge_Anus = models.CharField(max_length=100, choices=Common_Choices, default="")
    Symp_Discharge_Oropharyngeal = models.CharField(max_length=100, choices=Common_Choices, default="")
    Symp_Pain_Lower_Abdomen = models.CharField(max_length=100, choices=Common_Choices, default="")
    Symp_Tender_Testicles = models.CharField(max_length=100, choices=Common_Choices, default="")
    Symp_Painful_Urination = models.CharField(max_length=100,  choices=Common_Choices, default="")
    Symp_Painful_Intercourse = models.CharField(max_length=100, choices=Common_Choices, default="")
    Symp_Rectal_Pain = models.CharField(max_length=100, choices=Common_Choices, default="")
    Symp_Other = models.CharField(max_length=100,blank=True,default="n/a")
    Outcome_Of_Follow_Up_Visit = models.CharField(max_length=100, choices=Outcome_Followup_Choice, default="")
    Prev_Test_Pos = models.CharField(max_length=100,choices=Common_Choices, default="")
    Prev_Test_Pos_Date = models.CharField(max_length=100,blank=True, default="")
    Result_Test_Cure_Initial = models.CharField(max_length=100, choices=Result_TestCure_Choice,default="")
    Result_Test_Cure_Followup = models.CharField(max_length=100,choices=Result_TestCure_Choice, default="" )
    NoTOC_Other_Test = models.CharField(max_length=100,blank=True, default="n/a")
    NoTOC_DatePerformed = models.DateField(null= True, blank=True, )
    NoTOC_Result_of_Test = models.CharField(max_length=100, blank=True)
    Patient_Compliance_Antibiotics = models.CharField(max_length=100, choices=Common_Choices, default="")
    OtherDrugs_Specify= models.CharField(max_length=100,blank=True, )
    OtherDrugs_Dosage = models.CharField(max_length=100,blank=True, )
    OtherDrugs_Route = models.CharField(max_length=100, choices=OtherDrugsRoute_Choices, default="")
    OtherDrugs_Duration= models.CharField(max_length=100,  blank=True,)


    #treatment information
    Gonorrhea_Treatment = models.CharField(max_length=100, choices=Gonnorhea_Treatment_Choice, default="")
    Treatment_Outcome = models.CharField(max_length=100, choices=Treatment_Outcome_Choice, default="")
    Primary_Antibiotic = models.CharField(max_length=100, choices=Primary_Antibiotics, default="None")
    Primary_Abx_Other = models.CharField(max_length=100,blank=True, default="n/a")
    Secondary_Antibiotic = models.CharField(max_length=100, choices=Secondary_Antibiotics, default="None")
    Secondary_Abx_Other = models.CharField(max_length=100,blank=True, default="n/a")
    Notes = models.TextField(blank=True, max_length=255,)
    
    Clinic_Staff = models.CharField(max_length=100,blank=True,null=True,default="")
    Requesting_Physician = models.CharField(max_length=100,blank=True,null=True,default="")
    Telephone_Number = models.CharField(max_length=100,blank=True,default="")
    Email_Address = models.EmailField(max_length=100, blank=True, null=True, validators=[EmailValidator()])
    Date_Accomplished_Clinic = models.DateField(blank=True, null=True, auto_now = False)
    Date_Requested_Clinic = models.DateField(blank=True, null=True)
   


## Laboratory Results TAB
    Date_Specimen_Collection = models.DateField(null= True, blank=True)
    Specimen_Code = models.CharField(max_length=5, blank=True, null=True)
    Specimen_Type = models.CharField(max_length=100, choices=Sp_TypeChoice, default="Genital Male Urethral")
    Specimen_Quality = models.CharField(max_length=100, choices=Sp_QualChoice, default="")
    Date_Of_Gram_Stain = models.DateField( null=True, blank=True, )
    Diagnosis_At_This_Visit = models.CharField(max_length=100, choices=Diagnosis_Choice, default="")
    Gram_Neg_Intracellular = models.CharField(max_length=100, choices=Pus_cellsChoice, default="n/a")
    Gram_Neg_Extracellular = models.CharField(max_length=100, choices=Pus_cellsChoice,default="n/a")
    Gs_Presence_Of_Pus_Cells = models.CharField(max_length=100, choices=Common_Choices, default="")
    Presence_GN_Intracellular=models.CharField(max_length=100,choices=Common_Choices, default="")
    Presence_GN_Extracellular=models.CharField(max_length=100, choices=Common_Choices, default="")
    GS_Pus_Cells=models.CharField(max_length=100, choices=Pus_cellsChoice, default="n/a")
    Epithelial_Cells = models.CharField(max_length=100, choices=Pus_cellsChoice, default="n/a")
    GS_Date_Released = models.DateField( null= True, blank=True, )
    
    GS_Others = models.CharField(max_length=255, blank=True, default="" )
    GS_Other_sp = models.CharField(max_length=100, choices=Pus_cellsChoice, default="")
    
    GS_Others2 = models.CharField(max_length=255, blank=True, default="" )
    GS_Other_sp2 = models.CharField(max_length=100, choices=Pus_cellsChoice, default="")
    
    GS_Others3 = models.CharField(max_length=255, blank=True, default="" )
    GS_Other_sp3 = models.CharField(max_length=100, choices=Pus_cellsChoice, default="")
    
    GS_Negative=models.CharField(max_length=100, choices=Common_Choices, )
    Gs_Gram_neg_diplococcus=models.CharField(max_length=100, choices=Common_Choices, default="")
    Gs_NoGram_neg_diplococcus=models.CharField(max_length=100,choices=Common_Choices, default="")
    Gs_Not_performed=models.CharField(max_length=100, choices=Common_Choices, default="")
    Date_Received_in_lab = models.DateField( null= True,  blank=True, )
    Positive_Culture_Date = models.DateField(null= True, blank=True, )
    Culture_Result = models.CharField(max_length=100, choices=CultureResult_Choice, default="n/a")
    Growth = models.CharField(max_length=100,blank=True,)
    Growth_span = models.CharField(max_length=255, blank=True)
    Growth_span_other = models.CharField(max_length=255, blank=True)
    
    Species_Identification = models.CharField(max_length=100, choices=SpeciesChoices, default="n/a")
    Other_species_ID=models.CharField(max_length=100,blank=True,default="n/a" )
    Specimen_Quality_Cs = models.CharField(max_length=100,choices=Sp_QualChoice, default="n/a")
    Susceptibility_Testing_Date = models.DateField(null=True, blank=True)
    Retested_Mic = models.CharField(max_length=100, choices=Common_Choices, default="")
    Confirmation_Ast_Date = models.DateField(null= True, blank=True)

    NAAT_ng= models.CharField(max_length=100,choices=NAATng_Choice, default="n/a")
    NAAT_chl= models.CharField(max_length=100,choices=NAATchl_Choice, default="n/a")
    Beta_Lactamase=models.CharField(max_length=100, choices=OtherInfo_Choice, default="n/a")
    PPng=models.CharField(max_length=100, choices=OtherInfo_Choice, default="n/a")
    TRng=models.CharField(max_length=100, choices=OtherInfo_Choice, default="n/a")
    Date_Released = models.DateField(blank=True, null=True)
    For_possible_WGS=models.CharField(max_length=101, choices=Common_Choices, default="n/a")
    Date_stocked=models.DateField(blank=True, null=True)
    Location=models.CharField(max_length=103,blank=True,)
    abx_code=models.CharField(max_length=25, blank=True, )
    #laboratory personnel
    Laboratory_Staff = models.CharField(max_length=100,blank=True, null=True,)
    Date_Accomplished_ARSP=models.DateField(blank=True, null=True)
    ars_notes = models.TextField(blank=True, max_length=255, null=True)
    ars_contact = models.CharField(max_length=27, blank=True, null=True)
    ars_email = models.EmailField(blank=True, null=True, validators=[EmailValidator()])
    ars_license = models.CharField(max_length=100,blank=True, null=True, default="")
    ars_designation = models.CharField(max_length=100,blank=True, null=True, default="")
    Validator_Pers = models.CharField(max_length=100,blank=True, null=True,)
    Date_Validated_ARSP=models.DateField(blank=True, null=True)
    val_contact = models.CharField(max_length=27,blank=True, null=True)
    val_email = models.EmailField(blank=True, null=True, validators=[EmailValidator()])
    val_license = models.CharField(max_length=100,blank=True, null=True, default="")
    val_designation =  models.CharField(max_length=100,blank=True, null=True, default="")

    def __str__(self):
        return self.Egasp_Id
    
    def formatted_number(self):
        return self.Telephone_Number.as_e164  # Returns the number in +639XXXXXXX format
    
    def __str__(self):
        return f"Current: {self.Current_City}, {self.Current_Province} | Permanent: {self.Permanent_City}, {self.Permanent_Province}"


    # to dissallow duplicates
    def clean(self):
        if self.Egasp_Id:
            if Egasp_Data.objects.filter(Egasp_Id=self.Egasp_Id).exclude(pk=self.pk).exists():
                raise ValidationError({'Egasp_Id': 'Egasp_Id must be unique.'})
    
    def save(self, *args, **kwargs):
        if self.Current_Province_fk:
            self.Current_Province = self.Current_Province_fk.provincename
        if self.Current_City_fk:
            self.Current_City = self.Current_City_fk.cityname
        if self.Permanent_Province_fk:
            self.Permanent_Province = self.Permanent_Province_fk.provincename
        if self.Permanent_City_fk:
            self.Permanent_City = self.Permanent_City_fk.cityname

        super().save(*args, **kwargs)

class Meta:
    db_table ="Egasp_Data"

    

# for specific indexing use this to enable fast search
    indexes = [
                models.Index(fields=['Egasp_Id']),  # Index for field1
                models.Index(fields=['Uic_Ptid']),  # Index for field2
                models.Index(fields=['First_Name']),  # Index for field3
                models.Index(fields=['Last_Name']),  # Index for field4
                # add more indexes as needed
            ]

class ClinicData(models.Model):
    PTIDCode=models.CharField(max_length=2, blank=True, unique=True)
    ClinicCode=models.CharField(max_length=3, blank=True)
    ClinicName=models.CharField(max_length=155, blank=True)
    def __str__(self):
        return self.PTIDCode  
    
class Meta:
    db_table ="ClinicData"



class BreakpointsTable(models.Model):
    TestMethodChoices =(
        ('DISK', 'DISK'),
        ('MIC','MIC'),
    )
    
    GuidelineChoices = (
        ('CLSI', 'CLSI'),        
    )

    Guidelines = models.CharField(max_length=100, choices=GuidelineChoices, blank=True, default="")
    Test_Method = models.CharField(max_length=20, choices=TestMethodChoices, blank=True, default="")
    Potency = models.CharField(max_length=5, blank=True, default="")
    Abx_code = models.CharField(max_length=15, blank=True, default="")
    Tier = models.CharField(max_length=10, blank=True, default="")
    Show = models.BooleanField(default=True)
    Retest = models.BooleanField(default=False)
    Antibiotic = models.CharField(max_length=100, blank=True, default="")
    Whonet_Abx = models.CharField(max_length=100, blank=True, default="")
    Disk_Abx = models.BooleanField(default=False)
    R_val = models.CharField(max_length=30, blank=True, default="")
    I_val = models.CharField(max_length=30, blank=True, default="")
    SDD_val = models.CharField(max_length=30, blank=True, default="")
    S_val = models.CharField(max_length=30, blank=True, default="")
    Alert_val = models.CharField(max_length=30, blank=True, default="")
    Alert_cln = models.CharField(max_length=30, blank=True, default="")
    Date_Modified = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Abx_code 

class Meta:
    db_table ="BreakpointsTable"


class Breakpoint_upload(models.Model):
    File_uploadBP = models.FileField(upload_to='uploads/breakpoints/', null=True, blank=True)

class Meta:
    db_table = "Breakpoint_upload"

    
#for antibiotic test entries
class AntibioticEntry(models.Model):
      
    ab_idNumber_egasp = models.ForeignKey(Egasp_Data, on_delete=models.CASCADE, null=True, related_name='antibiotic_entries')
    ab_breakpoints_id = models.ManyToManyField(BreakpointsTable, max_length=6)
    ab_EgaspId= models.CharField(max_length=100, blank=True, null=True)
    
   
    ab_Antibiotic = models.CharField(max_length=100, blank=True, null=True)
    ab_Abx_code= models.CharField(max_length=100, blank=True, null=True)
    ab_Abx=models.CharField(max_length=100, blank=True, null=True)

    ab_Disk_value = models.IntegerField(blank=True, null=True)
    ab_Disk_RIS = models.CharField(max_length=4, blank=True)
    ab_MIC_operand=models.CharField(max_length=4, blank=True, null=True, default="")
    ab_MIC_value = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    ab_MIC_RIS = models.CharField(max_length=4, blank=True)
    ab_AlertMIC = models.BooleanField(default=False)
    ab_Alert_val = models.CharField(max_length=30, blank=True, null=True, default="")

    ab_Retest_Antibiotic = models.CharField(max_length=100, blank=True, null=True)
    ab_Retest_Abx_code = models.CharField(max_length=100, blank=True, null=True)
    ab_Retest_Abx = models.CharField(max_length=100, blank=True, null=True)
    ab_Retest_DiskValue = models.IntegerField(blank=True, null=True)
    ab_Retest_Disk_RIS = models.CharField(max_length=4, blank=True)
    ab_Retest_MIC_operand=models.CharField(max_length=4, blank=True, null=True, default="")
    ab_Retest_MICValue = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    ab_Retest_MIC_RIS = models.CharField(max_length=4, blank=True)
    ab_Retest_AlertMIC = models.BooleanField(default=False)
    ab_Retest_Alert_val = models.CharField(max_length=30, blank=True, null=True, default="")
    
    
    ab_R_breakpoint = models.CharField(max_length=10, blank=True, null=True)
    ab_I_breakpoint = models.CharField(max_length=10, blank=True, null=True)
    ab_SDD_breakpoint = models.CharField(max_length=10, blank=True, null=True)  
    ab_S_breakpoint = models.CharField(max_length=10, blank=True, null=True)

    ab_Ret_R_breakpoint = models.CharField(max_length=10, blank=True, null=True)
    ab_Ret_I_breakpoint = models.CharField(max_length=10, blank=True, null=True)
    ab_Ret_SDD_breakpoint = models.CharField(max_length=10, blank=True, null=True)
    ab_Ret_S_breakpoint = models.CharField(max_length=10, blank=True, null=True)    

    # #for joining of operand and MIC values
    # ab_MICjoined = models.CharField(max_length=7, blank=True, null=True)    
    def __str__(self):
        return ", ".join([abx.Whonet_Abx for abx in self.ab_breakpoints_id.all()]) 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the instance first
        

    class Meta:
        db_table = "AntibioticEntry"


class SpecimenTypeModel(models.Model):
    Specimen_name = models.CharField(max_length=100, blank=True, null=True)
    Specimen_code = models.CharField(max_length=4, blank=True, null=True)
    def __str__(self):
        return self.Specimen_code 

class Meta:
    db_table = "SpecimenTypeTable"


# Address Book used in Laboratory Personnel Providing Information
class Clinic_Staff_Details(models.Model):
    ClinStaff_Name = models.CharField(max_length=100, blank=True, null=True)
    ClinStaff_License= models.CharField(max_length=100, blank=True, null=True)
    ClinStaff_Designation= models.CharField(max_length=150, blank=True, null=True)
    ClinStaff_Email = models.EmailField(max_length=100, blank=True, null=True, validators=[EmailValidator()])
    ClinStaff_Contact = models.CharField(max_length=27, blank=True, null=True)

    def __str__(self):
        return self.ClinStaff_Name if self.ClinStaff_Name else ""




class Clinic_Pers_Other(models.Model):
    Pers_Name = models.CharField(max_length=100, blank=True, null=True)
    Pers_License= models.CharField(max_length=100, blank=True, null=True)
    Pers_Designation= models.CharField(max_length=150, blank=True, null=True)
    Pers_Email = models.EmailField(max_length=100, blank=True, null=True, validators=[EmailValidator()])
    Pers_Contact = models.CharField(max_length=27, blank=True, null=True)

    def __str__(self):
        return self.Pers_Name if self.Pers_Name else ""