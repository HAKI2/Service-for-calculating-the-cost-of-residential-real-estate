from flask import Blueprint
blueprint = Blueprint('excel_import', __name__,
                      url_prefix='/pool',
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/excel_import/static/')

from service.excel_import import views