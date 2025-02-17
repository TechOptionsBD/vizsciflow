import os
import logging

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from . import auth, cas
from .. import db
from ..email import send_email
from app.objectmodel.common import AccessRights
from ..util import Utility
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, \
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from ..managers.usermgr import usermanager
from ..managers.datamgr import datamanager

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is not None and user.verify_password(form.password.data):
#             login_user(user, form.remember_me.data)
#             return redirect(request.args.get('next') or url_for('main.index'))
#         flash('Invalid username or password.')
#     return render_template('auth/login.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.args.get('ticket'):
        return usask_login(request.args)
    form = LoginForm()
    if form.validate_on_submit():
        user = None
        try:
            user = usermanager.get_by_email(form.email.data)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('auth.login'))

        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data, force=True, fresh=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)

def usask_login(args):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    from app import app
    _, username, _ = cas.validate('{0}/auth/login'.format(app.config['VIZSCIFLOW_LOGIN_WELCOME']), args.get('ticket'))
    if not username:
        flash('Invalid username or password')
        return redirect(url_for('auth.login'))
    
    user = None
    try:
        user = usermanager.get_by_username(username)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('auth.login'))
    
    if not user:
        user = usermanager.create_user(username=username, oid=1)
        allocate_storage(user)
    login_user(user, remember=False)
    next_page = args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('main.index')
    return redirect(next_page)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


def allocate_storage(user):
    datasources = datamanager.get_datasources(active = True)
    for ds in datasources:
        try:
            fs = Utility.create_fs(ds)
            if fs:
                userpath = None
                if ds.type == 'gfs':
                    userpath = 'Libraries/' + user.username
                else:
                    userpath = os.path.join('/' + ds.user, user.username) if ds.user else '/' + user.username
                    
                if not fs.exists(userpath):
                    fs.makedirs(userpath)
                
                # datamanager.add_allocation(user.id, ds.id, userpath, AccessRights.Owner)
                # if ds.public:
                #     datamanager.add_allocation(user.id, ds.id, 'Libraries/' + ds.public if ds.type == 'gfs' else ds.public, AccessRights.Read)
        except Exception as e:
            logging.error(f'Storage allocation on {ds.name} has failed: {str(e)}')
            flash(f'Storage allocation on {ds.name} has failed.')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = usermanager.create_user(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            if user:
                allocate_storage(user)

    #         token = user.generate_confirmation_token()
    #         send_email(user.email, 'Confirm Your Account',
    #                    'auth/email/confirm', user=user, token=token)
    #         flash('A confirmation email has been sent to you by email.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Registration error')
            logging.error(f'Registration error:{str(e)}')
            return render_template('auth/register.html', form=form)

    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_and_update_password(form.old_password.data, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = usermanager.get_by_email(form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = usermanager.get_by_email(form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
