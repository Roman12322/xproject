from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
import pandas as pd
from . import db_configs
from . import sql_scripts
import json


def show_general_page(request):
    """
    Рендер главной страницы
    """
    return render(request, 'main_page.html')


def show_upload_leak_file_form(request):
    """
    Рендер страницы для загрузки утечек в базу данных
    """
    return render(request, 'add_leaks_form.html')


def search(passport_id, phone_number):
    """
    :param passport_id: паспорт пользователя
    :param phone_number: номер телефона
    :return: все возможные данные из таблиц утечек
    """
    engine, connection = db_configs.mssql_config()
    table = pd.read_sql_query()
    json_records = table.reset_index().to_json(orient='records')
    arr = []
    arr = json.loads(json_records)
    return arr


def execute_Search(request):
    try:
        if request.method == "POST":
            phone = request.POST.get("phone")
            passport = request.POST.get("passport")
            if phone and passport:
                answer = search(passport_id=passport, phone_number=phone)
                return render(request, "main_page.html", {'data': answer, 'phone': phone, 'passport': passport})
            else:
                data = {
                    'phone': phone,
                    'passport': passport,
                }
                messages.error(request, 'ничего не найдено')
                return render(request, "main_page.html", data)
    except IntegrityError:
        data = {
            'phone': phone,
            'passport': passport,
        }
        messages.error(request, 'ничего не найдено')
        return render(request, "main_page.html", data)


def upload_leak(request):
    try:
        if request.method == "POST":
            leak_file = request.FILES["leak_file"]
            try:
                engine, connection = db_configs.mssql_config()
                df = pd.read_csv(request.FILES['leak_file'].temporary_file_path(), sep=';', encoding='UTF-8')
                df_sql_version = df.to_sql(f'{leak_file.name}_leak', connection, index=False)
                answer = 'Successfully updated to database'
                data = {
                    'ans': answer
                }
                return render(request, "add_leaks_form.html", data)
            except:
                answer = 'Please, change file-encoding to UTF-8'
                data = {
                    'ans': answer
                }
                return render(request, "add_leaks_form.html", data)
    except IntegrityError:
        data = {
            'ans': answer
        }
        messages.error(request, 'ничего не найдено')
        return render(request, "add_leaks_form.html", data)