import os
from flask import (render_template, redirect, request, url_for, current_app, flash, make_response)
from service.excel_check import blueprint
from werkzeug.utils import secure_filename
import openpyxl

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

usecols = ['Обязательные при подбое аналогов', 'Корректируемые в соответствии со справочниками']

@blueprint.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # dataframe = pd.read_excel(file, usecols=usecols)[12:]
            # print(dataframe)
            dataframe = openpyxl.open(file)
            sheet = dataframe.active
            for i in sheet:
                print(i)
            return redirect(url_for('excel_check.calculate',
                                    filename=filename))
        return "Not an allowed extension"  # TODO proper return page with an error
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        '''
