import difflib
import csv
from io import BytesIO
from django.shortcuts import render
import pandas as pd
from .forms import CSVUploadForm,LoginForm,UserRegistartionForm
from django.db import connection
from .models import CSVData,Profile
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login



def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                
                return render(request,'myapp/upload.html')
                
            else:
                return HttpResponse("Invalid login")

    else:
       form = LoginForm()
    return render(request,'myapp/login.html',{'form':form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistartionForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,'myapp/home.html')
    else:
        user_form = UserRegistartionForm()
    return render(request,'myapp/register.html',{'user_form': user_form})


# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST,request.FILES)
        
        if form.is_valid():
            # Check if the uploaded file is a CSV
            file_name = request.FILES['csv_file'].name
            if not file_name.endswith('.csv'):
                return JsonResponse({'error': 'Invalid file format. Please upload a CSV file.'})

            #read the contents of the file using pandas
            df = pd.read_csv(request.FILES['csv_file'])
            #Find unit price using formula
            df['unit_price'] = df['CIF Value']/df['Stat Quantity']
            df['unit_price'] = df['unit_price'].apply(lambda x: round(x, 2))
            #grouped using groupby function
            grouped = df.groupby('M2_Declaration_Number')
            print(grouped)
            #find a average of unitprice
            group_averages = grouped['unit_price'].mean()
            print(group_averages)
            def check_price(row):
                group_avg = group_averages[row['M2_Declaration_Number']]
                group_avg_p = (group_avg*10)/100
                group_avg_pl = group_avg - group_avg_p
                group_avg_o = group_avg + group_avg_p
                if row['unit_price'] < group_avg_pl:
                    return "Undervalue"
                elif row['unit_price'] > group_avg_o:
                    return "Overvalue"
                else :
                    return "Expected"   
            df['Test'] = df.apply(check_price, axis=1)
            # Assuming your dataset is stored in a pandas DataFrame called `df`

            
        def check_price2(row):
                #split GOODS_DESCRIPTION using .split function
                expected_words = row['GOODS_DESCRIPTION'].split()
                print(expected_words)  
                #convert COMMODITY_DESC into upper letter using upper function for avoid case sensitive 
                commodity_desc = row['COMMODITY_DESC'].upper()
                print(commodity_desc)
                #loop for compare each word with commodity_desc 
                for word in expected_words:
                    print(f"Is '{word}' in '{commodity_desc}'? {word in commodity_desc}")
                #use any function is any word is match
                commodity_contains_expected = any(word in commodity_desc for word in expected_words)
                print(commodity_contains_expected)
                
                if commodity_contains_expected == True:
                      
                    print("one or more expected word")
                    return "True"
                    
                else:
                    print(f"Item is an expected import/export.")
                    return "False"
                  
        df['Test2'] = df.apply(lambda row: check_price2(row), axis=1) 
        df = df.drop(['Unnamed: 0'], axis=1) 

         # Add default value for CIF_Value if not present in the CSV file
        if 'CIF Value' not in df.columns:
                df['CIF Value'] = 0
            
            # Create a list of CSVData instances from the DataFrame rows
            
        csv_data_list = []
        for _, row in df.iterrows():
            existing_records = CSVData.objects.filter(
                Index=row['index'],
                M2_Declaration_Number=row['M2_Declaration_Number'],
                COMMODITY_DESC=row['COMMODITY_DESC'],
                GOODS_DESCRIPTION=row['GOODS_DESCRIPTION'],
                Stat_Quantity=row['Stat Quantity'],
                CIF_Value=row['CIF Value'],
                unit_price=row['unit_price'],
                Test=row['Test'],
                Test2=row['Test2']
            )
            if not existing_records:
                csv_data_list.append(CSVData(
                    Index=row['index'],
                    M2_Declaration_Number=row['M2_Declaration_Number'],
                    COMMODITY_DESC=row['COMMODITY_DESC'],
                    GOODS_DESCRIPTION=row['GOODS_DESCRIPTION'],
                    Stat_Quantity=row['Stat Quantity'],
                    CIF_Value=row['CIF Value'],
                    unit_price=row['unit_price'],
                    Test=row['Test'],
                    Test2=row['Test2']
            ))
        # Bulk insert the CSVData instances to the database
        CSVData.objects.bulk_create(csv_data_list) 
        
       # csv_data_list = [CSVData(
                
        #       Index = row['index'],
         #       COMMODITY_DESC = row['COMMODITY_DESC'],
          #      GOODS_DESCRIPTION = row['GOODS_DESCRIPTION'],
           #     Stat_Quantity=row['Stat Quantity'],
            #   CIF_Value=row['CIF Value'],
             #   unit_price=row['unit_price'],
             #   Test=row['Test'],
              #  Test2=row['Test2']
         #   ) for _, row in df.iterrows()]
            
            # Bulk insert the CSVData instances to the database
        #CSVData.objects.bulk_create(csv_data_list)
        #csv_data_list.save()
        #pass the dataframe to a templates
        return render(request,'myapp/data.html',{'data':df.to_html()})       
        
    else:
        form = CSVUploadForm()
    return render(request,'myapp/upload_csv.html',{'form':form})


def download_excel(request):
    
    # Get the data from the database
    data = CSVData.objects.all().values()
    df = pd.DataFrame(data)  # retrieve data from database or create DataFrame
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    filename = 'data.xlsx'
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


