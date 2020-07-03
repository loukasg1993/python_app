from django.shortcuts import render
from .models import personal_information, appointment
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import Createform, Createappointment
from django.contrib import messages
from django.http import Http404
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
import io
import matplotlib
import urllib, base64
import numpy as np
from django.core.paginator import Paginator
import pprint
import pandas as pd
import sys
import squarify
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import csv
from django.utils.encoding import smart_str
import xlwt
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from my_app.printing import MyPrint,MyPrints
from io import BytesIO

# Avoids this error: Tcl_AsyncDelete: async handler deleted by the wrong thread
matplotlib.use('Agg')


def editpost(request, id):
    obj = get_object_or_404(personal_information, pk=id)
    appointments = appointment.objects.filter(amka=id)

    form = Createform(request.POST or None, instance=obj)
    context = {'form': form}

    if form.is_valid():
        try:

            form.save()

            messages.success(request, "You successfully updated the patient's info")

            context = {'form': form, 'obj': obj}

            return redirect('editpost', id=id)
        except:
            return redirect('home')

    else:
        current_date = datetime.now()

        context = {'form': form, 'appointment': appointments, 'curr': current_date,
                   'error': 'The form was not updated successfully. Please enter in a title and content'}
        try:

            return render(request, 'my_app/new.html', context)
        except:
            return redirect('home')


def plot6():
    ages_10_20 = personal_information.objects.filter(age__gte=10, age__lte=20).count()
    ages_20_30 = personal_information.objects.filter(age__gt=20, age__lte=30).count()
    ages_30_40 = personal_information.objects.filter(age__gt=30, age__lte=40).count()
    ages_40_50 = personal_information.objects.filter(age__gt=40, age__lte=50).count()
    ages_50_60 = personal_information.objects.filter(age__gt=50, age__lte=60).count()
    ages_60 = personal_information.objects.filter(age__gt=60).count()

    all_patients = personal_information.objects.all().count()
    # count_fem=0
    # count_all=0
    # for i in female_bmi:
    #     count_fem+=1
    # for j in all_patients:
    #     count_all+=1
    # print(count_all)
    # print(count_fem)

    x = [ages_10_20, ages_20_30, ages_30_40, ages_40_50, ages_50_60, ages_60]
    labels = ['10 - 20', ' 20 - 30', ' 30 - 40', ' 40 - 50', ' 50 - 60', ' > 60']
    y_pos = np.arange(len(labels))

    plt.bar(y_pos, x)
    # , counterclock = False
    plt.title("Patient Ages")
    plt.xticks(y_pos, labels)
    plt.ylabel('Count')
    plt.ylim(50, 320)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uris = urllib.parse.quote(string)
    plt.close()
    return (uris)


def plot4():
    ages_10_20 = personal_information.objects.filter(age__gte=10, age__lte=20).count()
    ages_20_30 = personal_information.objects.filter(age__gt=20, age__lte=30).count()
    ages_30_40 = personal_information.objects.filter(age__gt=30, age__lte=40).count()
    ages_40_50 = personal_information.objects.filter(age__gt=40, age__lte=50).count()
    ages_50_60 = personal_information.objects.filter(age__gt=50, age__lte=60).count()
    ages_60 = personal_information.objects.filter(age__gt=60).count()

    all_patients = personal_information.objects.all().count()
    # count_fem=0
    # count_all=0
    # for i in female_bmi:
    #     count_fem+=1
    # for j in all_patients:
    #     count_all+=1
    # print(count_all)
    # print(count_fem)

    x = ((ages_10_20 / all_patients) * 100, (ages_20_30 / all_patients) * 100, (ages_30_40 / all_patients) * 100,
         (ages_40_50 / all_patients) * 100, (ages_50_60 / all_patients) * 100, (ages_60 / all_patients) * 100)
    labels = ['10 - 20', ' 20 - 30', ' 30 - 40', ' 40 - 50', ' 50 - 60', ' > 60']

    plt.pie(x, labels=labels, colors=["lightgreen", "deepskyblue", "tomato", "plum", "lightcoral", "khaki"],
            shadow=True, explode=(0, 0.1, 0, 0.1, 0.1, 0), startangle=90, radius=0.8 , autopct = '%1.1f%%')
    # , autopct = '%1.1f%%'
    # , counterclock = False
    plt.title("Patient Ages")

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uris = urllib.parse.quote(string)
    plt.close()
    return (uris)


def plot3():
    female_bmi = personal_information.objects.filter(sex="female").count()
    all_patients = personal_information.objects.all().count()

    # count_fem=0
    # count_all=0
    # for i in female_bmi:
    #     count_fem+=1
    # for j in all_patients:
    #     count_all+=1
    # print(count_all)
    # print(count_fem)

    x = ((female_bmi / all_patients) * 100, 100 - (female_bmi / all_patients) * 100)
    labels = ['Female', 'Male']

    plt.pie(x, labels=labels, colors=["lightsalmon", "lightskyblue"], shadow=True, explode=(0, 0.1), startangle=70,
            autopct='%1.1f%%', radius=0.8)

    plt.title("Sex Percentage of Patients")

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uris = urllib.parse.quote(string)
    plt.close()
    return (uris)


def plot1():
    female_bmi = personal_information.objects.filter(sex="female")
    male_bmi = personal_information.objects.filter(sex="male")
    bmi_fem = []
    bmi_male = []
    for i in female_bmi:
        p = i.bmi
        bmi_fem.append(p)
    for i in male_bmi:
        p = i.bmi
        bmi_male.append(p)
    count = 0
    g = 0
    for i in male_bmi:
        y = i.bmi
        g = g + y
        count += 1
    c = g / count
    count = 0
    g = 0
    for i in female_bmi:
        y = i.bmi
        g = g + y
        count += 1
    k = g / count
    n = [k, c]
    names = ('Female', 'Male')
    y_pos = np.arange(len(names))

    plt.bar(y_pos, n, color="mediumorchid", width=0.6)
    plt.xlabel('')
    plt.title("Average Bmi by gender")
    plt.ylabel('Body Mass Index')
    plt.ylim(30, 32)
    plt.xticks(y_pos, names)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uris = urllib.parse.quote(string)
    plt.close()
    return (uris)


def plot5():
    now_date = datetime.today().date()

    last = now_date + timedelta(days=-365)
    last_year = last.year
    dose = appointment.objects.filter(date__contains=last_year)
    doses = []
    # dates=[]
    # for i in dose:
    #     l=i.date
    #
    #     dates.append(l)
    # print(type(l))
    # print(dates)
    for i in dose:
        p = i.dose
        doses.append(p)
    # print(doses)
    # print(len(doses))

    n = 8
    final = [doses[i * n:(i + 1) * n] for i in range((len(doses) + n - 1) // n)]
    # print(final)
    #
    # print(len(final))

    new_list = []
    for i in range(240):
        count = 0
        for j in final[i]:
            count = count + j
        new_list.append(count)
    # print(new_list)
    # print(len(new_list))
    # names=range(1,17)
    y_pos = np.arange(240)
    plt.plot(y_pos, new_list, marker='.', color="lightseagreen")
    # linestyle = 'dotted'
    last_year = str(last_year)
    plt.title("Summary of Dose for Everyday in Year "+last_year)
    plt.ylabel('Dose')
    plt.xlabel('Days')

    # plt.ylim(1700, 1900)
    #
    #
    # plt.xticks(y_pos, names)
    #
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return (uri)


def plot2():
    now_date = datetime.today().date()

    last = now_date + timedelta(days=-365)
    last_year = last.year

    dose = appointment.objects.filter(date__contains=last_year)
    doses = []
    for i in dose:
        p = i.dose
        doses.append(p)
    # print(doses)
    # print(len(doses))

    n = 120
    final = [doses[i * n:(i + 1) * n] for i in range((len(doses) + n - 1) // n)]
    # print(final)
    #
    # print(len(final))

    new_list = []
    for i in range(0, 16):
        count = 0
        for j in final[i]:
            count = count + j
        new_list.append(count)
    names = range(1, 17)
    y_pos = np.arange(16)
    plt.bar(y_pos, new_list, color="royalblue")
    plt.xlabel('d')
    last_year=str(last_year)
    plt.title("Summary of Dose each 15 Days in Year "+ last_year)
    plt.ylabel('Dose')
    plt.xlabel('Days')
    plt.ylim(27000, 29000)

    plt.xticks(y_pos, names)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return (uri)


def plot7():
    x = [1, 2, 3, 4, 5]
    y1 = [5, 4, 3, 6, 4]
    y2 = [8, 6, 4, 5, 4]
    y3 = [9, 7, 5, 4, 4]

    y = np.vstack([y1, y2, y3])

    labels = ["Fibonacci ", "Evens", "Odds"]

    fig, ax = plt.subplots()
    ax.stackplot(x, y1, y2, y3, labels=labels)
    # ax.legend(loc='upper left')
    # plt.show()

    fig, ax = plt.subplots()
    ax.stackplot(x, y)
    ax.set_xlim(1, 5)
    plt.axis('off')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.0)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return (uri)


def plot8():
    x = [1, 2, 3, 4, 5]
    y1 = [2, 6, 2, 4, 5]
    y2 = [1, 5, 2, 6, 8]
    y3 = [3, 4, 5, 7, 9]

    y = np.vstack([y1, y2, y3])

    labels = ["Fibonacci ", "Evens", "Odds"]

    fig, ax = plt.subplots()
    ax.stackplot(x, y1, y2, y3, labels=labels)
    # ax.legend(loc='upper left')
    # plt.show()

    fig, ax = plt.subplots()
    ax.stackplot(x, y)
    ax.set_xlim(1, 5)
    plt.axis('off')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.0)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return (uri)


def plot9():
    x = [1, 2, 3, 4, 5]
    y1 = [4, 6, 8, 4, 5]
    y2 = [4, 5, 8, 6, 5]
    y3 = [4, 4, 8, 7, 5]

    y = np.vstack([y1, y2, y3])

    labels = ["Fibonacci ", "Evens", "Odds"]

    fig, ax = plt.subplots()
    ax.stackplot(x, y1, y2, y3, labels=labels)
    # ax.legend(loc='upper left')
    # plt.show()

    fig, ax = plt.subplots()
    ax.stackplot(x, y)
    ax.set_xlim(1, 5)
    plt.axis('off')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.0)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return (uri)


def plot10():
    pi = personal_information.objects.all()

    height = []
    weight = []
    bmi = []
    for i in pi:
        height.append(i.height)
        weight.append(i.weight)
        bmi.append(i.bmi)

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(height, weight, bmi, marker='^', color='#5c29db')
    ax.set_xlim(1.5, 2)
    ax.set_ylim(40, 175)
    ax.set_zlim(14, 55)
    ax.set_xlabel('Height')
    ax.set_ylabel('Weight')
    ax.set_zlabel('Bmi')

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.0)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return (uri)
def plot11():
    now_date = datetime.today().date()
    this_year = str(now_date.year)
    last = now_date + timedelta(days=-365)
    last_year = str(last.year)
    bmi_now = appointment.objects.filter(date__contains=this_year)
    bmi_last = appointment.objects.filter(date__contains=last_year)
    bmi_n = []
    bmi_l=[]

    for i in bmi_now:

        bmi_n.append(i.bmi)
    for j in bmi_last:
        bmi_l.append(j.bmi)
    # df=pd.DataFrame()
    # df['Now_Bmi']=pd.Series(bmi_n)
    # df['Last_Bmi']=pd.Series(bmi_l)


    plt.figure(figsize=(16, 10), dpi=80)

    sns.kdeplot(bmi_n, shade=True, color="#4596d9", label=this_year, alpha=.7)
    sns.kdeplot(bmi_l, shade=True, color="#c9d950", label=last_year, alpha=.7)
    plt.title('Density Plot of Bmi Distribution', fontsize=18)
    plt.xlabel('Bmi',fontsize=18)
    plt.ylabel('Density',fontsize=18)

    plt.legend( title='Year',fontsize=30)
    plt.xlim(10,55)







    fig = plt.gcf()
    # fig.set_size_inches(18.5, 6.5)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return (uri)

def showplots(request):
    x = plot1()
    y = plot2()
    z = plot3()
    k = plot4()
    a = plot5()
    l = plot6()
    n = plot10()
    m=plot11()

    return render(request, "my_app/showplots.html",
                  {'data': x, 'data2': y, 'data3': z, 'data4': k, 'data5': a, 'data6': l, 'data10': n,'data11':m})


def home(request):
    current_date = datetime.now()

    patients = personal_information.objects.all().count()
    female = personal_information.objects.filter(sex="female").count()
    male = personal_information.objects.filter(sex="male").count()
    charges = personal_information.objects.all()
    now_date = datetime.today().date()

    plot = plot7()
    plot84 = plot8()
    plot94 = plot9()

    if now_date.isoweekday() == 5:
        tomorrow = now_date + timedelta(days=3)
    elif now_date.isoweekday() == 6:
        tomorrow = now_date + timedelta(days=2)
    else:
        tomorrow = now_date + timedelta(days=1)
    doses_tomorrow = appointment.objects.filter(date__contains=tomorrow)
    count_dose = 0
    for i in doses_tomorrow:
        p = i.dose
        count_dose = count_dose + p
    char = 0
    for i in charges:
        char = char + i.charges
    count_dose=round(count_dose,3)
    context = {'curr': current_date, 'patients': patients, 'male': male, 'female': female, 'char': char,
               'count_dose': count_dose, 'plot7': plot, 'plot8': plot84, 'plot9': plot94}

    return render(request, 'base.html', context)



def tomorrowpdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tomorrow_dose.pdf"'

    buffer = BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.pdf_tomorrow()

    response.write(pdf)
    return response

def lastyearpdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="last_year.pdf"'

    buffer = BytesIO()

    report = MyPrints(buffer, 'Letter')
    pdf = report.pdf_tomorrow()

    response.write(pdf)
    return response


def tomorrow_dose(request):

    now_date = datetime.today().date()

    if now_date.isoweekday() == 5:
        tomorrow = now_date + timedelta(days=3)
    elif now_date.isoweekday() == 6:
        tomorrow = now_date + timedelta(days=2)
    else:
        tomorrow = now_date + timedelta(days=1)
    doses_tomorrow = appointment.objects.filter(date__contains=tomorrow)
    # .values_list('id','amka','dose','date')
    total_dose = 0
    amka = []
    date = []
    dose = []
    for i in doses_tomorrow:
        p = i.dose
        amka.append(i.amka)
        dose.append(i.dose)
        date.append(i.date)
        total_dose = total_dose + p
    df = pd.DataFrame()
    df['amka'] = amka

    df['date'] = date
    df['dose'] = dose
    df['empty'] = None
    df['total_dose'] = None
    df['total_dose'][0] =total_dose
    df['Mbq'] = None
    df['Mbq'][0]='MBq s  '


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tomorrow_dose.csv"'
    writer = csv.writer(response)
    writer.writerow(['Amka', 'Date', 'Dose', '', 'Total Dose',''])

    for index, row in df.iterrows():
        writer.writerow(row)
    return response
def lastyear(request):
    now_date = datetime.today().date()

    last=now_date + timedelta(days=-365)
    last_year=last.year
    last_year_info = appointment.objects.filter(date__contains=last_year)
    # .values_list('id','amka','dose','date')
    total_dose = 0
    total_bmi=0
    id=[]
    amka = []
    bmi = []
    dose = []
    date = []

    for i in last_year_info:
        p = i.dose
        bm = i.bmi
        id.append(i.id)
        amka.append(i.amka)
        bmi.append(i.bmi)
        dose.append(i.dose)
        date.append(i.date)
        total_bmi = total_bmi +bm
        total_dose = total_dose + p
    avg_bmi = total_bmi/len(bmi)
    avg_dose = total_dose/len(dose)

    df = pd.DataFrame()
    df['id'] = id
    df['amka'] = amka
    df['bmi'] = bmi

    df['date'] = date
    df['dose'] = dose

    df['empty'] = None
    df['avg_bmi'] = None
    df['avg_bmi'][0] =avg_bmi
    df['avg_dose'] = None
    df['avg_dose'][0] = avg_dose


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="last_year.csv"'
    writer = csv.writer(response)
    writer.writerow(['id','Amka','bmi', 'Date', 'Dose', '', 'Average Bmi','Average Dose'])

    for index, row in df.iterrows():
        writer.writerow(row)
    return response

def view_all(request):
    current_date = datetime.now()

    personal_info_list = personal_information.objects.all().order_by('-id')

    paginator = Paginator(personal_info_list, 25)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    personal_info = paginator.get_page(page_number)

    # .order_by("-added_date")
    context = {"personal_info": personal_info, 'curr': current_date}

    return render(request, 'my_app/index.html', context)


@csrf_exempt
def add_patient(request):
    if request.method == "POST":
        try:

            patient_info = personal_information()
            patient_info.name = request.POST.get('name')
            patient_info.age = request.POST.get('age')
            patient_info.sex = request.POST.get('sex')
            patient_info.height = request.POST.get('height')
            patient_info.weight = request.POST.get('weight')
            patient_info.bmi = request.POST.get('bmi')
            patient_info.children = request.POST.get('children')
            patient_info.smoker = request.POST.get('smoker')
            patient_info.region = request.POST.get('region')
            patient_info.charges = request.POST.get('charges')
            patient_info.telephone_no = request.POST.get('telephone_no')
            patient_info.address = request.POST.get('address')

            patient_info.save()
            context = {'smoker': patient_info.smoker}
            return render(request, "my_app/add_new.html",context)
        except:
            return redirect('home')

    return render(request, "my_app/add_new.html")


@csrf_exempt
def deleteapp(request, appointment_id):
    appointment.objects.get(id=appointment_id).delete()
    return redirect('home')


@csrf_exempt
def delete2(request, personal_information_id):
    personal_information.objects.get(id=personal_information_id).delete()
    # obj = get_object_or_404(personal_information, id=personal_information_id)
    # form = Createform(request.POST or None, instance=obj)
    return render(request, ",my_app/new.html", {"personal_information": personal_information})


@csrf_exempt
def delete(request, personal_information_id):
    personal_information.objects.get(id=personal_information_id).delete()
    # obj = get_object_or_404(personal_information, id=personal_information_id)
    # form = Createform(request.POST or None, instance=obj)
    return HttpResponseRedirect('/view/')


def view_all_appointments(request):
    current_date = datetime.now()

    appoint_info_list = appointment.objects.all().order_by('-date')
    paginator = Paginator(appoint_info_list, 25)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)
    context = {"appointment": appointments, 'curr': current_date}
    return render(request, 'my_app/indexapp.html', context)


def detail_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["personal_info"] = personal_information.objects.get(id=id)

    return render(request, "my_app/random.html", context)


def list(request):
    if request.method == "GET":
        try:
            search = request.GET['content']
            search = int(search)
            if personal_information.objects.get(pk=search) == None:

                return redirect('home')

            else:
                return redirect('editpost', id=search)



        except:
            return redirect('home')
    return redirect('home')


def dates1():
    x = appointment.objects.latest('date')
    last_date = x.date
    current_date = datetime.now(timezone.utc)
    y = last_date - current_date
    day_diff = y.days
    last_hour = last_date.hour



    if current_date < last_date and day_diff <= 14:

        if last_date.weekday() < 4:
            if last_hour < 16:
                app_date = last_date + timedelta(hours=1)
            elif last_hour == 16:
                app_date = last_date + timedelta(hours=17)

        elif last_date.weekday() == 4:
            if last_hour < 16:
                app_date = last_date + timedelta(hours=1)

            elif last_hour == 16:
                app_date = last_date + timedelta(days=2, hours=17)


    elif current_date > last_date:
        if current_date.weekday() < 4:
            tomorrowdate = current_date + timedelta(days=1)
            days = tomorrowdate.day
            months = tomorrowdate.month
            years = tomorrowdate.year
            app_date = datetime(year=years, month=months, day=days, hour=9)
        if current_date.weekday() == 4:
            tomorrowdate = current_date + timedelta(days=3)
            days = tomorrowdate.day
            months = tomorrowdate.month
            years = tomorrowdate.year
            app_date = datetime(year=years, month=months, day=days, hour=9)
        if current_date.weekday() == 5:
            tomorrowdate = current_date + timedelta(days=2)
            days = tomorrowdate.day
            months = tomorrowdate.month
            years = tomorrowdate.year
            app_date = datetime(year=years, month=months, day=days, hour=9)
        elif current_date.weekday() == 6:
            tomorrowdate = current_date + timedelta(days=1)
            days = tomorrowdate.day
            months = tomorrowdate.month
            years = tomorrowdate.year
            app_date = datetime(year=years, month=months, day=days, hour=9)
    else:
        return None

    return app_date
@csrf_exempt
def make_appointment(request, id):
    current_dates = datetime.now()
    obj = get_object_or_404(personal_information, id=id)
    forms = Createform(request.POST or None, instance=obj)
    context = {'form': forms}
    date = dates1()
    if request.method == "POST":

        if date is None:
            return redirect('home')
        else:
            dates = datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
            if forms.is_valid():
                try:



                    obj = forms.save(commit=False)

                    obj.save()

                    messages.success(request, "You successfully updated the post")

                    context = {'form': forms, 'date': dates}

                    return render(request, 'my_app/appointment.html', context)
                except:

                    return redirect('home')

            else:

                context = {'form': forms, 'date': dates, 'curr': current_dates,
                           'error': 'The form was not updated successfully. Please enter in a title and content'}
                try:
                    return render(request, 'my_app/appointment.html', context)
                except:

                    return redirect('home')


@csrf_exempt
def addapp(request):
    if request.method == "POST":
        try:
            appointments = appointment()

            appointments.amka = request.POST.get('amka')
            appointments.bmi = request.POST.get('bmi')
            appointments.dose = request.POST.get('dose')
            appointments.date = request.POST.get('date')
            appointments.save()

            return redirect('addapp')
        except:

            return redirect('home')

    return redirect('home')


def schedule(request):
    current_date = datetime.now()
    return render(request, "my_app/schedule.html", {'curr': current_date})
