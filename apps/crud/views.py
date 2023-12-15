# 필요한 패키지 불러오기
from flask import Blueprint, render_template, redirect, url_for
from apps.app import db
from apps.crud.models import User
from apps.crud.forms import UserForm

# Blueprint로 crud 앱 생성
crud = Blueprint("crud", __name__, template_folder="templates", static_folder="static")

# index 엔드포인트를 작성하고 index.html 반환
@crud.route('/')
def index():
    return render_template('crud/index.html')

# sql 엔드포인트 추가하기
@crud.route('/sql')
def sql():
    db.session.query(User).all()
    return "콘솔 로그를 확인해 주세요"

# "127.0.0.1:5000/crud/users/new"
@crud.route('/users/new', methods=['GET', 'POST'])
def create_user():
    # UserForm 인스턴스화
    form = UserForm()
    # 폼의 값 검증
    if form.validate_on_submit():
        # 사용자 작성
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        # 사용자 추가 및 commit
        db.session.add(user)
        db.session.commit()
        # 사용자의 일람 화면으로 리다이렉트
        return redirect(url_for('crud.users'))
    return render_template('crud/create.html', form=form)

# "127.0.0.1:5000/crud/users"
@crud.route('/users')
def users():
    # 사용자 일람 취득
    users = User.query.all()
    return render_template('crud/index.html', users=users)

# edit_user 엔드포인트 추가하기
@crud.route('users/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    form = UserForm()
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()     
        return redirect(url_for('crud.users'))
    return render_template('crud/edit.html', user=user, form=form)

# delete_user 엔드포인트 추가하기
@crud.route('users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('crud.users'))