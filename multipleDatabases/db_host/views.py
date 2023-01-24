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


def search(phone_number):
    """
    :param phone_number: номер телефона
    :return: все возможные данные о пользователе по заданному номеру телефона
    """
    engine, connection = db_configs.mssql_config()
    file = open("user_info.txt", 'w')
    tables_name = sql_scripts.get_table_names(engine=engine)
    for name in tables_name:
        info_about_user = pd.read_sql_query(f"""SELECT * from [{name}]
                                             WHERE phone_number LIKE '{phone_number}%'""", connection)
        if info_about_user is not None:
            file.write(f"В таблице: {name} найдена следующая информация\n"
                       f" Персональные данные пользовател(я/ей) с номером телефона похожим на: {phone_number}\n"
                       f" {info_about_user}")
    return file
def execute_Search(request):
    try:
        if request.method == "POST":
            phone = request.POST.get("phone")
            passport = request.POST.get("passport")
            if phone:
                answer = search(phone_number=phone)
                return render(request, "main_page.html", {'phone': phone})
            else:
                data = {
                    'phone': phone,
                }
                messages.error(request, 'ничего не найдено')
                return render(request, "main_page.html", data)
    except IntegrityError:
        data = {
            'phone': phone,
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