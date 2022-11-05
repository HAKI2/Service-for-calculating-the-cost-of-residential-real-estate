from flask import Blueprint
blueprint = Blueprint('admin_base', __name__,
                      url_prefix='/',
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/admin_base/static/')

from service.admin import views