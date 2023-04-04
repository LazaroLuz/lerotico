import os
import shutil
import glob
from multiprocessing import Process

import requests
from PIL import Image

from flask import Blueprint, jsonify, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_parameter
from core.models import Comic, Link, Videos


views = Blueprint('views', __name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'assistir')


@views.route('api/v1/comic/<id>/')
def comics(id):
    comic = Comic.get(Comic.id == id)
    revista = Link.select().join(Comic).where(Comic.id == comic)
    base_img = [b.urls for b in revista]
    return jsonify({'nome': comic.name, 'base_img': base_img})


@views.route('/')
def registro():
    q = request.args.get('search')
    if q:
        itens = Comic.select().where(Comic.name.contains(q)).order_by(Comic.name)
    else:
        itens = Comic.select().order_by(Comic.name)
    first_img = []
    for item in itens:
        imagem = Link.select().join(Comic).where(Comic.name == item.name)
        img_first = [b for b in imagem]

        try:
            first_img.append(img_first[0])
        except IndexError:
            continue

    def get_users(off_set=0, per_pages=20):
        """
        :type off_set: valor int
        :type per_pages: valor int
        """
        return first_img[off_set:off_set + per_pages]

    # page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', offset_parameter='off_set')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    offset = (page - 1) * per_page
    pagination_users = get_users(off_set=offset, per_pages=per_page)
    # pagination = Pagination(page=page, total=itens.count(), per_page=40, record_name=first_img)
    pagination = Pagination(page=page, total=itens.count(), per_page=per_page, css_framework='bootstrap5')

    return render_template('teste.html', users=pagination_users, page=page, per_page=per_page, first_img=first_img, pagination=pagination)


@views.route('api/v1/comic/all/')
def home():
    listas = []
    comics = [n.name for n in Comic.select()]
    for nome in comics:
        revista = Link.select().join(Comic).where(Comic.name == nome)
        base_img = [b.urls for b in revista]
        listas.append({'nome': nome, 'base_img': base_img})
    return jsonify(listas)


@views.route('revista/<int:id>/')
def photos(id):
    comic = Comic.get(Comic.id == id)
    revista = Link.select().join(Comic).where(Comic.id == comic)
    base_img = [b.urls for b in revista]
    p = Process(target=download, args=(comic.name, base_img))
    p.start()
    # download(comic.name, base_img)
    return render_template('index.html', base_img=base_img, comic=comic)


def download(name, imgs):
    os.makedirs(f'assert/{name}', exist_ok=True)
    photos_m = []
    for img in imgs:
        photos_m.append(os.path.basename(img))
        response = requests.get(img, timeout=None).content
        with open(os.path.join(f'assert/{name}', os.path.basename(img)), 'wb') as file:
            file.write(response)
    if f'{name}.pdf' in os.listdir('./static'):
        pass
    else:
        imagem1 = Image.open(os.path.join(f"assert/{name}", photos_m[0])).convert('RGB')
        del photos_m[0]
        imgs = []
        for img in photos_m:
            fot = Image.open(os.path.join(f"assert/{name}", img)).convert("RGB")
            imgs.append(fot)
        imagem1.save(f"static/{name}.pdf", save_all=True, append_images=imgs)

    shutil.rmtree(f"assert/{name}")
    # codigo abaixo tranforma em zip
    # shutil.make_archive(f'{name}', 'zip', f'assert/', f'{name}')


@views.route('pdf/<nome>/', methods=['GET', 'POST'])
def pdf(nome):
    return redirect(url_for('static', filename=f'{nome}.pdf'))


@views.route('arquivo/<nome>', methods=['GET', 'POST'])
def arquivo(nome):
    return render_template('download.html', nome=nome)


@views.route('video/')
def video():
    # videos = os.listdir('Donwload/images')
    # videos = glob.glob('Donwload/images/*.jpg')
    videos = Videos.select()

    def get_users(off_set=0, per_pages=12):
        """
        :type off_set: valor int
        :type per_pages: valor int
        """
        return videos[off_set:off_set + per_pages]
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 12
    offset = (page - 1) * per_page
    users = get_users(off_set=offset, per_pages=per_page)
    pagination = Pagination(page=page, total=videos.count(), per_page=per_page, css_framework='bootstrap5')

    return render_template('video.html', users=users, pagination=pagination)


@views.route('assistir/')
def assistir():
    nome = request.args.get('q')
    get_video = Videos.get(id=nome)
    # return render_template('assistir.html', video_finale=video_finale[1].split('>')[0])
    html = f"{get_video.link.replace('510', '900').replace('400', '650')}"

    return html


@views.route('upload/', methods=['POST'])
def upload():
    if request.files['movie']:
        file = request.files['movie']
        savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(savePath)
        return redirect(url_for('views.video'))
    return 'video não enviado'
