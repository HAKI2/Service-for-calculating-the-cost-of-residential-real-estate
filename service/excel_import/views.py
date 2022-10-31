from flask import (render_template, redirect, request, url_for, current_app, flash, make_response)
from service.excel_check import blueprint
from flask.templating import render_template
from werkzeug.utils import secure_filename
import openpyxl
from service.database.models import request_pool, segment, wall_material, flat, condition
from service.extensions import db
from sqlalchemy import exc


def create_flat(rp_id, data):
    trans = {"да": True,
             "нет": False}
    if data[3].lower() in trans:
        have_balcony = trans[data[3].lower()]
    else:
        raise Exception(f"WRONG FORMAT: {data[3]}. In row:")
    return flat(request_pool_id=rp_id, floor=data[0], total_area=data[1], kitchen_area=data[2],
                have_balcony=have_balcony, minutes_metro_walk=data[4],
                condition_id=condition.query.filter_by(name=data[5].lower()).first().id)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


usecols = ['Местоположение', 'Количество комнат', 'Сегмент (Новостройка, современное жилье, старый жилой фонд)',
           'Этажность дома', 'Материал стен (Кипич, панель, монолит)', 'Этаж расположения', 'Площадь квартиры, кв.м',
           'Площадь кухни, кв.м', 'Наличие балкона/лоджии', 'Удаленность от станции метро, мин. пешком',
           'Состояние (без отделки, муниципальный ремонт, с современная отделка)']


@blueprint.route('/calculate', methods=['GET', 'POST'])
def calculate():
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
                    col += 5
                    rp = request_pool(user_id=1, location=reqpl_data[0],
                                      segment_id=segment.query.filter_by(name=reqpl_data[2].lower()).first().id,
                                      floor_quantity=reqpl_data[3],
                                      wall_material_id=wall_material.query.filter_by(name=reqpl_data[4].lower()).first().id,
                                      room_quantity=reqpl_data[1])
                    db.session.add(rp)
                    db.session.flush()
                    first = False
                data = row[col:col + 6]
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

            return redirect(url_for('excel_check.calculate'))
        return "Not an allowed extension"  # TODO proper return page with an error
    return render_template('excel_import.html')
