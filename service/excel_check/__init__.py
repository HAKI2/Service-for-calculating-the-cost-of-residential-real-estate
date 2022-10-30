from flask import Blueprint
blueprint = Blueprint('excel_check', __name__,
                      url_prefix='/excel_check',
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/excel_check/static/')

from service.excel_check import views