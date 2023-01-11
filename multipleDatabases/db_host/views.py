from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
import pandas as pd
from . import db_configs
import json


def show_general_page(request):
    """
    Рендер главной страницы
    """
    return render(request, 'main_page.html')

def search(passport_id, job_title):
    """
    :param passport_id: паспорт работника
    :param job_title: занимаемая должность
    :return: таблица с его id, паспорт, должность, логин в системе,
    дата рождения, дата трудоустройства, зарплатная метка, часы отгула по болезни
    """
    engine, connection = db_configs.mssql_config()
    table = pd.read_sql_query(f"SELECT HumanResources.Employee.BusinessEntityID AS ID,"
                           "HumanResources.Employee.NationalIDNumber AS PASSPORT, "
                           "HumanResources.Employee.JobTitle AS POSITION, "
                           "HumanResources.Employee.LoginID AS LOGIN_ID, "
                           "CAST (HumanResources.Employee.BirthDate AS VARCHAR(50)) AS BITRHDAY, "
                           "CAST (HumanResources.Employee.HireDate AS VARCHAR(50)) AS HIRE_DATE, "
                           "CAST (HumanResources.Employee.SalariedFlag AS INT) AS SALARY_FLAG, "
                           "HumanResources.Employee.SickLeaveHours AS TimeOff "
                           "FROM HumanResources.Employee"
                           f" WHERE HumanResources.Employee.NationalIDNumber LIKE '%{passport_id}%' "
                           f"AND HumanResources.Employee.JobTitle LIKE '%{job_title}%'", connection)
    json_records = table.reset_index().to_json(orient='records')
    arr = []
    arr = json.loads(json_records)
    return arr

def execute_Search(request):
    try:
        if request.method == "POST":
            job_title = request.POST.get("job_title")
            passport = request.POST.get("passport")
            if job_title and passport:
                answer = search(passport_id=passport, job_title=job_title)
                return render(request, "main_page.html", {'data': answer, 'job_title': job_title, 'passport': passport})
            else:
                data = {
                    'job_title': job_title,
                    'passport': passport,
                }
                messages.error(request, 'ничего не найдено')
                return render(request, "main_page.html", data)
    except IntegrityError:
        data = {
            'job_title': job_title,
            'passport': passport,
        }
        messages.error(request, 'ничего не найдено')
        return render(request, "main_page.html", data)