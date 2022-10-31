from flask import (render_template, redirect, request, url_for, current_app, flash, make_response, flash)
from service.excel_import import blueprint
from flask.templating import render_template
from werkzeug.utils import secure_filename
import openpyxl
from service.database.models import request_pool, segment, wall_material, flat, condition
from service.extensions import db
from sqlalchemy import exc


def create_flat(rp_id, data):
    trans = {"да": True,
             "нет": False}
    if data[8].lower() in trans:
        have_balcony = trans[data[8].lower()]
    else:
        raise Exception(f"WRONG FORMAT: {data[3]}. In row:")
    return flat(request_pool_id=rp_id, floor=data[5], total_area=data[6], kitchen_area=data[7],
                have_balcony=have_balcony, minutes_metro_walk=data[9],
                condition_id=condition.query.filter_by(name=data[10].lower()).first().id, room_quantity=data[1])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


usecols = ['Местоположение', 'Количество комнат', 'Сегмент (Новостройка, современное жилье, старый жилой фонд)',
           'Этажность дома', 'Материал стен (Кипич, панель, монолит)', 'Этаж расположения', 'Площадь квартиры, кв.м',
           'Площадь кухни, кв.м', 'Наличие балкона/лоджии', 'Удаленность от станции метро, мин. пешком',
           'Состояние (без отделки, муниципальный ремонт, с современная отделка)']


@blueprint.route('/excel_import', methods=['GET', 'POST'])
def excel_import():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            dataframe = openpyxl.open(file)
            sheet = dataframe.active
            if not sheet:
                return 'Неверный формат файла'
            sheet_values = sheet.values
            col = 0
            for row in sheet_values:
                if usecols[0] in row:
                    try:
                        col = row.index('Местоположение')
                    except ValueError as VE:
                        return "Неверный формат файла: не был найден столбец 'Местоположение'"
                    break
            first = True
            for row in sheet_values:
                if first:
                    reqpl_data = row[col + 0:col + 5]
                    rp = request_pool(user_id=1, location=reqpl_data[0],
                                      segment_id=segment.query.filter_by(name=reqpl_data[2].lower()).first().id,
                                      floor_quantity=reqpl_data[3],
                                      wall_material_id=wall_material.query.filter_by(
                                          name=reqpl_data[4].lower()).first().id,
                                      )
                    db.session.add(rp)
                    db.session.flush()
                    first = False
                data = row[col:col + 11]
                print(data)
                try:
                    temp = create_flat(rp.id, data)
                except Exception as e:
                    db.session.close()
                    return ''.join(e.args) + str(row)
                db.session.add(temp)
            try:
                db.session.commit()
            except Exception as e:
                db.session.close()
                return ''.join(e.args) + str(row)

            return redirect(url_for('excel_import.choose_reference', id=rp.id))
        return "Not an allowed extension"  # TODO proper return page with an error
    return render_template('excel_import.html')


@blueprint.route('/<int:id>/choose_reference', methods=['POST', 'GET'])
def choose_reference(id):
    # TODO catch errors: req_pool id doesnt exist; flat id doesnt exist - None in request.args or flat dosnt exist
    req_pool = request_pool.query.filter_by(id=id).first()
    if request.method == "GET":
        return render_template('choose_reference.html', flats=req_pool.flats)
    elif request.method == "POST":
        reference_quantity = flat.query.filter_by(request_pool_id=req_pool.id).distinct(flat.id).count()
        print("REFErence quantity", reference_quantity)
        choosed_refq = int(request.form.get('reference_quantity'))
        print(choosed_refq, request.args)
        if choosed_refq == reference_quantity:
            for i in range(1, reference_quantity+1):
                id = request.form.get(i)
                flat.query.get(id).is_reference = True
            db.session.commit()
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
            return render_template('choose_reference.html', id=id, error=error)