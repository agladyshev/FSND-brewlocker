from flask import render_template, session, redirect, url_for, current_app,\
    request
from .. import db
from ..models import User, Item, Permission
from ..email import send_email
from . import main
from .forms import ItemForm
from ..decorators import admin_required, permission_required
from ..filters import timesince_filter
from flask_login import login_required, current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.order_by(Item.timestamp.desc()).paginate(
        page, per_page=current_app.config['BREWLOCKER_POSTS_PER_PAGE'],
        error_out=False)
    items = pagination.items
    return render_template('index.html', items=items, pagination=pagination)


@main.route('/new', methods=['GET', 'POST'])
@login_required
def newItem():
    form = ItemForm()
    if current_user.can(Permission.ADD_ITEMS) and \
            form.validate_on_submit():
        images = request.files.getlist("img")
        item = Item(header=form.header.data,
                    body=form.body.data,
                    phone=form.phone.data,
                    author=current_user._get_current_object())
        db.session.add(item)
        print "item created"
        item.save_img(images)
        return redirect(url_for('.index'))
    return render_template('new_item.html', form=form)


@main.route('/<int:item_id>', methods=['GET'])
def getItem(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', item=item)


@main.route('/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_id):
    return render_template('edit_item.html')


@main.route('/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(item_id):
    return


@main.route('/user/<int:user_id>', methods=['GET'])
@login_required
def getProfile(user_id):
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.filter_by(author_id=user_id).order_by(Item.timestamp.desc()).paginate(
        page, per_page=current_app.config['BREWLOCKER_POSTS_PER_PAGE'],
        error_out=False)
    items = pagination.items
    return render_template('index.html', items=items, pagination=pagination)


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"