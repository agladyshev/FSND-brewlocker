from flask import jsonify, request, url_for, current_app
from .. import db
from ..models import Item
from . import api


@api.route('/items/')
def get_items():
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.paginate(
        page, per_page=current_app.config['BREWLOCKER_POSTS_PER_PAGE'],
        error_out=False)
    items = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'items': [item.to_json() for item in items],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/item/<int:id>')
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_json())
