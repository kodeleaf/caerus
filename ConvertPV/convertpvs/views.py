from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import  Add_Profile
from .generatexml import generate_xml

import logging

import os
import datetime
import pathlib
import shutil
import glob
import zipfile

# folder paths
obj = Add_Profile.objects.last()
XML_FILE_PATH = ""
JSON_FILE_PATH =  ""
ARCHIEVE_FILE_PATH =  ""

logger = logging.getLogger('caerusApp')

def admin(request):
    allprofiles = Add_Profile.objects.all()
    print(allprofiles)

def xml_file_details(path):
    files_details = []
    dir_name = f'{path}\\'
    # Get list of all files only in the given directory

    list_of_files = filter(os.path.isfile, glob.glob(dir_name + '*'))
    # Sort list of files based on last modification time in ascending order
    files = sorted(list_of_files, key=os.path.getmtime, reverse=True)
    # files = os.listdir(path)
    # important
    if len(files) > 0:
        for a in files:
            i = os.path.split(a)[1]
            individual_file_details = []
            file_name = f'{path}\\{i}'
            if pathlib.Path(file_name).suffix.lower() == '.xml':
                # file name
                individual_file_details.append(i)

                # file size
                size = os.path.getsize(file_name) / (1024)
                individual_file_details.append(f'{round(size, 0)}kb')

                # file modification time
                modification_time = os.path.getmtime(file_name)
                y = datetime.datetime.fromtimestamp(modification_time)
                individual_file_details.append(y.strftime('%x %X'))

                files_details.append(individual_file_details)
    return files_details


def json_file_details(path):
    files_details = []

    dir_name = f'{path}\\'
    # Get list of all files only in the given directory

    list_of_files = filter(os.path.isfile, glob.glob(dir_name + '*'))
    # Sort list of files based on last modification time in ascending order
    files = sorted(list_of_files, key=os.path.getmtime, reverse=True)

    # important
    if len(files) > 0:
        for a in files:
            i = os.path.split(a)[1]
            file_name = f'{path}\\{i}'
            individual_file_details = []

            if pathlib.Path(file_name).suffix.lower() == '.xml':
                # file name
                individual_file_details.append(i)

                # file size
                size = os.path.getsize(file_name) / (1024)
                individual_file_details.append(f'{round(size, 0)}kb')

                # file creation time
                creation_time = os.path.getctime(file_name)
                x = datetime.datetime.fromtimestamp(creation_time)

                individual_file_details.append(x.strftime('%x %X'))

                files_details.append(individual_file_details)
    return files_details


# ------------------------------------------------------------    END Function
@login_required(login_url='/admin')
def files(request):
    logger.info('text')
    allprofiles = Add_Profile.objects.all()
    print(allprofiles)

    profile_data = Add_Profile.objects.first()

    # old_path = os.getcwd() + '//in_xml_data//'
    old_path = "D:\\Kapish Project\\Nanda Sir\\Project\\caerus_1_0\\caerus 1\\caerus1\\in_xml_data"
    xml_files_data = xml_file_details(path=old_path)

    # new_path = os.getcwd() + '//out_json_data//'
    new_path =""
    json_files_data = json_file_details(path=new_path)
    profile_data = Add_Profile.objects.all()

    data = {
        # 'xml' and 'json' files details
        'profile_data': profile_data,
        'file_details': xml_files_data,
        'new_file_details': json_files_data,
        'allprofile': allprofiles,
        # no. of 'json' and 'xml' file
        'length': len(xml_files_data),
        'no_of_json_files': len(json_files_data),
    }

    return render(request, 'admin/index.html', data)


def fileConverion(request):
    allprofiles = Add_Profile.objects.all()
    print(allprofiles)
    test_data= 23
    print(test_data)
    return HttpResponse(test_data)
    mydata = Add_Profile.objects.all()

    context = {
        'allprofile': mydata,
    }
    # return render(request, 'admin/index.html', context)
    new_path = settings.JSON_FILE_PATH
    status = ''
    try:
        # help to create a folder
        directory = "Archieve"

        path = os.path.join(settings.XML_FILE_PATH, directory)
        # print(path)
        os.mkdir(path)


    except FileExistsError:

        pass
    finally:
        length = 0
        # help to create files
        # length = int(request.POST.get('number'))
        try:
            length = int(request.POST.get('number'))
        except TypeError:
            pass

        source = settings.XML_FILE_PATH
        # destination = f'{source}\Archieve'
        destination = settings.ARCHIEVE_FILE_PATH
        # folder paths

        # destination =new_path
        for i in range(1, length + 1):
            get_value = request.POST.get('file' + str(i))

            # copy file frome one location to another
            if get_value != None:
                try:
                    file_perfix = get_value.split('.xml')[0]
                    file_suffix = '_r3_converted'
                    in_file = get_value  # for database(in_file_name)
                    out_file = file_perfix + file_suffix + '.xml'  # for database(out_file name)
                    if generate_xml((os.path.join(source, in_file)), (os.path.join(new_path, out_file))):
                        status = 'True'
                        creation_time = os.path.getctime(
                            os.path.join(new_path, out_file))  # for database(modification time)
                        x = datetime.datetime.fromtimestamp(creation_time)

                        # to sent data into database
                        # obj = audit_log(in_file_name=in_file, out_file_name=out_file,
                        #                 converted_datetime=x.strftime('%x %X'), user_name=request.user.username,
                        #                 status=status)
                        # obj.save()
                        shutil.move(os.path.join(source, get_value),
                                    os.path.join(settings.ARCHIEVE_FILE_PATH, get_value))

                    else:
                        x = datetime.datetime.now()
                        status = 'False'
                        # obj = audit_log(in_file_name=in_file, out_file_name='null',
                        #                 converted_datetime=x.strftime('%x %X'), user_name=request.user.username,
                        #                 status=status)
                        # obj.save()
                    # shutil.move(f'{source}\\{get_value}', f'{destination}\\{get_value}')
                    # to sent data into database


                except  Exception as e:
                    logger.error('An error occured while conversion', e)
                    pass

        # file_details function call
        json_files_deta = json_file_details(path=new_path)

        xml_files_data = xml_file_details(path=source)
        new_data = {
            # 'xml' and 'json' files details
            'new_file_details': json_files_deta,
            'no_of_json_files': len(json_files_deta),
            # no. of 'xml' and 'json' files
            'file_details': xml_files_data,
            'length': len(xml_files_data),
        }
        logger.info('View accessed')

    # return render(request, 'admin\caerus_templates\conversion.html', new_data)
    return  HttpResponse(test_data)


def download_file(request, file):
    try:
        # help to download single file
        path = settings.JSON_FILE_PATH
        file_path = os.path.join(path, file)
        response = FileResponse(open(file_path, 'rb'))
        file_name = file
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        logger.info(f'{file_name}json_file downloaded successfully')
        return response
    except:
        logger.error('json_file download failed')


def view_file(request, file, view):
    try:
        path = settings.JSON_FILE_PATH
        if view == 'r2':

            path = settings.XML_FILE_PATH


        else:

            path = settings.JSON_FILE_PATH

        file_path = os.path.join(path, file)
        response = FileResponse(open(file_path, 'rb'))
        file_name = file
        response['Content-Disposition'] = 'inline; filename=' + file_name
        logger.info(f'{file}Viewed successfully')
        return response
    except:
        logger.error(f'IN viewing: {file} ')


# ***************************************************************************************************
def download_zip_files(request):
    # help to download multiple files
    data = str(request.GET['post_id'])
    multiple_file_names = data.split(',')
    path = settings.JSON_FILE_PATH

    zip_file_name = os.path.join(path, "SelectedFiles.zip")
    with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
        for i in multiple_file_names:
            if i.endswith('.json'):
                # file_name = os.path.basename(path + i)
                file_name = os.path.basename(os.path.join(path, i))
                # zip_file.write(path+i, file_name)
                zip_file.write(os.path.join(path, i), file_name)

    file_path = os.path.join(path, 'json786.zip')

    response = FileResponse(open(file_path, 'rb'))
    # file_name = 'json786.zip'
    response['Content-Disposition'] = 'attachment; filename =' + file_name
    return response


def Profile(request):
    mydata = Add_Profile.objects.all()

    context = {
        'mymembers': mydata,
    }
    return render(request, 'ConvertPV/templates/admin/index.html', context)

