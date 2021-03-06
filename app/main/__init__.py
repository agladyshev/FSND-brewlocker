from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors, filters
from ..models import Permission


@main.app_context_processor
def inject_permissions():
	# add permission to templates
    return dict(Permission=Permission)
