# -*- encoding: utf-8 -*-
import os
from django.conf import settings
from django.templatetags.static import static
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404 
from django.template import loader
from django.db.models import Prefetch
from .models import *
from .forms import *
# imports for generating pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.templatetags.static import static
from reportlab.lib.units import cm
# for paginator
from django.core.paginator import Paginator
# for dropdown items
from django.contrib import messages
#to auto generate clinic_code, egasp id and clinic
from django.http import JsonResponse, FileResponse
#for importation 
import pandas as pd
from django.utils import timezone
from django.db.models import Q
from django.utils.timezone import now
import csv
from io import TextIOWrapper


@login_required(login_url="/login/")
def index(request):
    isolates = Egasp_Data.objects.all().order_by('-Date_of_Entry')

    # Count per clinic
    tly_count = Egasp_Data.objects.filter(Clinic_Code='TLY').count()
    psh_count = Egasp_Data.objects.filter(Clinic_Code='PSH').count()
    tsh_count = Egasp_Data.objects.filter(Clinic_Code='TSH').count()
    
    # Count per city (assuming you have a 'Current_City' field)
    record_count = Egasp_Data.objects.values('Egasp_Id').distinct().count()

    # Count per sex
    male_count = Egasp_Data.objects.filter(Sex='Male').count()
    female_count = Egasp_Data.objects.filter(Sex='Female').count()

    # Count per age group
    age_0_18 = Egasp_Data.objects.filter(Age__lte=18).count()
    age_19_35 = Egasp_Data.objects.filter(Age__range=(19, 35)).count()
    age_36_60 = Egasp_Data.objects.filter(Age__range=(36, 60)).count()
    age_60_plus = Egasp_Data.objects.filter(Age__gte=61).count()

    # Include all context variables
    context = {
        'isolates' : isolates,
        'tly_count': tly_count,
        'psh_count': psh_count,
        'tsh_count': tsh_count,
        'record_count': record_count,
        'male_count': male_count,
        'female_count': female_count,
        'age_0_18': age_0_18,
        'age_19_35': age_19_35,
        'age_36_60': age_36_60,
        'age_60_plus': age_60_plus,
    }

    return render(request, 'home/index.html', context)






@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        # Redirect to a different view or render a different template
        return redirect('home')  # Redirect to the home view or any other view

    except Exception as e:
        # Log the exception if needed
        print(f"Error: {e}")
        # Redirect to a different view or render a different template
        return redirect('home')  # Redirect to the home view or any other view

# Adding Data view
@login_required(login_url="/login/")
def crf_data(request):
    # Fetch only antibiotics where 'Show' is True
    whonet_abx_data = BreakpointsTable.objects.filter(Show=True)
    # Fetch only retest-related antibiotics
    whonet_retest_data = BreakpointsTable.objects.filter(Retest=True)
    if request.method == "POST":
        form = egasp_Form(request.POST)
        if form.is_valid():
            # Save the main form first
            egasp_instance = form.save(commit=False)
            lab_staff = form.cleaned_data.get('Laboratory_Staff')
            validator = form.cleaned_data.get('Validator_Pers')
          

            if lab_staff:
                egasp_instance.ars_license = lab_staff.ClinStaff_License
                egasp_instance.ars_designation = lab_staff.ClinStaff_Designation
                
            if  validator:
                egasp_instance.val_license = validator.ClinStaff_License
                egasp_instance.val_designation = validator.ClinStaff_Designation
         
            if egasp_instance.Clinic_Staff is None: # if None, dont put N/A put an Empty string
                egasp_instance.Clinic_Staff = ""
            
            if egasp_instance.Requesting_Physician is None:
                egasp_instance.Requesting_Physician = ""

            egasp_instance.save()
            
            # Loop through `whonet_abx_data` to save the related antibiotics
            for entry in whonet_abx_data:
                abx_code = entry.Whonet_Abx  # `Abx_code` from`BreakpointsTable`
                
                # Get user input values for disk & MIC
                if entry.Disk_Abx:
                    disk_value = request.POST.get(f'disk_{entry.id}')
                    mic_value = ''
                    mic_operand = ''
                    alert_mic = False

                else:
                    mic_value = request.POST.get(f'mic_{entry.id}')
                    mic_operand = request.POST.get(f'mic_operand_{entry.id}')
                    alert_mic = f'alert_mic_{entry.id}' in request.POST
                    disk_value = ''

                mic_operand = mic_operand if mic_operand else ""
        # Create the AntibioticEntry object **without** retest values yet
                antibiotic_entry = AntibioticEntry.objects.create(
                    ab_idNumber_egasp=egasp_instance,
                    ab_EgaspId=egasp_instance.Egasp_Id,
                    ab_Antibiotic = entry.Antibiotic,
                    ab_Abx = entry.Abx_code,
                    ab_Abx_code=abx_code,  
                    ab_Disk_value = int(disk_value) if disk_value and disk_value.strip().isdigit() else None,
                    ab_MIC_value=mic_value or None,
                    ab_MIC_operand=mic_operand or '',
                    ab_R_breakpoint=entry.R_val or None,
                    ab_I_breakpoint=entry.I_val or None,
                    ab_SDD_breakpoint=entry.SDD_val or None,
                    ab_S_breakpoint=entry.S_val or None,
                    ab_AlertMIC = alert_mic,
                    ab_Alert_val = entry.Alert_val if alert_mic else '',
                )
                # Link to BreakpointsTable
                antibiotic_entry.ab_breakpoints_id.set([entry])

            # Separate loop for **retest** data so it’s handled correctly
            for retest in whonet_retest_data:
                retest_abx_code = retest.Whonet_Abx  # Use retest-specific Abx_code

                # Get retest values
                if retest.Disk_Abx:
                    retest_disk_value = request.POST.get(f'retest_disk_{retest.id}')
                    retest_mic_value = ''
                    retest_mic_operand = ''
                    retest_alert_mic = False
                else:
                    retest_mic_value = request.POST.get(f'retest_mic_{retest.id}')
                    retest_mic_operand = request.POST.get(f'retest_mic_operand_{retest.id}')
                    retest_alert_mic = f'retest_alert_mic_{retest.id}' in request.POST
                    retest_disk_value = ''
                
                retest_mic_operand = retest_mic_operand if retest_mic_operand else ""
                # Create a new AntibioticEntry **only if values exist**
                if retest_disk_value or retest_mic_value:
                    retest_entry = AntibioticEntry.objects.create(
                        ab_idNumber_egasp=egasp_instance,
                        ab_Retest_Abx_code=retest_abx_code,  
                        ab_Retest_DiskValue=int(retest_disk_value) if retest_disk_value and retest_disk_value.strip().isdigit() else None,
                        ab_Retest_MICValue=retest_mic_value or None,
                        ab_Retest_MIC_operand=retest_mic_operand or '',
                        ab_Retest_Antibiotic=retest.Antibiotic,
                        ab_Retest_Abx=retest.Abx_code,
                        ab_Ret_R_breakpoint = retest.R_val or None,
                        ab_Ret_I_breakpoint = retest.I_val or None,
                        ab_Ret_SDD_breakpoint = retest.SDD_val or None,
                        ab_Ret_S_breakpoint = retest.S_val or None,
                        ab_Retest_AlertMIC = retest_alert_mic,
                        ab_Retest_Alert_val = retest.Alert_val if retest_alert_mic else '',
                    )
                    retest_entry.ab_breakpoints_id.set([retest])

            messages.success(request, 'Added Successfully')
            return redirect('show_data')

        else:
            messages.error(request, 'Error / Adding Unsuccessful')
            print(form.errors)

    else:
        form = egasp_Form()

    return render(request, 'home/crf_form.html', {
        'form': form,
        'whonet_abx_data': whonet_abx_data,
        'whonet_retest_data': whonet_retest_data
    })


@login_required(login_url="/login/")
#with sorting function
def show_data(request):
    sort_by = request.GET.get('sort', 'Date_of_Entry')  # Default sort field
    order = request.GET.get('order', 'desc')  # Default sort order

    sort_field = f"-{sort_by}" if order == 'desc' else sort_by

    isolates = Egasp_Data.objects.prefetch_related(
        'antibiotic_entries'
    ).order_by(sort_field)

    paginator = Paginator(isolates, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'current_sort': sort_by,
        'current_order': order,
    }

    return render(request, 'home/tables.html', context)


@login_required(login_url="/login/")
def edit_data(request, id):
    # Fetch the Egasp_Data instance to edit
    isolates = get_object_or_404(Egasp_Data, pk=id)

    # --- Province/City fix for edit mode ---
    # This ensures that the form fields are populated with the correct Province and City instances
    # Province fix
    if isinstance(isolates.Current_Province_fk, str):
        isolates.Current_Province_fk = Province.objects.filter(provincename=isolates.Current_Province_fk).first()

    if isinstance(isolates.Permanent_Province_fk, str):
        isolates.Permanent_Province = Province.objects.filter(provincename=isolates.Permanent_Province_fk).first()

    # City fix
    if isinstance(isolates.Current_City_fk, str):
        isolates.Current_City = City.objects.filter(cityname=isolates.Current_City_fk).first()

    if isinstance(isolates.Permanent_City_fk, str):
        isolates.Permanent_City = City.objects.filter(cityname=isolates.Permanent_City_fk).first()


    # Fetch related data for antibiotics
  
    whonet_abx_data = BreakpointsTable.objects.filter(Show=True)
    whonet_retest_data = BreakpointsTable.objects.filter(Retest=True)

    if request.method == 'POST':
        # Print received data for debugging
        print("POST Data:", request.POST)

        form = egasp_Form(request.POST, instance=isolates)
        if form.is_valid():
            # Save the main form first
            egasp_instance = form.save(commit=False)
            lab_staff = form.cleaned_data.get('Laboratory_Staff')
            validator = form.cleaned_data.get('Validator_Pers')
            if lab_staff:
                egasp_instance.ars_license = lab_staff.ClinStaff_License
                egasp_instance.ars_designation = lab_staff.ClinStaff_Designation
            if  validator:
                egasp_instance.val_license = validator.ClinStaff_License
                egasp_instance.val_designation = validator.ClinStaff_Designation
            
            if egasp_instance.Clinic_Staff is None:
                egasp_instance.Clinic_Staff = ""
            
            if egasp_instance.Requesting_Physician is None:
                egasp_instance.Requesting_Physician = ""

            egasp_instance.save()

            # Update or Create Antibiotic Entries (whonet_abx_data)
            for entry in whonet_abx_data:
                abx_code = entry.Whonet_Abx

                # Fetch user input values for MIC and Disk
                if entry.Disk_Abx:
                    disk_value = request.POST.get(f'disk_{entry.id}')
                    mic_value = ''
                    mic_operand = ''
                    alert_mic = False  
                else:
                    mic_value = request.POST.get(f'mic_{entry.id}')
                    mic_operand = request.POST.get(f'mic_operand_{entry.id}')
                    alert_mic = f'alert_mic_{entry.id}' in request.POST
                    disk_value = ''
                
                # Check and update mic_operand if needed
                mic_operand = mic_operand.strip() if mic_operand else ''

                # Convert `disk_value` safely
                disk_value = int(disk_value) if disk_value and disk_value.strip().isdigit() else None

                # Debugging: Print the values before saving
                print(f"Saving values for Antibiotic Entry {entry.id}:", {
                    'mic_operand': mic_operand,
                    'disk_value': disk_value,
                    'mic_value': mic_value,
                })
                
                # Get or create antibiotic entry
                antibiotic_entry, created = AntibioticEntry.objects.update_or_create(
                    ab_idNumber_egasp=egasp_instance,
                    ab_Abx_code=abx_code,
                    defaults={
                        "ab_EgaspId": egasp_instance.Egasp_Id,
                        "ab_Antibiotic": entry.Antibiotic,
                        "ab_Abx": entry.Abx_code,
                        "ab_Disk_value": disk_value,
                        "ab_MIC_value": mic_value or None,
                        "ab_MIC_operand": mic_operand,
                        "ab_R_breakpoint": entry.R_val or None,
                        "ab_I_breakpoint": entry.I_val or None,
                        "ab_SDD_breakpoint": entry.SDD_val or None,
                        "ab_S_breakpoint": entry.S_val or None,
                        "ab_AlertMIC": alert_mic,
                        "ab_Alert_val": entry.Alert_val if alert_mic else '',
                    }
                )

                antibiotic_entry.ab_breakpoints_id.set([entry.pk])
                
                # update RIS fields where disk or mic values are deleted during editing
                if not disk_value and not mic_value:
                    antibiotic_entry.ab_Disk_RIS = ''
                    antibiotic_entry.ab_MIC_RIS = ''
                    antibiotic_entry.save(update_fields=['ab_Disk_RIS', 'ab_MIC_RIS'])

            # Separate loop for Retest Data
            for retest in whonet_retest_data:
                retest_abx_code = retest.Whonet_Abx

                # Fetch user input values for MIC and Disk
                if retest.Disk_Abx:
                    retest_disk_value = request.POST.get(f'retest_disk_{retest.id}')
                    retest_mic_value = ''
                    retest_mic_operand = ''
                    retest_alert_mic = False
                else:
                    retest_mic_value = request.POST.get(f'retest_mic_{retest.id}')
                    retest_mic_operand = request.POST.get(f'retest_mic_operand_{retest.id}')
                    retest_alert_mic = f'retest_alert_mic_{retest.id}' in request.POST
                    retest_disk_value = ''

                # Check and update retest mic_operand if needed
                retest_mic_operand = retest_mic_operand.strip() if retest_mic_operand else ''

                # Convert `retest_disk_value` safely
                retest_disk_value = int(retest_disk_value) if retest_disk_value and retest_disk_value.strip().isdigit() else None

                # Debugging: Print the values before saving
                print(f"Saving values for Retest Entry {retest.id}:", {
                    'retest_mic_operand': retest_mic_operand,
                    'retest_disk_value': retest_disk_value,
                    'retest_mic_value': retest_mic_value,
                    'retest_alert_mic': retest_alert_mic,
                    'retest_alert_val': retest.Alert_val if retest_alert_mic else '',
                })

                # Get or update retest antibiotic entry
                retest_entry, created = AntibioticEntry.objects.update_or_create(
                    ab_idNumber_egasp=egasp_instance,
                    ab_Retest_Abx_code=retest_abx_code,
                    defaults={
                        "ab_Retest_DiskValue": retest_disk_value,
                        "ab_Retest_MICValue": retest_mic_value or None,
                        "ab_Retest_MIC_operand": retest_mic_operand,
                        "ab_Retest_Antibiotic": retest.Antibiotic,
                        "ab_Retest_Abx": retest.Abx_code,
                        "ab_Ret_R_breakpoint": retest.R_val or None,
                        "ab_Ret_S_breakpoint": retest.S_val or None,
                        "ab_Ret_SDD_breakpoint": retest.SDD_val or None,
                        "ab_Ret_I_breakpoint": retest.I_val or None,
                        "ab_Retest_AlertMIC": retest_alert_mic,
                        "ab_Retest_Alert_val": retest.Alert_val if retest_alert_mic else '',
                    }
                )

                retest_entry.ab_breakpoints_id.set([retest.pk])
            
            # update RIS fields where disk or mic values are deleted during editing
                if not retest_disk_value and not retest_mic_value:
                    retest_entry.ab_Retest_Disk_RIS = ''
                    retest_entry.ab_Retest_MIC_RIS = ''
                    retest_entry.save(update_fields=['ab_Retest_Disk_RIS', 'ab_Retest_MIC_RIS'])

            messages.success(request, 'Data updated successfully')
            return redirect('/show/')

        else:
            messages.error(request, 'There was an error with your form')
            print(form.errors)

    else:
        form = egasp_Form(instance=isolates)

    # Fetch all entries in one query
    all_entries = AntibioticEntry.objects.filter(ab_idNumber_egasp=isolates)

    # Separate them based on the 'retest' condition
    existing_entries = all_entries.filter(ab_Retest_Abx_code__isnull=True)  # Regular entries
    retest_entries = all_entries.filter(ab_Retest_Abx_code__isnull=False)   # Retest entries

    context = {
        'isolates': isolates,
        'form': form,
        'whonet_abx_data': whonet_abx_data,
        'whonet_retest_data': whonet_retest_data,
        'existing_entries': existing_entries,
        'retest_entries': retest_entries,
    
    }
    return render(request, 'home/edit.html', context)



#Deleting Data
@login_required(login_url="/login/")
def delete_data(request, id):
    isolate = get_object_or_404(Egasp_Data, pk=id)
    isolate.delete()
    return redirect('show_data')


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access images and static files.
    """
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Path to static folder
    mUrl = settings.MEDIA_URL       # Typically /media/
    mRoot = settings.MEDIA_ROOT     # Path to media folder

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # Absolute URL (http://...)

    if not os.path.isfile(path):
        raise Exception('File not found: %s' % path)

    return path


@login_required(login_url="/login/")
def generate_pdf(request, id):
    # Get the record from the database using the provided ID
    isolate = get_object_or_404(Egasp_Data, pk=id)
    
    # Fetch related antibiotic entries
    antibiotic_entries = AntibioticEntry.objects.filter(ab_idNumber_egasp=isolate)

    # Debugging: Print antibiotic entries to verify data
    print("Antibiotic Entries Count:", antibiotic_entries.count())
    for entry in antibiotic_entries:
        print("Antibiotic Entry:", entry.ab_Abx_code, entry.ab_Disk_value, entry.ab_MIC_value, entry.ab_Retest_MICValue)

    # Use the static URL for the logo
    logo_path = static("assets/img/brand/arsplogo.jpg")

    # Debugging: Check if the logo file exists
    absolute_logo_path = os.path.join(settings.STATIC_ROOT, "assets/img/brand/arsplogo.jpg").replace("\\", "/").strip()
    if not os.path.exists(absolute_logo_path):
        print(f"Logo file not found at: {absolute_logo_path}")
        logo_path = ""  # Set to None if the file does not exist

    context = {
        'isolate': isolate,
        'antibiotic_entries': antibiotic_entries,
        'now': timezone.now(),  # Add current time to context
        'logo_path': logo_path,  # Use the static URL
    }
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    # Name the PDF for download or preview
    response['Content-Disposition'] = 'filename="Lab_Result_Report.pdf"'
    
    # Find the template and render it
    template_path = 'home/Lab_result.html'
    template = get_template(template_path)
    html = template.render(context)

    # Debugging: Print rendered HTML to verify template rendering
    print("Rendered HTML:", html[:500])  # Print the first 500 characters of the rendered HTML

    # Generate PDF using Pisa
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    # Check for errors during PDF generation
    if pisa_status.err:
        print("Pisa Error:", pisa_status.err)
        return HttpResponse(f'Error in generating PDF: {html}')
    
    return response



@login_required(login_url="/login/")
# generate gram stain
def generate_gs(request, id):
    # Get the record from the database using the provided ID
    try:
        isolate = Egasp_Data.objects.get(pk=id)
        antibiotic_entries = AntibioticEntry.objects.filter(ab_idNumber_egasp=isolate).order_by('ab_Antibiotic')
    except Egasp_Data.DoesNotExist:
        return HttpResponse("Error: Data not found.", status=404)
    
      # Debugging: Print antibiotic entries to verify data
    print("Antibiotic Entries Count:", antibiotic_entries.count())
    for entry in antibiotic_entries:
        print("Antibiotic Entry:", entry.ab_Abx_code, entry.ab_Disk_value, entry.ab_MIC_value, entry.ab_Retest_MICValue)

     # Use the static URL for the logo
    logo_path = static("assets/img/brand/arsplogo.jpg")

    # Debugging: Check if the logo file exists
    absolute_logo_path = os.path.join(settings.STATIC_ROOT, "assets/img/brand/arsplogo.jpg").replace("\\", "/").strip()
    if not os.path.exists(absolute_logo_path):
        print(f"Logo file not found at: {absolute_logo_path}")
        logo_path = ""  # Set to None if the file does not exist

    # Context data to pass to the template
    context = {
        'isolate': isolate,
        'antibiotic_entries': antibiotic_entries,
        'now': timezone.now(),  # Current timestamp
        'logo_path': logo_path,  # Use the static URL
    }

    # Create a Django response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Gram_Stain_Report.pdf"'

    # Load and render the template
    template_path = 'home/GS_result.html'  # Adjust if needed
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF using Pisa
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    # Check for errors
    if pisa_status.err:
        return HttpResponse(f'Error generating PDF: {html}')

    return response




@login_required(login_url="/login/")
# for Quick search
def search(request):
   query = request.GET.get('q')
   items = Egasp_Data.objects.filter(Egasp_Id__icontains=query).order_by('Egasp_Id')
   return render (request, 'home/search_results.html',{'items': items, 'query':query})



@login_required(login_url="/login/")
# FOR DROPDOWN ITEMS (Clinic Code)
def add_dropdown(request):
    if request.method == "POST":
        form = Clinic_Form(request.POST)  
        if form.is_valid():           
            form.save()  
            messages.success(request, 'Added Successfully')
            return redirect('add_dropdown')  # Redirect after successful POST
            
            
        else:
            messages.error(request, 'Error / Adding Unsuccessful')
            print(form.errors)
    else:
        form = Clinic_Form()  # Show an empty form for GET request

    # Fetch clinic data from the database for dropdown options
    clinics = ClinicData.objects.all()
    
    return render(request, 'home/ClinicForm.html', {'form': form, 'clinics': clinics})

@login_required(login_url="/login/")
def delete_dropdown(request, id):
    clinic_items = get_object_or_404(ClinicData, pk=id)
    clinic_items.delete()
    return redirect('clinic_view')

@login_required(login_url="/login/")
def clinic_view(request):
    clinic_items = ClinicData.objects.all()  # Fetch all clinic data
    return render(request, 'home/ClinicView.html', {'clinic_items': clinic_items})

@login_required(login_url="/login/")
# auto generate clinic_code based on javascript
def get_clinic_code(request):
    ptid_code = request.GET.get('ptid_code')
    clinic_code = ClinicData.objects.filter(PTIDCode=ptid_code).values_list('ClinicCode', flat=True).first()
    clinic_name = ClinicData.objects.filter(PTIDCode=ptid_code).values_list('ClinicName', flat=True).first()
    return JsonResponse({'clinic_code': clinic_code, 'clinic_name': clinic_name})



@login_required(login_url="/login/")
def add_breakpoints(request, pk=None):
    breakpoint = None  # Initialize breakpoint to avoid UnboundLocalError
    upload_form = Breakpoint_uploadForm()

    if pk:  # Editing an existing breakpoint
        breakpoint = get_object_or_404(BreakpointsTable, pk=pk)
        form = BreakpointsForm(request.POST or None, instance=breakpoint)
        editing = True
    else:  # Adding a new breakpoint
        form = BreakpointsForm(request.POST or None)
        editing = False

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Update Successful")
            return redirect('breakpoints_view')  # Redirect to avoid form resubmission

    return render(request, 'home/Breakpoints.html', {
        'form': form,
        'editing': editing,  # Pass editing flag to template
        'breakpoint': breakpoint,  # Pass breakpoint even if None
        'upload_form': upload_form,
    })

@login_required(login_url="/login/")
#View existing breakpoints
def breakpoints_view(request):
    breakpoints = BreakpointsTable.objects.all().order_by('-Date_Modified')
    paginator = Paginator(breakpoints, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/BreakpointsView.html',{ 'breakpoints':breakpoints,  'page_obj': page_obj})

@login_required(login_url="/login/")
#Delete breakpoints
def breakpoints_del(request, id):
    breakpoints = get_object_or_404(BreakpointsTable, pk=id)
    breakpoints.delete()
    return redirect('breakpoints_view')

@login_required(login_url="/login/")
# for uploading and replacing existing breakpoints data
def upload_breakpoints(request):
    if request.method == "POST":
        upload_form = Breakpoint_uploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            # Save the uploaded file instance
            uploaded_file = upload_form.save()
            file = uploaded_file.File_uploadBP  # Get the actual file field
            print("Uploaded file:", file)  # Debugging statement
            try:
                # Load file into a DataFrame using file's temporary path
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)  # For CSV files
                    
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)  # For Excel files

                else:
                    messages.error(request, messages.INFO, 'Unsupported file format. Please upload a CSV or Excel file.')
                    return redirect('upload_breakpoints')

                # Check the DataFrame for debugging
                print(df)
                
                # Check the DataFrame for debugging
                print("DataFrame contents:\n", df.head())  # Print the first few rows

                # Check column and Replace NaN values with empty strings to avoid validation errors
                df.fillna(value={col: "" for col in df.columns}, inplace=True)


                 # Use this to Clear existing records with matching Whonet_Abx values
                whonet_abx_values = df['Whonet_Abx'].unique()
                BreakpointsTable.objects.filter(Whonet_Abx__in=whonet_abx_values).delete()


                # Insert rows into BreakpointsTable
                for _, row in df.iterrows():
                    # Parse Date_Modified if it's present and valid
                    date_modified = None
                    if row.get('Date_Modified'):
                        date_modified = pd.to_datetime(row['Date_Modified'], errors='coerce')
                        if pd.isna(date_modified):
                            date_modified = None

                    # Create a new instance of BreakpointsTable
                    BreakpointsTable.objects.create(
                        Show=bool(row.get('Show', False)),
                        Retest=bool(row.get('Retest', False)),
                        Disk_Abx=bool(row.get('Disk_Abx', False)),
                        Guidelines=row.get('Guidelines', ''),
                        Tier=row.get('Tier', ''),
                        Test_Method=row.get('Test_Method', ''),
                        Potency=row.get('Potency', ''),
                        Abx_code=row.get('Abx_code', ''),
                        Antibiotic=row.get('Antibiotic', ''),
                        Alert_val=row.get('Alert_val',''),
                        Alert_cln=row.get('Alert_cln',''),
                        Whonet_Abx=row.get('Whonet_Abx', ''),
                        R_val=row.get('R_val', ''),
                        I_val=row.get('I_val', ''),
                        SDD_val=row.get('SDD_val', ''),
                        S_val=row.get('S_val', ''),
                        Date_Modified=date_modified,
                    )
                
                messages.success(request, messages.INFO, 'File uploaded and data added successfully to the database!')
                return redirect('breakpoints_view')

            except Exception as e:
                print("Error during processing:", e)  # Debug statement
                messages.error(request, f"Error processing file: {e}")
                return redirect('add_breakpoints')
        else:
            messages.error(request, messages.INFO, "Form is not valid.")

    else:
        upload_form = Breakpoint_uploadForm()

    return render(request, 'home/Breakpoints.html', {'upload_form': upload_form})

@login_required(login_url="/login/")
#for exporting into excel
def export_breakpoints(request):
    objects = BreakpointsTable.objects.all()
    data = []

    for obj in objects:
        data.append({
            "Show": obj.Show,
            "Retest": obj.Retest,
            "Disk_Abx": obj.Disk_Abx,
            "Guidelines": obj.Guidelines,
            "Tier": obj.Tier,
            "Test_Method": obj.Test_Method,
            "Potency": obj.Potency,
            "Abx_code": obj.Abx_code,
            "Antibiotic": obj.Antibiotic,
            "Alert_val": obj.Alert_val,
            "Alert_cln": obj.Alert_cln,
            "Whonet_Abx": obj.Whonet_Abx,
            "R_val": obj.R_val,
            "I_val": obj.I_val,
            "SDD_val": obj.SDD_val,
            "S_val": obj.S_val,
            "Date_Modified": obj.Date_Modified,
        })
    
    # Define file path
    file_path = "Breakpoints_egasp.xlsx"

    # Convert data to DataFrame and save as Excel
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

    # Return the file as a response
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename="Breakpoints_egasp.xlsx")



@login_required(login_url="/login/")
def delete_all_breakpoints(request):
    BreakpointsTable.objects.all().delete()
    messages.success(request, "All records have been deleted successfully.")
    return redirect('breakpoints_view')  # Redirect to the table view


@login_required(login_url="/login/")
def abxentry_view(request):
    entries = AntibioticEntry.objects.filter(ab_Retest_Abx_code__isnull=True)
    abx_data = {}
    abx_codes = set()

    for entry in entries:
        egasp_id = entry.ab_EgaspId
        abx_code = entry.ab_Abx_code  # Only ordinary antibiotic (excluding retest antibiotics)

        # Get all values and interpretations for ordinary antibiotics
        value = entry.ab_Disk_value or entry.ab_MIC_value
        RIS = entry.ab_Disk_RIS or entry.ab_MIC_RIS
        Operand = entry.ab_MIC_operand or None

        if egasp_id not in abx_data:
            abx_data[egasp_id] = {}

        # Store only **ordinary** antibiotic values
        if abx_code:  
            abx_data[egasp_id][abx_code] = {'value': value, 'RIS': RIS, 'Operand': Operand}
            abx_codes.add(abx_code)  # Add only ordinary antibiotics


    context = {
        'abx_data': abx_data,
        'abx_codes': sorted(abx_codes),  # Sorted list of ordinary antibiotics
    }
    
    return render(request, 'home/AntibioticentryView.html', context)


@login_required(login_url="/login/")
# View to display all specimen types
def specimen_list(request):
    specimen_items = SpecimenTypeModel.objects.all()
    return render(request, 'home/SpecimenView.html', {'specimen_items': specimen_items})

@login_required(login_url="/login/")
# View to add or edit a specimen type
def add_specimen(request):
    if request.method == 'POST':
        form = SpecimenTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_specimen')  # Redirect after saving
    else:
        form = SpecimenTypeForm()  # Empty form for new specimen
    
    return render(request, 'home/Specimentype.html', {'form': form})

@login_required(login_url="/login/")
# Edit an existing specimen
def edit_specimen(request, pk):
    specimen = get_object_or_404(SpecimenTypeModel, pk=pk)

    if request.method == 'POST':
        form = SpecimenTypeForm(request.POST, instance=specimen)  # Pre-fill with existing data
        if form.is_valid():
            form.save()
            return redirect('specimen_list')  # Redirect after saving
    else:
        form = SpecimenTypeForm(instance=specimen)  # Load existing data
    
    return render(request, 'home/SpecimenEdit.html', {'form': form, 'specimen': specimen})


@login_required(login_url="/login/")
# View to delete a specimen type
def delete_specimen(request, pk):
    specimen = get_object_or_404(SpecimenTypeModel, pk=pk)
    specimen.delete()
    return redirect('specimen_list')



@login_required(login_url="/login/")
def export_Antibioticentry(request):
    objects = AntibioticEntry.objects.all()
    data = []

    for obj in objects:
        data.append({
            "ab_idNumber_egasp": obj.ab_idNumber_egasp.Egasp_Id if obj.ab_idNumber_egasp else None,
            "EgaspId": obj.ab_EgaspId,
            "Antibiotic": obj.ab_Antibiotic,
            "Abx_code": obj.ab_Abx_code,
            "Abx": obj.ab_Abx,
            "Disk_value": obj.ab_Disk_value,
            "Disk_RIS": obj.ab_Disk_RIS,
            "MIC_operand": obj.ab_MIC_operand,
            "MIC_value": obj.ab_MIC_value,
            "MIC_RIS": obj.ab_MIC_RIS,
            "Retest_Antibiotic": obj.ab_Retest_Antibiotic,
            "Retest_Abx_code": obj.ab_Retest_Abx_code,
            "Retest_Abx": obj.ab_Retest_Abx,
            "Retest_DiskValue": obj.ab_Retest_DiskValue,
            "Retest_Disk_RIS": obj.ab_Retest_Disk_RIS,
            "Ret_MIC_Operand": obj.ab_Retest_MIC_operand,
            "Retest_MICValue": obj.ab_Retest_MICValue,
            "Retest_MIC_RIS": obj.ab_Retest_MIC_RIS,
        })
    
    # Define file path
    file_path = "AntibioticEntry_egasp.xlsx"

    # Convert data to DataFrame and save as Excel
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

    # Return the file as a response
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename="AntibioticEntry_egasp.xlsx")


@login_required(login_url="/login/")
#Address Book
#Contact Form not working
def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)  
        if form.is_valid():           
            form.save()  
            messages.success(request, 'Added Successfully')
            return redirect('add_contact')  # Redirect after successful POST
            
            
        else:
            messages.error(request, 'Error / Adding Unsuccessful')
            print(form.errors)
    else:
        form = ContactForm()  # Show an empty form for GET request

    # Fetch clinic data from the database for dropdown options
    contacts = Clinic_Staff_Details.objects.all()
    
    return render(request, 'home/Contact_Form.html', {'form': form, 'contacts': contacts})


@login_required(login_url="/login/")
def delete_contact(request, id):
    contact_items = get_object_or_404(Clinic_Staff_Details, pk=id)
    contact_items.delete()
    return redirect('contact_view')


# for LAB PERSONNEL
def edit_contact(request, pk):
    contact = get_object_or_404(Clinic_Staff_Details, pk=pk)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)  # Pre-fill with existing data
        if form.is_valid():
            form.save()
            return redirect('contact_view')  # Redirect after saving
    else:
        form = ContactForm(instance=contact)  # Load existing data
    
    return render(request, 'home/Contact_Edit.html', {'form': form, 'contact': contact})


@login_required(login_url="/login/")
def contact_view(request):
    contact_items = Clinic_Staff_Details.objects.all()  # Fetch all contact data
    return render(request, 'home/Contact_View.html', {'contact_items': contact_items})


## FOR CLINIC PERSONNEL

def add_clin_pers(request):
    if request.method == "POST":
        form = Clinic_Pers_Form(request.POST)  
        if form.is_valid():           
            form.save()  
            messages.success(request, 'Added Successfully')
            return redirect('view_clin_pers')  # Redirect after successful POST
            
            
        else:
            messages.error(request, 'Error / Adding Unsuccessful')
            print(form.errors)
    else:
        form = Clinic_Pers_Form()  # Show an empty form for GET request

    # Fetch clinic data from the database for dropdown options
    contacts = Clinic_Pers_Other.objects.all()
    
    return render(request, 'home/Clinic_Staff.html', {'form': form, 'contacts': contacts})


@login_required(login_url="/login/")
def view_clin_pers(request):
    clin_staff_items = Clinic_Pers_Other.objects.all()  # Fetch all contact data
    return render(request, 'home/Clinic_Staff_View.html', {'clin_staff_items': clin_staff_items})


@login_required(login_url="/login/")
def edit_clin_pers(request, pk):
    clinstaff = get_object_or_404(Clinic_Pers_Other, pk=pk)

    if request.method == 'POST':
        form = Clinic_Pers_Form(request.POST, instance=clinstaff)  # Pre-fill with existing data
        if form.is_valid():
            form.save()
            return redirect('view_clin_pers')  # Redirect after saving
    else:
        form = Clinic_Pers_Form(instance=clinstaff)  # Load existing data
    
    return render(request, 'home/Clinic_Staff_Edit.html', {'form': form, 'clinstaff': clinstaff})


@login_required(login_url="/login/")
def delete_clin_pers(request, pk):
    clin_staff_items = get_object_or_404(Clinic_Pers_Other, pk=pk)
    clin_staff_items.delete()
    return redirect('view_clin_pers')


@login_required(login_url="/login/")
def get_clinic_pers_details(request):
    clin_staff_name = request.GET.get('clin_staff_id')  #  contains a name, not an ID
    clin_staff = Clinic_Pers_Other.objects.filter(Pers_Name=clin_staff_name).first()

    if clin_staff:
        return JsonResponse({
            # 'ClinStaff_Telnum': str(lab_staff.ClinStaff_Telnum),  # Convert PhoneNumber to string
            'Pers_Contact': clin_staff.Pers_Contact,  
            'Pers_Email': clin_staff.Pers_Email,
        
        })
    else:
        return JsonResponse({'error': 'Staff not found'}, status=404)








@login_required(login_url="/login/")
def get_clinic_staff_details(request):
    lab_staff_name = request.GET.get('lab_staff_id')  # Actually contains a name, not an ID
    lab_staff = Clinic_Staff_Details.objects.filter(ClinStaff_Name=lab_staff_name).first()

    if lab_staff:
        return JsonResponse({
            # 'ClinStaff_Telnum': str(lab_staff.ClinStaff_Telnum),  # Convert PhoneNumber to string
            'ClinStaff_Contact': lab_staff.ClinStaff_Contact,  # Convert PhoneNumber to string
            'ClinStaff_Email': lab_staff.ClinStaff_Email,
            'ClinStaff_License': lab_staff.ClinStaff_License,
            'ClinStaff_Designation': lab_staff.ClinStaff_Designation
        })
    else:
        return JsonResponse({'error': 'Staff not found'}, status=404)



@login_required(login_url="/login/")
#for province and city fields
def upload_locations(request):
    if request.method == "POST":
        upload_form = LocationUploadForm(request.POST, request.FILES)
        
        if upload_form.is_valid():
            uploaded_file = upload_form.save()
            file = uploaded_file.file  # Get the uploaded file
            
            print("Uploaded file:", file)  # Debugging statement

            try:
                # Load file into a DataFrame based on file type
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    messages.error(request, 'Unsupported file format. Please upload a CSV or Excel file.')
                    return redirect('upload_locations')

                print("DataFrame contents:\n", df.head())  # Debugging statement

                # Fill NaN values to avoid errors
                df.fillna("", inplace=True)

                # Loop through rows and save Provinces and Cities
                for _, row in df.iterrows():
                    provincename = row.get('Province', '').strip()
                    cityname = row.get('City', '').strip()

                    if not provincename or not cityname:
                        continue  # Skip empty rows

                    # Get or create province
                    province, _ = Province.objects.get_or_create(provincename=provincename)

                    # Get or create city linked to the province
                    City.objects.get_or_create(cityname=cityname, province=province)

                messages.success(request, "File uploaded successfully and data added!")
                return redirect('add_location')

            except Exception as e:
                print("Error:", e)
                messages.error(request, f"Error processing file: {e}")
                return redirect('upload_locations')
        else:
            messages.error(request, "Invalid form submission.")

    else:
        upload_form = LocationUploadForm()

    return render(request, 'home/Add_location.html', {'upload_form': upload_form})


@login_required(login_url="/login/")
def add_location(request, id=None):
    provinces = Province.objects.all()  # Renamed 'province' to 'provinces' for clarity
    upload_form = LocationUploadForm()  
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Location added successfully!")
            return redirect("add_location")  # Use the correct URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CityForm()

    return render(request, "home/Add_location.html", {"form": form, "provinces": provinces, "upload_form": upload_form})

@login_required(login_url="/login/")
#used for grouping cities
def get_cities_by_province(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).values('id', 'cityname')
    return JsonResponse({'cities': list(cities)})


# def get_cities_by_province(request):
#     province_name = request.GET.get('province_id')  # actually province_name
#     if not province_name:
#         return JsonResponse({'cities': []})

#     cities = City.objects.filter(province__provincename=province_name).values('id', 'cityname')
#     return JsonResponse(list(cities), safe=False)


@login_required(login_url="/login/")
def view_locations(request):
    # Fetch all provinces, sorted by province name
    provinces = Province.objects.prefetch_related(
        Prefetch('cities', queryset=City.objects.order_by('cityname'))  # Sort cities by city name
    ).order_by('provincename')  # Sort provinces by province name

    return render(request, 'home/view_locations.html', {'provinces': provinces})


@login_required(login_url="/login/")
def delete_cities(request):
    City.objects.all().delete()
    Province.objects.all().delete()
    messages.success(request, "All records have been deleted successfully.")
    return redirect('view_locations')  # Redirect to the table view

@login_required(login_url="/login/")
def delete_city(request, id):
    city_items = get_object_or_404(City, pk=id)
    city_items.delete()
    return redirect('view_locations')



#download combined table
def is_blank(value):
    return value in [None, '', 0]


def download_combined_table(request):
    egasp_data_entries = Egasp_Data.objects.all()

    # Collect unique antibiotics from both abx and retest
    unique_abx_codes = set()
    for abx_code, rt_code in AntibioticEntry.objects.values_list('ab_Abx_code', 'ab_Retest_Abx_code').distinct():
        if abx_code:
            unique_abx_codes.add(abx_code)
        if rt_code:
            unique_abx_codes.add(rt_code)

    sorted_antibiotics = sorted(unique_abx_codes)

    # Pre-check which antibiotics are disk types
    disk_abx_lookup = {
        abx: BreakpointsTable.objects.filter(Whonet_Abx=abx, Disk_Abx=True).exists()
        for abx in sorted_antibiotics
    }

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="combined_table.csv"'
    response.write('\ufeff')  # UTF-8 BOM
    writer = csv.writer(response)

    # Static fields (as you defined)
    static_fields = [
        'Date_of_Entry', 'ID_Number', 'Egasp_Id', 'PTIDCode', 'Laboratory', 'Clinic', 'Consult_Date',
        'Consult_Type', 'Client_Type', 'Uic_Ptid', 'Clinic_Code', 'ClinicCodeGen', 'First_Name', 'Middle_Name',
        'Last_Name', 'Suffix', 'Birthdate', 'Age', 'Sex', 'Gender_Identity', 'Gender_Identity_Other',
        'Occupation', 'Civil_Status', 'Civil_Status_Other', 'Current_Province', 'Current_City', 'Current_Country',
        'PermAdd_same_CurrAdd', 'Permanent_Province', 'Permanent_City', 'Permanent_Country', 'Other_Country',
        'Nationality', 'Nationality_Other', 'Travel_History', 'Travel_History_Specify', 'Client_Group',
        'Client_Group_Other', 'History_Of_Sex_Partner', 'Nationality_Sex_Partner', 'Date_of_Last_Sex',
        'Nationality_Sex_Partner_Other', 'Number_Of_Sex_Partners', 'Relationship_to_Partners', 'SB_Urethral',
        'SB_Vaginal', 'SB_Anal_Insertive', 'SB_Oral_Insertive', 'Sharing_of_Sex_Toys', 'SB_Oral_Receptive',
        'SB_Anal_Receptive', 'SB_Others', 'Sti_None', 'Sti_Hiv', 'Sti_Hepatitis_B', 'Sti_Hepatitis_C',
        'Sti_NGI', 'Sti_Syphilis', 'Sti_Chlamydia', 'Sti_Anogenital_Warts', 'Sti_Genital_Ulcer', 'Sti_Herpes',
        'Sti_Other', 'Sti_Trichomoniasis', 'Sti_Mycoplasma_genitalium', 'Sti_Lymphogranuloma', 'Illicit_Drug_Use',
        'Illicit_Drug_Specify', 'Abx_Use_Prescribed', 'Abx_Use_Prescribed_Specify', 'Abx_Use_Self_Medicated',
        'Abx_Use_Self_Medicated_Specify', 'Abx_Use_None', 'Abx_Use_Other', 'Abx_Use_Other_Specify',
        'Route_Oral', 'Route_Injectable_IV', 'Route_Dermal', 'Route_Suppository', 'Route_Other',
        'Symp_With_Discharge', 'Symp_No', 'Symp_Discharge_Urethra', 'Symp_Discharge_Vagina',
        'Symp_Discharge_Anus', 'Symp_Discharge_Oropharyngeal', 'Symp_Pain_Lower_Abdomen', 'Symp_Tender_Testicles',
        'Symp_Painful_Urination', 'Symp_Painful_Intercourse', 'Symp_Rectal_Pain', 'Symp_Other',
        'Outcome_Of_Follow_Up_Visit', 'Prev_Test_Pos', 'Prev_Test_Pos_Date', 'Result_Test_Cure_Initial',
        'Result_Test_Cure_Followup', 'NoTOC_Other_Test', 'NoTOC_DatePerformed', 'NoTOC_Result_of_Test',
        'Patient_Compliance_Antibiotics', 'OtherDrugs_Specify', 'OtherDrugs_Dosage', 'OtherDrugs_Route',
        'OtherDrugs_Duration', 'Gonorrhea_Treatment', 'Treatment_Outcome', 'Primary_Antibiotic',
        'Primary_Abx_Other', 'Secondary_Antibiotic', 'Secondary_Abx_Other', 'Notes', 'Clinic_Staff',
        'Requesting_Physician', 'Telephone_Number', 'Email_Address', 'Date_Accomplished_Clinic',
        'Date_Requested_Clinic', 'Date_Specimen_Collection', 'Specimen_Code', 'Specimen_Type',
        'Specimen_Quality', 'Date_Of_Gram_Stain', 'Diagnosis_At_This_Visit', 'Gram_Neg_Intracellular',
        'Gram_Neg_Extracellular', 'Gs_Presence_Of_Pus_Cells', 'Presence_GN_Intracellular',
        'Presence_GN_Extracellular', 'GS_Pus_Cells', 'Epithelial_Cells', 'GS_Date_Released', 'GS_Others',
        'GS_Negative', 'Gs_Gram_neg_diplococcus', 'Gs_NoGram_neg_diplococcus', 'Gs_Not_performed',
        'Date_Received_in_lab', 'Positive_Culture_Date', 'Culture_Result', 'Growth', 'Growth_span',
        'Species_Identification', 'Other_species_ID', 'Specimen_Quality_Cs', 'Susceptibility_Testing_Date',
        'Retested_Mic', 'Confirmation_Ast_Date', 'NAAT_ng', 'NAAT_chl', 'Beta_Lactamase', 'PPng', 'TRng',
        'Date_Released', 'For_possible_WGS', 'Date_stocked', 'Location', 'abx_code', 'Laboratory_Staff',
        'Date_Accomplished_ARSP', 'ars_notes', 'ars_license', 'ars_designation', 'Validator_Pers',
        'Date_Validated_ARSP', 'val_license', 'val_designation'
    ]

    header = static_fields[:]
    for abx in sorted_antibiotics:
        header.append(f'{abx}_Val')
        header.append(f'{abx}_RIS')
        header.append(f'{abx}_RT_Val')
        header.append(f'{abx}_RT_RIS')

    writer.writerow(header)

    for egasp in egasp_data_entries:
        row = [getattr(egasp, field, '') for field in static_fields]
        abx_entries = AntibioticEntry.objects.filter(ab_idNumber_egasp=egasp)
        abx_data = {}

        for ab in abx_entries:
            # Initial result
            if ab.ab_Abx_code:
                code = ab.ab_Abx_code
                if code not in abx_data:
                    abx_data[code] = {}
                if not is_blank(ab.ab_MIC_value) or not is_blank(ab.ab_Disk_value):
                    val = ab.ab_Disk_value if not is_blank(ab.ab_Disk_value) else f"{ab.ab_MIC_operand or ''}{ab.ab_MIC_value}"
                    ris = ab.ab_Disk_RIS or ab.ab_MIC_RIS
                    abx_data[code].update({
                        '_Val': val,
                        '_RIS': ris,
                    })

            # Retest result
            if ab.ab_Retest_Abx_code:
                code = ab.ab_Retest_Abx_code
                if code not in abx_data:
                    abx_data[code] = {}
                if not is_blank(ab.ab_Retest_MICValue) or not is_blank(ab.ab_Retest_DiskValue):
                    rt_val = ab.ab_Retest_DiskValue if not is_blank(ab.ab_Retest_DiskValue) else f"{ab.ab_Retest_MIC_operand or ''}{ab.ab_Retest_MICValue}"
                    rt_ris = ab.ab_Retest_Disk_RIS or ab.ab_Retest_MIC_RIS
                    abx_data[code].update({
                        'RT_Val': rt_val,
                        'RT_RIS': rt_ris,
                    })

        # Populate row with antibiotic data
        for abx in sorted_antibiotics:
            data = abx_data.get(abx, {})
            val = data.get('_Val', '')
            if isinstance(val, (int, float)):
                val = format(val, '.3f')
            rt_val = data.get('RT_Val', '')
            if isinstance(rt_val, (int, float)):
                rt_val = format(rt_val, '.3f')
            row.extend([val, data.get('_RIS', ''), rt_val, data.get('RT_RIS', '')])

        writer.writerow(row)

    return response



# @login_required(login_url="/login/")
# #download combined table
# def download_combined_table(request):
#     egasp_data_entries = Egasp_Data.objects.all()

#     # Collect unique antibiotics from both abx and retest
#     unique_abx_codes = set()
#     for abx_code, rt_code in AntibioticEntry.objects.values_list('ab_Abx_code', 'ab_Retest_Abx_code').distinct():
#         if abx_code:
#             unique_abx_codes.add(abx_code)
#         if rt_code:
#             unique_abx_codes.add(rt_code)

#     sorted_antibiotics = sorted(unique_abx_codes)

#     # Pre-check which antibiotics are disk types
#     disk_abx_lookup = {
#         abx: BreakpointsTable.objects.filter(Whonet_Abx=abx, Disk_Abx=True).exists()
#         for abx in sorted_antibiotics
#     }

#     response = HttpResponse(content_type='text/csv; charset=utf-8')
#     response['Content-Disposition'] = 'attachment; filename="combined_table.csv"'
#     response.write('\ufeff')
#     writer = csv.writer(response)

#     # Static column headers
#     static_fields = [
#     'Date_of_Entry', 'ID_Number', 'Egasp_Id', 'PTIDCode', 'Laboratory', 'Clinic', 'Consult_Date',
#     'Consult_Type', 'Client_Type', 'Uic_Ptid', 'Clinic_Code', 'ClinicCodeGen', 'First_Name', 'Middle_Name',
#     'Last_Name', 'Suffix', 'Birthdate', 'Age', 'Sex', 'Gender_Identity', 'Gender_Identity_Other',
#     'Occupation', 'Civil_Status', 'Civil_Status_Other', 'Current_Province', 'Current_City', 'Current_Country',
#     'PermAdd_same_CurrAdd', 'Permanent_Province', 'Permanent_City', 'Permanent_Country', 'Other_Country',
#     'Nationality', 'Nationality_Other', 'Travel_History', 'Travel_History_Specify', 'Client_Group',
#     'Client_Group_Other', 'History_Of_Sex_Partner', 'Nationality_Sex_Partner', 'Date_of_Last_Sex',
#     'Nationality_Sex_Partner_Other', 'Number_Of_Sex_Partners', 'Relationship_to_Partners', 'SB_Urethral',
#     'SB_Vaginal', 'SB_Anal_Insertive', 'SB_Oral_Insertive', 'Sharing_of_Sex_Toys', 'SB_Oral_Receptive',
#     'SB_Anal_Receptive', 'SB_Others', 'Sti_None', 'Sti_Hiv', 'Sti_Hepatitis_B', 'Sti_Hepatitis_C',
#     'Sti_NGI', 'Sti_Syphilis', 'Sti_Chlamydia', 'Sti_Anogenital_Warts', 'Sti_Genital_Ulcer', 'Sti_Herpes',
#     'Sti_Other', 'Sti_Trichomoniasis', 'Sti_Mycoplasma_genitalium', 'Sti_Lymphogranuloma', 'Illicit_Drug_Use',
#     'Illicit_Drug_Specify', 'Abx_Use_Prescribed', 'Abx_Use_Prescribed_Specify', 'Abx_Use_Self_Medicated',
#     'Abx_Use_Self_Medicated_Specify', 'Abx_Use_None', 'Abx_Use_Other', 'Abx_Use_Other_Specify',
#     'Route_Oral', 'Route_Injectable_IV', 'Route_Dermal', 'Route_Suppository', 'Route_Other',
#     'Symp_With_Discharge', 'Symp_No', 'Symp_Discharge_Urethra', 'Symp_Discharge_Vagina',
#     'Symp_Discharge_Anus', 'Symp_Discharge_Oropharyngeal', 'Symp_Pain_Lower_Abdomen', 'Symp_Tender_Testicles',
#     'Symp_Painful_Urination', 'Symp_Painful_Intercourse', 'Symp_Rectal_Pain', 'Symp_Other',
#     'Outcome_Of_Follow_Up_Visit', 'Prev_Test_Pos', 'Prev_Test_Pos_Date', 'Result_Test_Cure_Initial',
#     'Result_Test_Cure_Followup', 'NoTOC_Other_Test', 'NoTOC_DatePerformed', 'NoTOC_Result_of_Test',
#     'Patient_Compliance_Antibiotics', 'OtherDrugs_Specify', 'OtherDrugs_Dosage', 'OtherDrugs_Route',
#     'OtherDrugs_Duration', 'Gonorrhea_Treatment', 'Treatment_Outcome', 'Primary_Antibiotic',
#     'Primary_Abx_Other', 'Secondary_Antibiotic', 'Secondary_Abx_Other', 'Notes', 'Clinic_Staff',
#     'Requesting_Physician', 'Telephone_Number', 'Email_Address', 'Date_Accomplished_Clinic',
#     'Date_Requested_Clinic', 'Date_Specimen_Collection', 'Specimen_Code', 'Specimen_Type',
#     'Specimen_Quality', 'Date_Of_Gram_Stain', 'Diagnosis_At_This_Visit', 'Gram_Neg_Intracellular',
#     'Gram_Neg_Extracellular', 'Gs_Presence_Of_Pus_Cells', 'Presence_GN_Intracellular',
#     'Presence_GN_Extracellular', 'GS_Pus_Cells', 'Epithelial_Cells', 'GS_Date_Released', 'GS_Others',
#     'GS_Negative', 'Gs_Gram_neg_diplococcus', 'Gs_NoGram_neg_diplococcus', 'Gs_Not_performed',
#     'Date_Received_in_lab', 'Positive_Culture_Date', 'Culture_Result', 'Growth', 'Growth_span',
#     'Species_Identification', 'Other_species_ID', 'Specimen_Quality_Cs', 'Susceptibility_Testing_Date',
#     'Retested_Mic', 'Confirmation_Ast_Date', 'NAAT_ng', 'NAAT_chl', 'Beta_Lactamase', 'PPng', 'TRng',
#     'Date_Released', 'For_possible_WGS', 'Date_stocked', 'Location', 'abx_code', 'Laboratory_Staff',
#     'Date_Accomplished_ARSP', 'ars_notes', 'ars_license', 'ars_designation', 'Validator_Pers',
#     'Date_Validated_ARSP', 'val_license', 'val_designation'
# ]

#     header = [
#         'Date_of_Entry', 'ID_Number', 'Egasp_Id', 'PTIDCode', 'Laboratory', 'Clinic', 'Consult_Date',
#         'Consult_Type', 'Client_Type', 'Uic_Ptid', 'Clinic_Code', 'ClinicCodeGen', 'First_Name', 'Middle_Name',
#         'Last_Name', 'Suffix', 'Birthdate', 'Age', 'Sex', 'Gender_Identity', 'Gender_Identity_Other',
#         'Occupation', 'Civil_Status', 'Civil_Status_Other', 'Current_Province', 'Current_City', 'Current_Country',
#         'PermAdd_same_CurrAdd', 'Permanent_Province', 'Permanent_City', 'Permanent_Country', 'Other_Country',
#         'Nationality', 'Nationality_Other', 'Travel_History', 'Travel_History_Specify', 'Client_Group',
#         'Client_Group_Other', 'History_Of_Sex_Partner', 'Nationality_Sex_Partner', 'Date_of_Last_Sex',
#         'Nationality_Sex_Partner_Other', 'Number_Of_Sex_Partners', 'Relationship_to_Partners', 'SB_Urethral',
#         'SB_Vaginal', 'SB_Anal_Insertive', 'SB_Oral_Insertive', 'Sharing_of_Sex_Toys', 'SB_Oral_Receptive',
#         'SB_Anal_Receptive', 'SB_Others', 'Sti_None', 'Sti_Hiv', 'Sti_Hepatitis_B', 'Sti_Hepatitis_C',
#         'Sti_NGI', 'Sti_Syphilis', 'Sti_Chlamydia', 'Sti_Anogenital_Warts', 'Sti_Genital_Ulcer', 'Sti_Herpes',
#         'Sti_Other', 'Sti_Trichomoniasis', 'Sti_Mycoplasma_genitalium', 'Sti_Lymphogranuloma', 'Illicit_Drug_Use',
#         'Illicit_Drug_Specify', 'Abx_Use_Prescribed', 'Abx_Use_Prescribed_Specify', 'Abx_Use_Self_Medicated',
#         'Abx_Use_Self_Medicated_Specify', 'Abx_Use_None', 'Abx_Use_Other', 'Abx_Use_Other_Specify',
#         'Route_Oral', 'Route_Injectable_IV', 'Route_Dermal', 'Route_Suppository', 'Route_Other',
#         'Symp_With_Discharge', 'Symp_No', 'Symp_Discharge_Urethra', 'Symp_Discharge_Vagina',
#         'Symp_Discharge_Anus', 'Symp_Discharge_Oropharyngeal', 'Symp_Pain_Lower_Abdomen', 'Symp_Tender_Testicles',
#         'Symp_Painful_Urination', 'Symp_Painful_Intercourse', 'Symp_Rectal_Pain', 'Symp_Other',
#         'Outcome_Of_Follow_Up_Visit', 'Prev_Test_Pos', 'Prev_Test_Pos_Date', 'Result_Test_Cure_Initial',
#         'Result_Test_Cure_Followup', 'NoTOC_Other_Test', 'NoTOC_DatePerformed', 'NoTOC_Result_of_Test',
#         'Patient_Compliance_Antibiotics', 'OtherDrugs_Specify', 'OtherDrugs_Dosage', 'OtherDrugs_Route',
#         'OtherDrugs_Duration', 'Gonorrhea_Treatment', 'Treatment_Outcome', 'Primary_Antibiotic',
#         'Primary_Abx_Other', 'Secondary_Antibiotic', 'Secondary_Abx_Other', 'Notes', 'Clinic_Staff',
#         'Requesting_Physician', 'Telephone_Number', 'Email_Address', 'Date_Accomplished_Clinic',
#         'Date_Requested_Clinic', 'Date_Specimen_Collection', 'Specimen_Code', 'Specimen_Type',
#         'Specimen_Quality', 'Date_Of_Gram_Stain', 'Diagnosis_At_This_Visit', 'Gram_Neg_Intracellular',
#         'Gram_Neg_Extracellular', 'Gs_Presence_Of_Pus_Cells', 'Presence_GN_Intracellular',
#         'Presence_GN_Extracellular', 'GS_Pus_Cells', 'Epithelial_Cells', 'GS_Date_Released', 'GS_Others',
#         'GS_Negative', 'Gs_Gram_neg_diplococcus', 'Gs_NoGram_neg_diplococcus', 'Gs_Not_performed',
#         'Date_Received_in_lab', 'Positive_Culture_Date', 'Culture_Result', 'Growth', 'Growth_span',
#         'Species_Identification', 'Other_species_ID', 'Specimen_Quality_Cs', 'Susceptibility_Testing_Date',
#         'Retested_Mic', 'Confirmation_Ast_Date', 'NAAT_ng', 'NAAT_chl', 'Beta_Lactamase', 'PPng', 'TRng',
#         'Date_Released', 'For_possible_WGS', 'Date_stocked', 'Location', 'abx_code', 'Laboratory_Staff',
#         'Date_Accomplished_ARSP', 'ars_notes', 'ars_license', 'ars_designation', 'Validator_Pers',
#         'Date_Validated_ARSP', 'val_license', 'val_designation'
#     ]

#     for abx in sorted_antibiotics:
#         if not disk_abx_lookup[abx]:
#             header.append(f'{abx}_Op')
#         header.append(f'{abx}_Val')
#         header.append(f'{abx}_RIS')
#         if not disk_abx_lookup[abx]:
#             header.append(f'{abx}_RT_Op')
#         header.append(f'{abx}_RT_Val')
#         header.append(f'{abx}_RT_RIS')

#     writer.writerow(header)

#     for egasp in egasp_data_entries:
#         row = [getattr(egasp, field, '') for field in static_fields]


#         # Collect antibiotic results
#         abx_entries = AntibioticEntry.objects.filter(ab_idNumber_egasp=egasp)
#         abx_data = {}

#         for ab in abx_entries:
#             # Initial
#             if ab.ab_Abx_code:
#                 code = ab.ab_Abx_code
#                 if code not in abx_data:
#                     abx_data[code] = {}
#                 abx_data[code].update({
#                     '_Val': ab.ab_Disk_value or ab.ab_MIC_value,
#                     '_RIS': ab.ab_Disk_RIS or ab.ab_MIC_RIS,
#                     '_Op': ab.ab_MIC_operand or '',
#                 })

#             # Retest
#             if ab.ab_Retest_Abx_code:
#                 code = ab.ab_Retest_Abx_code
#                 if code not in abx_data:
#                     abx_data[code] = {}
#                 abx_data[code].update({
#                     'RT_Val': ab.ab_Retest_DiskValue or ab.ab_Retest_MICValue,
#                     'RT_RIS': ab.ab_Retest_Disk_RIS or ab.ab_Retest_MIC_RIS,
#                     'RT_Op': ab.ab_Retest_MIC_operand or '',
#                 })

#         # Add antibiotic data to row
#         for abx in sorted_antibiotics:
#             is_disk = disk_abx_lookup[abx]
#             data = abx_data.get(abx, {})
#             if not is_disk:
#                 row.append(data.get('_Op', ''))
#             val = data.get('_Val', '')
#             if isinstance(val, (int, float)):
#                 val = format(val, '.3f')
#             row.append(val)
#             row.append(data.get('_RIS', ''))
#             if not is_disk:
#                 row.append(data.get('RT_Op', ''))
#             rt_val = data.get('RT_Val', '')
#             if isinstance(rt_val, (int, float)):
#                 rt_val = format(rt_val, '.3f')
#             row.append(rt_val)
#             row.append(data.get('RT_RIS', ''))

#         writer.writerow(row)

#     return response



#for uploading data in tables egasp and antibiotics entries
# def upload_combined_table(request):
#     if request.method == 'POST':
#         upload_form = UploadDataForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = request.FILES['data_upload']
#             csv_file = TextIOWrapper(uploaded_file.file, encoding='utf-8')
#             reader = csv.DictReader(csv_file)


#             for row in reader:
#                 egasp_id = row.get('Egasp_Id')
#                 if not egasp_id:
#                     continue  # Skip row without Egasp_Id
                
#                 # Create or update the Egasp_Data record
#                 egasp_obj, created = Egasp_Data.objects.get_or_create(
#                     Egasp_Id=egasp_id,
#                     defaults={
#                         'Date_of_Entry': row.get('Date_of_Entry', ' '),
#                         'ID_Number': row.get('ID_Number', ' '),
#                         'Egasp_Id': row.get('Egasp_Id', ' '),
#                         'PTIDCode': row.get('PTIDCode', ' '),
#                         'Laboratory': row.get('Laboratory', ' '),
#                         'Clinic': row.get('Clinic', ' '),
#                         'Consult_Date': row.get('Consult_Date', ' '),
#                         'Consult_Type': row.get('Consult_Type', ' '),
#                         'Client_Type': row.get('Client_Type', ' '),
#                         'Uic_Ptid': row.get('Uic_Ptid', ' '),
#                         'Clinic_Code': row.get('Clinic_Code', ' '),
#                         'ClinicCodeGen': row.get('ClinicCodeGen', ' '),
#                         'First_Name': row.get('First_Name', ' '),
#                         'Middle_Name': row.get('Middle_Name', ' '),
#                         'Last_Name': row.get('Last_Name', ' '),
#                         'Suffix': row.get('Suffix', ' '),
#                         'Birthdate': row.get('Birthdate', ' '),
#                         'Age': row.get('Age', ' '),
#                         'Sex': row.get('Sex', ' '),
#                         'Gender_Identity': row.get('Gender_Identity', ' '),
#                         'Gender_Identity_Other': row.get('Gender_Identity_Other', ' '),
#                         'Occupation': row.get('Occupation', ' '),
#                         'Civil_Status': row.get('Civil_Status', ' '),
#                         'Civil_Status_Other': row.get('Civil_Status_Other', ' '),
#                         'Current_Province': row.get('Current_Province', ' '),
#                         'Current_City': row.get('Current_City', ' '),
#                         'Current_Country': row.get('Current_Country', ' '),
#                         'PermAdd_same_CurrAdd': row.get('PermAdd_same_CurrAdd', ' '),
#                         'Permanent_Province': row.get('Permanent_Province', ' '),
#                         'Permanent_City': row.get('Permanent_City', ' '),
#                         'Permanent_Country': row.get('Permanent_Country', ' '),
#                         'Other_Country': row.get('Other_Country', ' '),
#                         'Nationality': row.get('Nationality', ' '),
#                         'Nationality_Other': row.get('Nationality_Other', ' '),
#                         'Travel_History': row.get('Travel_History', ' '),
#                         'Travel_History_Specify': row.get('Travel_History_Specify', ' '),
#                         'Client_Group': row.get('Client_Group', ' '),
#                         'Client_Group_Other': row.get('Client_Group_Other', ' '),
#                         'History_Of_Sex_Partner': row.get('History_Of_Sex_Partner', ' '),
#                         'Nationality_Sex_Partner': row.get('Nationality_Sex_Partner', ' '),
#                         'Date_of_Last_Sex': row.get('Date_of_Last_Sex', ' '),
#                         'Nationality_Sex_Partner_Other': row.get('Nationality_Sex_Partner_Other', ' '),
#                         'Number_Of_Sex_Partners': row.get('Number_Of_Sex_Partners', ' '),
#                         'Relationship_to_Partners': row.get('Relationship_to_Partners', ' '),
#                         'SB_Urethral': row.get('SB_Urethral', ' '),
#                         'SB_Vaginal': row.get('SB_Vaginal', ' '),
#                         'SB_Anal_Insertive': row.get('SB_Anal_Insertive', ' '),
#                         'SB_Oral_Insertive': row.get('SB_Oral_Insertive', ' '),
#                         'Sharing_of_Sex_Toys': row.get('Sharing_of_Sex_Toys', ' '),
#                         'SB_Oral_Receptive': row.get('SB_Oral_Receptive', ' '),
#                         'SB_Anal_Receptive': row.get('SB_Anal_Receptive', ' '),
#                         'SB_Others': row.get('SB_Others', ' '),
#                         'Sti_None': row.get('Sti_None', ' '),
#                         'Sti_Hiv': row.get('Sti_Hiv', ' '),
#                         'Sti_Hepatitis_B': row.get('Sti_Hepatitis_B', ' '),
#                         'Sti_Hepatitis_C': row.get('Sti_Hepatitis_C', ' '),
#                         'Sti_NGI': row.get('Sti_NGI', ' '),
#                         'Sti_Syphilis': row.get('Sti_Syphilis', ' '),
#                         'Sti_Chlamydia': row.get('Sti_Chlamydia', ' '),
#                         'Sti_Anogenital_Warts': row.get('Sti_Anogenital_Warts', ' '),
#                         'Sti_Genital_Ulcer': row.get('Sti_Genital_Ulcer', ' '),
#                         'Sti_Herpes': row.get('Sti_Herpes', ' '),
#                         'Sti_Other': row.get('Sti_Other', ' '),
#                         'Sti_Trichomoniasis': row.get('Sti_Trichomoniasis', ' '),
#                         'Sti_Mycoplasma_genitalium': row.get('Sti_Mycoplasma_genitalium', ' '),
#                         'Sti_Lymphogranuloma': row.get('Sti_Lymphogranuloma', ' '),
#                         'Illicit_Drug_Use': row.get('Illicit_Drug_Use', ' '),
#                         'Illicit_Drug_Specify': row.get('Illicit_Drug_Specify', ' '),
#                         'Abx_Use_Prescribed': row.get('Abx_Use_Prescribed', ' '),
#                         'Abx_Use_Prescribed_Specify': row.get('Abx_Use_Prescribed_Specify', ' '),
#                         'Abx_Use_Self_Medicated': row.get('Abx_Use_Self_Medicated', ' '),
#                         'Abx_Use_Self_Medicated_Specify': row.get('Abx_Use_Self_Medicated_Specify', ' '),
#                         'Abx_Use_None': row.get('Abx_Use_None', ' '),
#                         'Abx_Use_Other': row.get('Abx_Use_Other', ' '),
#                         'Abx_Use_Other_Specify': row.get('Abx_Use_Other_Specify', ' '),
#                         'Route_Oral': row.get('Route_Oral', ' '),
#                         'Route_Injectable_IV': row.get('Route_Injectable_IV', ' '),
#                         'Route_Dermal': row.get('Route_Dermal', ' '),
#                         'Route_Suppository': row.get('Route_Suppository', ' '),
#                         'Route_Other': row.get('Route_Other', ' '),
#                         'Symp_With_Discharge': row.get('Symp_With_Discharge', ' '),
#                         'Symp_No': row.get('Symp_No', ' '),
#                         'Symp_Discharge_Urethra': row.get('Symp_Discharge_Urethra', ' '),
#                         'Symp_Discharge_Vagina': row.get('Symp_Discharge_Vagina', ' '),
#                         'Symp_Discharge_Anus': row.get('Symp_Discharge_Anus', ' '),
#                         'Symp_Discharge_Oropharyngeal': row.get('Symp_Discharge_Oropharyngeal', ' '),
#                         'Symp_Pain_Lower_Abdomen': row.get('Symp_Pain_Lower_Abdomen', ' '),
#                         'Symp_Tender_Testicles': row.get('Symp_Tender_Testicles', ' '),
#                         'Symp_Painful_Urination': row.get('Symp_Painful_Urination', ' '),
#                         'Symp_Painful_Intercourse': row.get('Symp_Painful_Intercourse', ' '),
#                         'Symp_Rectal_Pain': row.get('Symp_Rectal_Pain', ' '),
#                         'Symp_Other': row.get('Symp_Other', ' '),
#                         'Outcome_Of_Follow_Up_Visit': row.get('Outcome_Of_Follow_Up_Visit', ' '),
#                         'Prev_Test_Pos': row.get('Prev_Test_Pos', ' '),
#                         'Prev_Test_Pos_Date': row.get('Prev_Test_Pos_Date', ' '),
#                         'Result_Test_Cure_Initial': row.get('Result_Test_Cure_Initial', ' '),
#                         'Result_Test_Cure_Followup': row.get('Result_Test_Cure_Followup', ' '),
#                         'NoTOC_Other_Test': row.get('NoTOC_Other_Test', ' '),
#                         'NoTOC_DatePerformed': row.get('NoTOC_DatePerformed', ' '),
#                         'NoTOC_Result_of_Test': row.get('NoTOC_Result_of_Test', ' '),
#                         'Patient_Compliance_Antibiotics': row.get('Patient_Compliance_Antibiotics', ' '),
#                         'OtherDrugs_Specify': row.get('OtherDrugs_Specify', ' '),
#                         'OtherDrugs_Dosage': row.get('OtherDrugs_Dosage', ' '),
#                         'OtherDrugs_Route': row.get('OtherDrugs_Route', ' '),
#                         'OtherDrugs_Duration': row.get('OtherDrugs_Duration', ' '),
#                         'Gonorrhea_Treatment': row.get('Gonorrhea_Treatment', ' '),
#                         'Treatment_Outcome': row.get('Treatment_Outcome', ' '),
#                         'Primary_Antibiotic': row.get('Primary_Antibiotic', ' '),
#                         'Primary_Abx_Other': row.get('Primary_Abx_Other', ' '),
#                         'Secondary_Antibiotic': row.get('Secondary_Antibiotic', ' '),
#                         'Secondary_Abx_Other': row.get('Secondary_Abx_Other', ' '),
#                         'Notes': row.get('Notes', ' '),
#                         'Clinic_Staff': row.get('Clinic_Staff', ' '),
#                         'Requesting_Physician': row.get('Requesting_Physician', ' '),
#                         'Telephone_Number': row.get('Telephone_Number', ' '),
#                         'Email_Address': row.get('Email_Address', ' '),
#                         'Date_Accomplished_Clinic': row.get('Date_Accomplished_Clinic', ' '),
#                         'Date_Requested_Clinic': row.get('Date_Requested_Clinic', ' '),
#                         'Date_Specimen_Collection': row.get('Date_Specimen_Collection', ' '),
#                         'Specimen_Code': row.get('Specimen_Code', ' '),
#                         'Specimen_Type': row.get('Specimen_Type', ' '),
#                         'Specimen_Quality': row.get('Specimen_Quality', ' '),
#                         'Date_Of_Gram_Stain': row.get('Date_Of_Gram_Stain', ' '),
#                         'Diagnosis_At_This_Visit': row.get('Diagnosis_At_This_Visit', ' '),
#                         'Gram_Neg_Intracellular': row.get('Gram_Neg_Intracellular', ' '),
#                         'Gram_Neg_Extracellular': row.get('Gram_Neg_Extracellular', ' '),
#                         'Gs_Presence_Of_Pus_Cells': row.get('Gs_Presence_Of_Pus_Cells', ' '),
#                         'Presence_GN_Intracellular': row.get('Presence_GN_Intracellular', ' '),
#                         'Presence_GN_Extracellular': row.get('Presence_GN_Extracellular', ' '),
#                         'GS_Pus_Cells': row.get('GS_Pus_Cells', ' '),
#                         'Epithelial_Cells': row.get('Epithelial_Cells', ' '),
#                         'GS_Date_Released': row.get('GS_Date_Released', ' '),
#                         'GS_Others': row.get('GS_Others', ' '),
#                         'GS_Negative': row.get('GS_Negative', ' '),
#                         'Gs_Gram_neg_diplococcus': row.get('Gs_Gram_neg_diplococcus', ' '),
#                         'Gs_NoGram_neg_diplococcus': row.get('Gs_NoGram_neg_diplococcus', ' '),
#                         'Gs_Not_performed': row.get('Gs_Not_performed', ' '),
#                         'Date_Received_in_lab': row.get('Date_Received_in_lab', ' '),
#                         'Positive_Culture_Date': row.get('Positive_Culture_Date', ' '),
#                         'Culture_Result': row.get('Culture_Result', ' '),
#                         'Growth': row.get('Growth', ' '),
#                         'Growth_span': row.get('Growth_span', ' '),
#                         'Species_Identification': row.get('Species_Identification', ' '),
#                         'Other_species_ID': row.get('Other_species_ID', ' '),
#                         'Specimen_Quality_Cs': row.get('Specimen_Quality_Cs', ' '),
#                         'Susceptibility_Testing_Date': row.get('Susceptibility_Testing_Date', ' '),
#                         'Retested_Mic': row.get('Retested_Mic', ' '),
#                         'Confirmation_Ast_Date': row.get('Confirmation_Ast_Date', ' '),
#                         'NAAT_ng': row.get('NAAT_ng', ' '),
#                         'NAAT_chl': row.get('NAAT_chl', ' '),
#                         'Beta_Lactamase': row.get('Beta_Lactamase', ' '),
#                         'PPng': row.get('PPng', ' '),
#                         'TRng': row.get('TRng', ' '),
#                         'Date_Released': row.get('Date_Released', ' '),
#                         'For_possible_WGS': row.get('For_possible_WGS', ' '),
#                         'Date_stocked': row.get('Date_stocked', ' '),
#                         'Location': row.get('Location', ' '),
#                         'abx_code': row.get('abx_code', ' '),
#                         'Laboratory_Staff': row.get('Laboratory_Staff', ' '),
#                         'Date_Accomplished_ARSP': row.get('Date_Accomplished_ARSP', ' '),
#                         'ars_notes': row.get('ars_notes', ' '),
#                         'ars_contact': row.get('ars_contact', ' '),
#                         'ars_email': row.get('ars_email', ' '),
#                         # Add other fields here as needed
#                     }
#                 )

#                 # Clear previous antibiotics for this entry
#                 AntibioticEntry.objects.filter(ab_idNumber_egasp=egasp_obj).delete()

#                 # Loop over antibiotics in the row
#                 for field in row:
#                     if field.endswith('_Val'):
#                         abx_code = field.replace('_Val', '')
#                         val = row.get(f'{abx_code}_Val', '').strip()
#                         ris = row.get(f'{abx_code}_RIS', '').strip()
#                         operand = row.get(f'{abx_code}_Op', '').strip()

#                         rt_val = row.get(f'{abx_code}_RT_Val', '').strip()
#                         rt_ris = row.get(f'{abx_code}_RT_RIS', '').strip()
#                         rt_operand = row.get(f'{abx_code}_RT_Op', '').strip()

#                         if not val and not rt_val:
#                             continue  # Skip if no values at all

#                         is_disk_abx = BreakpointsTable.objects.filter(
#                             Whonet_Abx=abx_code, Disk_Abx=True
#                         ).exists()

#                         abx_entry = AntibioticEntry(
#                             ab_idNumber_egasp=egasp_obj,
#                             ab_EgaspId=egasp_id,
#                             ab_Abx_code=abx_code,
#                         )

#                         if is_disk_abx:
#                             abx_entry.ab_Disk_value = val
#                             abx_entry.ab_Disk_RIS = ris
#                             abx_entry.ab_Retest_DiskValue = rt_val
#                             abx_entry.ab_Retest_Disk_RIS = rt_ris
#                         else:
#                             abx_entry.ab_MIC_value = val
#                             abx_entry.ab_MIC_RIS = ris
#                             abx_entry.ab_MIC_operand = operand
#                             abx_entry.ab_Retest_MICValue = rt_val
#                             abx_entry.ab_Retest_MIC_RIS = rt_ris
#                             abx_entry.ab_Retest_MIC_operand = rt_operand

#                         abx_entry.save()

#                         # Link antibiotic to matching breakpoints
#                         bp_matches = BreakpointsTable.objects.filter(Whonet_Abx=abx_code)
#                         if bp_matches.exists():
#                             abx_entry.ab_breakpoints_id.set(bp_matches)

#             messages.success(request, "CSV uploaded and data imported successfully.")
#             return redirect('show_data')
#     else:

#         messages.error(request, 'Error uploading file')
#         form = UploadDataForm()

#     return render(request, 'tables.html', {'upload_form': upload_form})

