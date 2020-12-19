import os
import qrcode
import base64
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def judge_filepath(file_type):
    img_list = ['bmp', 'jpeg', 'jpg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf',
                'ufo', 'eps', 'ai', 'raw', 'WMF', 'webp']
    doc_list = ['txt', 'doc', 'xls', 'ppt', 'docx', 'xlsx',
                'pptx', 'lrc', 'wps', 'zip', 'rar', '7z', 'torrent', 'pdf']
    video_list = ['cd', 'ogg', 'mp3', 'asf', 'wma', 'wav', 'mp3pro', 'rm', 'mp4', 'real', 'ape', 'module', 'midi',
                  'vqf']
    procedure_list = ['exe', 'py', 'java', 'class', 'pyc', 'app', 'apk', 'bat']
    if file_type in img_list:
        file_path = 'img'
    elif file_type in doc_list:
        file_path = 'doc'
    elif file_type in video_list:
        file_path = 'video'
    elif file_type in procedure_list:
        file_path = 'procedure'
    else:
        file_path = 'others'
    return file_path


def format_size(old_size):
    if old_size <= 1024:
        return str(old_size) + 'B'
    elif 1024 < old_size <= 1024 * 1024:
        new_size = round(old_size / 1024, 2)
        return str(new_size) + 'KB'
    elif 1024 * 1024 < old_size <= 1024 * 1024 * 1024:
        new_size = round(old_size / (1024 * 1024), 2)
        return str(new_size) + 'MB'
    elif old_size > 1024 * 1024 * 1024:
        new_size = round(old_size / (1024 * 1024 * 1024), 2)
        return str(new_size) + 'GB'


def gen_qrcode(user_name, file_name, pwd):
    user_name_b64 = base64.b64encode(
        user_name.encode()).decode().replace('/', '-').replace('+', '_')
    file_name_b64 = base64.b64encode(
        file_name.encode()).decode().replace('/', '-').replace('+', '_')
    pwd_b64 = base64.b64encode(pwd.encode()).decode().replace(
        '/', '-').replace('+', '_')
    # share_url = 'http://39.101.164.48:8000/download_share_file?user_name=' + user_name_b64 + '&file_name=' + file_name_b64 + '&pwd=' + pwd_b64
    share_url = 'http://127.0.0.1:9999/download_share_file?user_name=' + \
        user_name_b64 + '&file_name=' + file_name_b64 + '&pwd=' + pwd_b64

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(share_url)
    qr.make(fit=True)

    img = qr.make_image()
    # save_path = '1.png'
    save_dir = os.path.join(BASE_DIR, 'static', user_name, 'qr')
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    save_path = os.path.join(save_dir, file_name + '.png')
    img.save(save_path)
    with open(save_path, "rb") as f:
        img_str = base64.b64encode(f.read())
    return share_url, img_str.decode()
