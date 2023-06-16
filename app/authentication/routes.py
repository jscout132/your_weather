from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from forms import CreateUser, UserLogin
from models import sqla, check_password_hash, User

auth = Blueprint('auth', __name__, template_folder='auth_pages')

@auth.route('/sign_up', methods = ['GET','POST'])
def sign_up():
    form = CreateUser()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user_city = form.user_city.data
            f_name = form.f_name.data
            l_name = form.l_name.data

            user = User(email = email, password = password, 
                        user_city = user_city, f_name = f_name, l_name = l_name)
            
            sqla.session.add(user)
            sqla.session.commit()

            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data, please check your form')
    
    return render_template('sign_up.html', form=form)

@auth.route('/sign_in', methods = ['GET', 'POST'])
def sign_in():
    form = UserLogin()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print(f'{email} logged in now')
                return redirect(url_for('site.profile'))
            else:
                return redirect(url_for('auth.sign_in', form = form))
    except:
        raise Exception('Invalid form data, please check your information')
    
    return render_template('sign_in.html', form = form)

@auth.route('/sign_out')
def sign_out():
    logout_user()
    return redirect(url_for('site.home'))