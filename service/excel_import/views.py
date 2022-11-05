import xlrd
from flask import (redirect, request, url_for, current_app, make_response, flash)
from service.excel_import import blueprint
from flask.templating import render_template
import openpyxl
from service.database.models import request_pool, segment, wall_material, flat, condition, room_quantity, user, floor, \
    analogue_flat
from service.extensions import db
from service.excel_import.parser import parse
from flask_login import login_required, current_user

@blueprint.before_app_first_request
def cradmin():
    conf = current_app.config
    if not user.query.filter_by(username='admin').first() and conf.get('ADMIN_PASSWORD'):
        us = user(username='admin', first_name='fname_admin', last_name='lname_admin', is_admin=True,
                  email=conf.get('ADMIN_EMAIL'))
        us.set_password(conf['ADMIN_PASSWORD'])
        db.session.add(us)
        db.session.commit()

@blueprint.context_processor
def inject_user():
    return dict(user=current_user)


def create_flat(rp, data):
    trans = {"да": True,
             "нет": False}
    if data[8].lower() in trans:
        have_balcony = trans[data[8].lower()]
    else:
        raise Exception(f"WRONG FORMAT: {data[8]}. In row:")
    room_q = str(data[1]).lower()
    if rp.floor_quantity == int(data[5]):
        flr = floor.query.filter_by(name='last').first().id
    elif int(data[5]) == 1:
        flr = floor.query.filter_by(name='first').first().id
    else:
        flr = floor.query.filter_by(name='mid').first().id
    return flat(request_pool_id=rp.id, floor_id=flr, total_area=data[6], kitchen_area=data[7],
                have_balcony=have_balcony, minutes_metro_walk=data[9],
                condition_id=condition.query.filter_by(name=data[10].lower()).first().id,
                room_quantity_id=room_quantity.query.filter_by(name=room_q).first().id,
                )


def allowed_file(filename):
    extension = filename.rsplit('.', 1)
    if '.' in filename and extension and extension[1] in current_app.config['ALLOWED_EXTENSIONS']:
        return extension[1]
    return False


usecols = ['Местоположение', 'Количество комнат', 'Сегмент (Новостройка, современное жилье, старый жилой фонд)',
           'Этажность дома', 'Материал стен (Кипич, панель, монолит)', 'Этаж расположения', 'Площадь квартиры, кв.м',
           'Площадь кухни, кв.м', 'Наличие балкона/лоджии', 'Удаленность от станции метро, мин. пешком',
           'Состояние (без отделки, муниципальный ремонт, с современная отделка)']


@blueprint.route('/excel_import', methods=['GET', 'POST'])
@login_required
def excel_import():
    if request.method == 'POST':
        file = request.files['file']
        extension = allowed_file(file.filename)
        if file and extension:
            if extension == 'xlsx':
                dataframe = openpyxl.open(file)
                sheet = dataframe.active
                if not sheet:
                    return 'Неверный формат файла'
                sheet_values = sheet.values
            elif extension == 'xls':
                dataframe = xlrd.open_workbook(file_contents=file.stream.read())
                sheet = dataframe.sheet_by_index(0)
                if not sheet:
                    return 'Неверный формат файла'
                sheet_values = (list(map(lambda x: x.value, sheet.row(i))) for i in range(sheet.nrows))
            col = None
            for row in sheet_values:
                if usecols[0] in row:
                    try:
                        col = row.index('Местоположение')
                    except ValueError as VE:
                        return "Неверный формат файла: не был найден столбец 'Местоположение'"
                    break
            if col is None:
                return 'Wrong format'  # TODO a proper error page (flash() and return same page)
            first = True
            for row in sheet_values:
                if first:
                    reqpl_data = row[col + 0:col + 5]
                    rp = request_pool(user_id=current_user.id, location=reqpl_data[0],
                                      segment_id=segment.query.filter_by(name=reqpl_data[2].lower()).first().id,
                                      floor_quantity=reqpl_data[3],
                                      wall_material_id=wall_material.query.filter_by(
                                          name=reqpl_data[4].lower()).first().id,
                                      )
                    db.session.add(rp)
                    db.session.flush()
                    first = False
                data = row[col:col + 11]
                try:
                    temp = create_flat(rp, data)
                    db.session.add(temp)
                except Exception as e:
                    db.session.close()
                    return ''.join(e.args) + str(row)
            try:
                db.session.commit()
            except Exception as e:
                db.session.close()
                return ''.join(e.args) + str(row)

            return redirect(url_for('excel_import.choose_reference', id=rp.id))
        return "Not an allowed extension"  # TODO proper return page with an error
    return render_template('excel_import.html')


@blueprint.route('/<int:id>/choose_reference', methods=['POST', 'GET'])
@login_required
def choose_reference(id):
    # TODO catch errors: req_pool id doesnt exist; flat id doesnt exist - None in request.args or flat dosnt exist
    req_pool = request_pool.query.filter_by(id=id).first()
    if request.method == "GET":
        return render_template('choose_reference.html', flats=req_pool.flats)
    elif request.method == "POST":
        reference_quantity = flat.query.filter_by(request_pool_id=req_pool.id).distinct(flat.room_quantity_id).count()
        print("REFErence quantity", reference_quantity)
        choosed_refq = int(request.form.get('reference_quantity'))
        print(choosed_refq, request.args)
        if choosed_refq == reference_quantity:
            ref_objects = []
            for i in range(1, reference_quantity + 1):
                id = request.form.get(str(i))
                print(id)
                fl = flat.query.get(id)
                fl.is_reference = True
                ref_objects.append(fl)
            db.session.commit()
            analogue_flats = parse(ref_objects, req_pool, current_app)
            for ref_anfl in len(analogue_flats):
                for an_objects in analogue_flats[ref_anfl]:
                    an_flat = analogue_flat(flat_id=ref_objects[ref_anfl].id, location=an_objects['location'],
                                  total_area=an_objects['total_area'], kitchen_area=an_objects['kitchen_area'],
                                  have_balcony=an_objects['have_balcony'], price=int(an_objects['price']),
                                  condition_id=condition.query.filter_by(name=an_objects['condition']).first().id,
                                  minutes_metro_walk=int(an_objects['minutes_metro_walk']),
                                  floor_id=floor.query.filter_by(name=an_objects['floor']).first().id,
                                  )

            return 'OK'
        else:
            # TODO message about incorrect value of choosed references!!!!!!!!!!!
            ref_obj = "эталонный объект"
            if 2 <= reference_quantity <= 4:
                ref_obj = "эталонных объекта"
            elif reference_quantity >= 5:
                ref_obj = "эталонных объектов"
            error = f'Необходимо выбрать {reference_quantity} {ref_obj}. Вы выбрали: {choosed_refq}.'
            flash(error, 'error')
            return render_template('choose_reference.html', flats=req_pool.flats, id=id, error=error)


@blueprint.route('/check', methods=['POST', 'GET'])
@login_required
def check():
    fl = flat.query.first()
    req_pool = fl.request_pool
    ref_objects = [fl,]
    return parse(ref_objects, req_pool, current_app)
