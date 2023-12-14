# 필요한 패키지 불러오기
from flask import Flask, render_template, url_for, request, redirect, flash
from email_validator import validate_email, EmailNotValidError
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_mail import Mail, Message

# flask 클래스를 인스턴스화함
app = Flask(__name__)

# 세션 정보 보안을 위해 시크릿 키 설정
app.config['SECRET_KEY'] = 'qwer1234%'

# 로그 레벨을 디버그로 설정
app.logger.setLevel(logging.DEBUG)

# 로그 출력하도록 설정
# app.logger.critical('fatal error')
# app.logger.error('error')
# app.logger.warning('warning')
# app.logger.info('info')
# app.logger.debug('debug')

# 리다이렉트가 중단하지 않도록 설정
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Mail 클래스의 config를 추가
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# flask-mail 확장을 앱에 등록
mail = Mail(app)

# DebugToolbarExtension에 애플리케이션 설정
toolbar = DebugToolbarExtension(app)

# URL과 실행할 함수 매핑
# 127.0.0.1:5000:/
@app.route('/')
def index():
    return 'Hello, Flaskbook!'

# endpoint : URI와 연결된 함수명 또는 함수에 붙인 이름
@app.route('/hello/<name>', methods=['GET', 'POST'], endpoint='hello-endpoint')
def show_name(name):
    return render_template('index.html', name=name)

@app.route('/light_check/<command>', methods=['GET', 'POST'])
def light_check(command):
    return render_template('light_check.html', command=command)

@app.route('/contact')
def contact():
    return render_template('contact.html')

# 이메일을 보내는 함수 생성
def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

@app.route('/contact/complete', methods=['GET', 'POST'])
def contact_complete():
    if request.method=='POST':
        # form 속성을 사용해서 폼의 값 취득
        username = request.form['username']
        email = request.form['email']
        description = request.form['description']

        # 입력 체크하기
        is_valid = True
        
        if not username:
            flash('사용자명은 필수입니다')
            is_valid = False

        if not email:
            flash('메일 주소는 필수입니다')
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError as e:
            flash('메일 주소의 형식으로 입력해 주세요')
            flash(str(e))
            is_valid=False

        if not description:
            flash('문의 내용은 필수입니다')
            is_valid = False
        
        if not is_valid:
            return redirect(url_for('contact'))

        # 이메일 보내기
        send_email(email, '문의 감사합니다.', 'contact_mail',
                   username=username,
                   description=description)

        # contact 엔드포인트로 리다이렉트
        flash('문의해 주셔서 감사합니다.')
        return redirect(url_for('contact_complete'))
    
    return render_template('contact_complete.html')

# url_for : URL 확인하기
with app.test_request_context():
    # /
    print(url_for('index'))
    # hello/SHY?page=1
    print(url_for('hello-endpoint', name='SHY', page='1'))
    print(url_for('hello-endpoint', name=''))

with app.test_request_context('/users?updated=true'):
    print(request.args.get('updated'))