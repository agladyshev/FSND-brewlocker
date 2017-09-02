from flask import render_template, session, abort, redirect,\
    url_for, current_app, request, flash
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
    return render_template('index.html',
                           items=items, pagination=pagination, page=page)


@main.route('/new', methods=['GET', 'POST'])
@login_required
def newItem():
    form = ItemForm()
    if not current_user.can(Permission.ADD_ITEMS):
        flash('insufficient privileges')
        return redirect(url_for('.index'))
    if form.validate_on_submit():
        item = Item(header=form.header.data,
                    body=form.body.data,
                    phone=form.phone.data,
                    author=current_user._get_current_object())
        db.session.add(item)
        images = request.files.getlist("img")
        if form.img.data:
            item.save_img(images)
        flash('Item added')
        return redirect(url_for('.index'))
    return render_template('new_item.html', form=form)


@main.route('/<int:item_id>', methods=['GET'])
def getItem(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', item=item)


@main.route('/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        abort(403)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        images = request.files.getlist("img")
        if form.img.data:
            item.save_img(images)
        flash("Info updated")
        return redirect(url_for('.index'))
    return render_template('edit_item.html', item=item, form=form)


@main.route('/<int:item_id>/delete', methods=['POST'])
@login_required
def deleteItem(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user == item.author or current_user.can(Permission.MODERATE):
        for image in item.images:
            image.deleteFromServer()
        db.session.delete(item)
        flash('Item deleted')
        return redirect(url_for('.index'))
    else:
        abort(403)


@main.route('/<int:item_id>/delete/<int:image_id>', methods=['POST'])
@login_required
def deleteImage(item_id, image_id):
    item = Item.query.get_or_404(item_id)
    image = item.images.filter_by(id=image_id).first()
    if current_user != image.author:
        abort(403)
    image.deleteFromServer()
    db.session.delete(image)
    return redirect(url_for('.editItem', item_id=item_id))


@main.route('/user/<int:user_id>', methods=['GET'])
@login_required
def getProfile(user_id):
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.filter_by(
        author_id=user_id).order_by(Item.timestamp.desc()).paginate(
        page, per_page=current_app.config['BREWLOCKER_POSTS_PER_PAGE'],
        error_out=False)
    items = pagination.items
    return render_template('index.html', items=items, pagination=pagination)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.order_by(Item.timestamp.desc()).paginate(
        page, per_page=current_app.config['BREWLOCKER_POSTS_PER_PAGE'],
        error_out=False)
    items = pagination.items
    return render_template('moderate.html', items=items,
                           pagination=pagination, page=page)
