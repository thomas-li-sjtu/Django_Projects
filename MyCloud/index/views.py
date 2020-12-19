import base64
import datetime
import os
import shutil
import hashlib
import base64

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import csrf
from django.utils import timezone
from django.utils.http import urlquote

from index import models
from index.utils import format_size, gen_qrcode, judge_filepath

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@login_required
def index(request):
    user = request.user
    ua = request.GET.get('ua', '')
    user_id = User.objects.get(username=user).id
    file_obj = models.FileInfo.objects.filter(
        user_id=user_id, belong_folder='')
    folder_obj = models.FolderInfo.objects.filter(
        user_id=user_id, belong_folder='')
    if not ua:
        index_list = []
        for file in file_obj:
            file.is_file = True
            index_list.append(file)
        for folder in folder_obj:
            folder.is_file = False
            index_list.append(folder)
        breadcrumb_list = [{'tag': '全部文件', 'uri': ''}]
        return render(request, 'index.html',
                      {'index_list': index_list, 'username': str(user), 'breadcrumb_list': breadcrumb_list})
    elif ua == 'pyqt':
        file_list = []
        folder_list = []
        for f in file_obj:
            file_list.append({
                'file_name': f.file_name,
                'file_path': f.file_path,
                'file_type': f.file_type,
                'file_size': f.file_size,
                'update_time': f.update_time,
                'belong_folder': f.belong_folder
            })
        for f in folder_obj:
            folder_list.append({
                'folder_name': f.folder_name,
                'update_time': f.update_time,
                'belong_folder': f.belong_folder
            })
        return JsonResponse({'file_list': file_list, 'folder_list': folder_list})
    else:
        return render(request, '404.html')


@login_required
def folder(request):
    user = request.user
    ua = request.GET.get('ua', '')
    pdir = request.GET.get('pdir')
    user_id = User.objects.get(username=user).id
    if pdir:
        if pdir[-1:] == '/':
            belong_folder = pdir
        else:
            belong_folder = pdir + '/'
    else:
        belong_folder = ''
    file_obj = models.FileInfo.objects.filter(
        user_id=user_id, belong_folder=belong_folder)
    folder_obj = models.FolderInfo.objects.filter(
        user_id=user_id, belong_folder=belong_folder)
    if not ua:
        index_list = []
        for file in file_obj:
            file.is_file = True
            index_list.append(file)
        for folder in folder_obj:
            folder.is_file = False
            index_list.append(folder)
        breadcrumb_list = [{'tag': '全部文件', 'uri': ''}]
        uri = ''
        for value in pdir.split('/'):
            if value:
                uri = uri + value + '/'
                breadcrumb_list.append({'tag': value, 'uri': uri})
        return render(request, 'index.html',
                      {'index_list': index_list, 'username': str(user), 'breadcrumb_list': breadcrumb_list})
    elif ua == 'pyqt':
        file_list = []
        folder_list = []
        for f in file_obj:
            file_list.append({
                'file_name': f.file_name,
                'file_path': f.file_path,
                'file_type': f.file_type,
                'file_size': f.file_size,
                'update_time': f.update_time,
                'belong_folder': f.belong_folder
            })
        for f in folder_obj:
            folder_list.append({
                'folder_name': f.folder_name,
                'update_time': f.update_time,
                'belong_folder': f.belong_folder
            })
        return JsonResponse({'file_list': file_list, 'folder_list': folder_list})
    else:
        return render(request, '404.html')


@login_required
def delete_file(request):
    if request.method == 'GET':
        return redirect('/folder/?pdir=' + pwd)
    elif request.method == 'POST':
        ua = request.POST.get('ua', '')
        if ua == 'pyqt':
            user_name = request.POST.get('user_name')
        else:
            user_name = str(request.user)
        file_path = request.POST.get('file_path')
        pwd = request.POST.get('pwd')
        user_obj = User.objects.get(username=user_name)
        user_id = user_obj.id
        file_obj = models.FileInfo.objects.filter(
            file_path=file_path, user_id=user_id)
        print('path', file_path)
        for i in file_obj:
            i.delete()
        try:
            os.remove(BASE_DIR + '/static/' + file_path)
        except Exception as e:
            print(e)
        if ua == 'pyqt':
            return JsonResponse({
                'delete_flag': True
            })
        else:
            return redirect('/folder/?pdir=' + pwd)


@login_required
def share_file(request):
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        ua = request.POST.get('ua', '')
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd', '')
        user_name = request.POST.get('user_name')
        user_obj = User.objects.get(username=user_name)
        user_id = user_obj.id
        file_name = request.POST.get('file_name')
        share_duration = int(request.POST.get('share_duration'))
        file_sharecode = request.POST.get('file_sharecode')
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(days=share_duration)
        file_obj = models.FileInfo.objects.get(
            belong_folder=pwd, file_name=file_name, user_id=user_id)
        file_path = file_obj.file_path
        file_size = file_obj.file_size
        share_url, qr_str = gen_qrcode(user_name, file_name, pwd)
        share_obj = models.ShareInfo.objects.filter(
            user_id=user_id, file_path=file_path)
        if share_obj:
            share_obj.update(start_time=start_time,
                             end_time=end_time, file_sharecode=file_sharecode)
        else:
            share_obj = models.ShareInfo.objects.create(user_id=user_id, file_path=file_path, file_sharecode=file_sharecode,

                                                        file_name=file_name, start_time=start_time, end_time=end_time, file_size=file_size,
                                                        belong_folder=pwd, share_url=share_url)
        return JsonResponse({
            'share_flag': True,
            'file_sharecode': file_sharecode,
            'share_url': share_url,
            'qr_str': qr_str
        })


# 下载某一用户分享的文件 /download_share_file?user_name=&file_name=&pwd=
def download_share_file(request):
    user_name = base64.b64decode(request.GET.get('user_name', '').replace(
        '-', '/').replace('_', '+').encode()).decode()
    file_name = base64.b64decode(request.GET.get('file_name', '').replace(
        '-', '/').replace('_', '+').encode()).decode()
    pwd = base64.b64decode(request.GET.get('pwd', '').replace(
        '-', '/').replace('_', '+').encode()).decode()
    user_obj = User.objects.get(username=user_name)
    user_id = user_obj.id
    file_sharecode = request.POST.get('sharecode', '')
    if request.method == 'GET':
        share_obj = models.ShareInfo.objects.filter(
            user_id=user_id, belong_folder__exact=pwd, file_name=file_name)
        if not share_obj:
            return render(request, '404.html')
        return render(request, 'share.html')
    elif request.method == 'POST':
        share_obj = models.ShareInfo.objects.filter(
            user_id=user_id, belong_folder__exact=pwd, file_name=file_name, file_sharecode__exact=file_sharecode)
        if share_obj:
            # share_obj = models.ShareInfo.objects.get(user_id=user_id, belong_folder__exact=pwd, file_name=file_name, file_sharecode__exact=file_sharecode)
            file_path = share_obj[0].file_path
            file_dir = BASE_DIR + '/static/' + file_path
            file = open(file_dir, 'rb')
            print(file_dir)
            response = FileResponse(file)
            response['status'] = 'success'
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment;filename={urlquote(file_name)}'
            return response
        else:
            return render(request, 'share.html', {'info': "提取码错误"})


@login_required
def rename_file(request):
    if request.method == 'GET':
        return redirect('/folder/?pdir=' + pwd)
    elif request.method == 'POST':
        ua = request.POST.get('ua', '')
        if ua == 'pyqt':
            user_name = request.POST.get('user_name')
        else:
            user_name = str(request.user)
        user_id = User.objects.get(username=user_name).id
        old_file_name = request.POST.get('old_file_name')
        file_suffix = old_file_name.split('.')[-1]
        new_file_name = request.POST.get('new_file_name')+'.'+file_suffix
        pwd = request.POST.get('pwd', '')
        file_obj = models.FileInfo.objects.get(
            belong_folder=pwd, file_name=old_file_name, user_id=user_id)
        old_path = file_obj.file_path
        new_path = old_path.replace(old_file_name, new_file_name)
        file_obj.file_path = new_path
        old_full_path = BASE_DIR + '/static/' + old_path
        new_full_path = BASE_DIR + '/static/' + new_path
        os.rename(old_full_path, new_full_path)
        file_obj.file_name = new_file_name
        file_obj.save()
        share_obj = models.ShareInfo.objects.filter(
            belong_folder=pwd, file_name=old_file_name, user_id=user_id)
        if share_obj:
            share_obj[0].file_path = new_path
            share_obj[0].file_name = new_file_name
            share_obj[0].save()
        if ua == 'pyqt':
            return JsonResponse({
                'rename_flag': True
            })
        else:
            return redirect('/folder/?pdir=' + pwd)
    # models.FileInfo.objects.get(file_path=file_path, user_id=user_id).delete()


@login_required
def rename_folder(request):
    user = str(request.user)
    user_id = User.objects.get(username=user).id
    old_folder_name = request.GET.get('old_folder_name')
    new_folder_name = request.GET.get('new_folder_name')
    pwd = request.GET.get('pwd')
    folder_obj = models.FolderInfo.objects.get(
        belong_folder=pwd, folder_name=old_folder_name, user_id=user_id)
    folder_obj.folder_name = new_folder_name
    old_belong_folder = folder_obj.belong_folder + old_folder_name + '/'
    new_belong_folder = folder_obj.belong_folder + new_folder_name + '/'
    old_full_path = BASE_DIR + '/static/' + user + '/' + old_belong_folder
    new_full_path = BASE_DIR + '/static/' + user + '/' + new_belong_folder
    os.rename(old_full_path, new_full_path)
    folder_belong_folder_objs = models.FolderInfo.objects.filter(belong_folder__startswith=old_belong_folder,
                                                                 user_id=user_id)
    for folder_belong_folder_obj in folder_belong_folder_objs:
        tmp_belong_folder = folder_belong_folder_obj.belong_folder.replace(
            old_belong_folder, new_belong_folder)
        folder_belong_folder_obj.belong_folder = tmp_belong_folder
        folder_belong_folder_obj.save()
    file_belong_folder_objs = models.FileInfo.objects.filter(belong_folder__startswith=old_belong_folder,
                                                             user_id=user_id)
    for file_belong_folder_obj in file_belong_folder_objs:
        tmp_belong_folder = file_belong_folder_obj.belong_folder.replace(
            old_belong_folder, new_belong_folder)
        file_belong_folder_obj.belong_folder = tmp_belong_folder
        file_belong_folder_obj.save()
    folder_obj.save()
    return redirect('/folder/?pdir=' + pwd)


@login_required
def delete_folder(request):
    user = request.user
    pwd = request.GET.get('pwd')
    folder_name = request.GET.get('folder_name')
    try:
        models.FolderInfo.objects.filter(
            belong_folder__contains=folder_name).delete()
        models.FolderInfo.objects.filter(folder_name=folder_name).delete()
        models.FileInfo.objects.filter(
            belong_folder__contains=folder_name).delete()
        rm_dir = BASE_DIR + '/static/' + str(user) + '/' + pwd + folder_name
        shutil.rmtree(rm_dir)
    except Exception as e:
        print(e)
    return redirect('/folder/?pdir=' + pwd)


@login_required
def mkdir(request):
    ua = request.GET.get('ua', '')
    user = request.user
    user_id = User.objects.get(username=user).id
    pwd = request.GET.get('pwd')
    folder_name = request.GET.get('folder_name')
    update_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    if not ua:
        try:
            models.FolderInfo.objects.create(user_id=user_id, folder_name=folder_name, belong_folder=pwd,
                                            update_time=update_time)
            user_path = os.path.join(BASE_DIR, 'static', str(user))
            os.mkdir(user_path + '/' + pwd + folder_name)
        except Exception as e:
            print(e)
        return redirect('/folder/?pdir=' + pwd)
    elif ua == "pyqt":
        try:
            models.FolderInfo.objects.create(user_id=user_id, folder_name=folder_name, belong_folder=pwd,
                                            update_time=update_time)
            user_path = os.path.join(BASE_DIR, 'static', str(user))
            os.mkdir(user_path + '/' + pwd + folder_name)
        except Exception as e:
            return JsonResponse({"error_info": e})
    else:
        return render(request, '404.html')


@login_required
def download_file(request):
    ua = request.GET.get('ua', '')
    file_path = request.GET.get('file_path')
    file_name = file_path.split('/')[-1]
    file_dir = BASE_DIR + '/static/' + file_path
    if ua == 'pyqt':
        CHUNK_SIZE = 1048576
        file = []
        file_all = b''
        with open(file_dir, 'rb') as f:
            while True:
                a = f.read(CHUNK_SIZE)
                if len(a):
                    a_base64 = base64.encodebytes(a).decode("utf-8")
                    file_all += a
                    # size_finish += len(a)
                    # self.upload_process[filename] = size_finish / size_all
                    file.append(a_base64)
                else:
                    f.close()
                    break
        response = {'length': len(file),
                    "file_name": file_name
                    }
        md5 = hashlib.md5(file_all).hexdigest()
        response["md5"] = md5
        for index, d in enumerate(file):
            response[f'data{index}'] = d
        return JsonResponse(response)
    else:
        file = open(file_dir, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename={urlquote(file_name)}'
        return response


@login_required
def upload_file(request):
    if request.method == "GET":
        return redirect('/')
    elif request.method == "POST":
        ua = request.POST.get('ua', '')
        if ua == 'pyqt':
            data = []
            user_name = request.POST.get('user_name', '')
            user_obj = User.objects.get(username=user_name)
            file_type = request.POST.get('type', '')
            length = int(request.POST.get('length'))
            for i in range(length):
                data.append(base64.b64decode(
                    request.POST.get(f'data{i}', '')))
            # data_all = ''.join(data).encode()
            data_all = b''
            for i in data:
                data_all += i
            md5 = request.POST.get('md5', '')
            md5_ = hashlib.md5(data_all).hexdigest()
            if md5 != md5_:
                return JsonResponse({
                    "upload_flag": False,
                    "error_info": "MD5 error!"
                })
            pwd = request.POST.get('pwd', '')
            file_type = judge_filepath(file_type)
            file_size = format_size(len(data_all))
            file_name = request.POST.get('file_name', '')
        else:
            user_name = str(request.user)
            user_obj = User.objects.get(username=user_name)
            file_obj = request.FILES.get('file')
            file_type = judge_filepath(file_obj.name.split('.')[-1].lower())
            pwd = request.POST.get('file_path')
            file_size = format_size(file_obj.size)
            file_name = file_obj.name

        update_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        file_suffix = file_name.split('.')[-1]
        file_version = 0
        save_path = BASE_DIR + '/static/' + user_name + '/' + pwd
        file_path = user_name + '/' + pwd + file_name

        file_obj_exist = models.FileInfo.objects.filter(
            belong_folder=pwd, file_type=file_type, file_name__icontains=file_name, user_id=user_obj.id)
        while (file_obj_exist):
            file_version += 1
            file_name = file_name.replace(
                '.'+file_suffix, (f'({file_version})' if file_version else '')+'.'+file_suffix)
            file_obj_exist = models.FileInfo.objects.filter(
                belong_folder=pwd, file_type=file_type, file_path=file_path, file_name__icontains=file_name, user_id=user_obj.id)

        file_path = file_path.replace(
            '.'+file_suffix, (f'({file_version})' if file_version else '') + '.' + file_suffix)

        models.FileInfo.objects.create(user_id=user_obj.id, file_path=file_path,
                                       file_name=file_name, update_time=update_time, file_size=file_size,
                                       file_type=file_type, belong_folder=pwd)
        if ua == 'pyqt':
            with open(save_path + file_name, 'wb+') as f:
                for i in data:
                    f.write(i)
                f.close()
            return JsonResponse({
                "upload_flag": True,
            })
        else:
            with open(save_path + file_name, 'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            return redirect('/')


@login_required
def file_type(request):
    user = request.user
    file_type = request.GET.get('file_type')
    user_id = User.objects.get(username=user).id
    file_list = []
    if file_type == 'all':
        file_obj = models.FileInfo.objects.filter(user_id=user_id)
    else:
        file_obj = models.FileInfo.objects.filter(
            file_type=file_type, user_id=user_id)
    for file in file_obj:
        file_list.append({'file_id': file.id, 'file_path': file.file_path, 'file_name': file.file_name,
                          'update_time': str(file.update_time), 'file_size': file.file_size,
                          'file_type': file.file_type})
    return JsonResponse(file_list, safe=False)


@login_required
def search(request):
    file_type = request.GET.get('file_type')
    file_name = request.GET.get('file_name')
    user = request.user
    user_id = User.objects.get(username=user).id
    file_list = []
    if file_type == 'all':
        file_obj = models.FileInfo.objects.filter(
            file_name__icontains=file_name, user_id=user_id)
    else:
        file_obj = models.FileInfo.objects.filter(
            file_type=file_type, file_name__icontains=file_name, user_id=user_id)
    for file in file_obj:
        file_list.append({'file_path': file.file_path, 'user_id': user_id, 'file_name': file.file_name,
                          'update_time': str(file.update_time), 'file_size': file.file_size,
                          'file_type': file.file_type})
    return JsonResponse(file_list, safe=False)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        ua = request.POST.get('ua', '')
        user = auth.authenticate(username=username, password=password)
        if not ua:
            if user:
                auth.login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'info': '用户名或密码错误'})
        elif ua == 'pyqt':
            if user:
                auth.login(request, user)
                return JsonResponse({'login_flag': True})
            else:
                return JsonResponse({'login_flag': False})
        else:
            return render(request, '404.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        # 去除空格
        username = username.rstrip()
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        ua = request.POST.get('ua', '')
        user_path = os.path.join(BASE_DIR, 'static', username)
        if not ua:
            if password == repassword:
                try:
                    User.objects.create_user(
                        username=username, password=password)
                except:
                    return render(request, 'register.html', {'info': '用户已存在'})
                os.mkdir(user_path)
                os.mkdir(os.path.join(user_path, 'qr'))
            else:
                return render(request, 'register.html', {'info': '两次密码不一致'})
            return redirect('/login')
        elif ua == 'pyqt':
            if password == repassword:
                try:
                    User.objects.create_user(
                        username=username, password=password)
                except:
                    return JsonResponse({'register_flag': False, 'error_info': '用户已存在'})
                os.mkdir(user_path)
                os.mkdir(os.path.join(user_path, 'qr'))
            else:
                return JsonResponse({'register_flag': False, 'error_info': '两次密码不一致'})
            return JsonResponse({'register_flag': True})
        else:
            return render(request, '404.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def page_not_found(request, exception):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def get_csrf(request):
    # 生成 csrf token
    if request.method == 'GET':
        csrf_token = csrf(request)['csrf_token']
        return HttpResponse(csrf_token)
