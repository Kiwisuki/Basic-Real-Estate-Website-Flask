from flask import Flask, redirect, url_for, render_template, request, session, flash
import pymysql
import string
import random
from datetime import datetime, timedelta

from sympy import re
from queries import *

app = Flask(__name__)
app.secret_key = 'Test_flask'

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/register', methods=["POST", 'GET'])
def register():
    if request.method == 'POST':
        if insert(dict(request.form), 'users'):
            flash('Registration success')
        else:
            flash('Registration failed')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/login', methods=["POST", 'GET'])
def login():
    if request.method == 'POST':
        form = {}
        form['email'] = request.form['email']
        form['password'] = request.form['password']
        if auth_password(form['email'], form["password"]):
            session['user'] = form['email']
            eml = session['user']
            flash(f'Welcome {eml}')
            return redirect(url_for('home'))
        flash('Incorrect password')
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    flash('Logged out successfully')
    return redirect(url_for('login'))

@app.route("/my-ads")
def my_ads():
    return render_template("my_ads.html", rows=user_ads(session['user']))

@app.route("/ad-statistics")
def ad_statistics():
    return render_template("statistics.html")

@app.route("/create-ad")
def choose_object():
    return render_template("create_ad.html")

@app.route("/create-ad/flat",  methods=["POST", 'GET'])
def create_ad_flat():
    if request.method == 'POST':
        create_ad_request(request, 'flat')
    return render_template("flat_form.html")

@app.route("/create-ad/house", methods=["POST", 'GET'])
def create_ad_house():
    if request.method == 'POST':
        create_ad_request(request, 'house')
    return render_template("house_form.html")

@app.route("/create-ad/premise", methods=["POST", 'GET'])
def create_ad_premises():
    if request.method == 'POST':
        create_ad_request(request, 'premise')
    return render_template("premise_form.html")

@app.route("/create-ad/garage", methods=["POST", 'GET'])
def create_ad_garage():
    if request.method == 'POST':
        create_ad_request(request, 'garage')
    return render_template("garage_form.html")

@app.route("/create-ad/plot", methods=["POST", 'GET'])
def create_ad_plot():
    if request.method == 'POST':
        create_ad_request(request, 'plot')

    return render_template("plot_form.html")

@app.route("/browse-ads")
def browse_ads():
    return render_template("browse_ads.html", rows=get_ads_browse())

@app.route("/ads/<ad_id>", methods=["POST", 'GET'])
def ad(ad_id):
    seen_ad(ad_id, session['user'])
    return render_template("ad.html", rows=get_ad_object(ad_id))

@app.route("/ads/edit/<ad_id>", methods=["POST", 'GET'])
def edit_ad(ad_id):
    if request.method == 'POST':
        update_ad(ad_id, dict(request.form))
        return redirect('/my-ads')
    return render_template("edit_ad.html", ad=get_ad(ad_id))

@app.route("/ads/delete/<ad_id>")
def delete_ad_request(ad_id):
        delete_ad(ad_id)
        return redirect('/my-ads')

@app.route("/ads/<ad_id>/save", methods=["POST", 'GET'])
def save_ad(ad_id):
    try:
        seen_ad(ad_id, session['user'], table='saved_ads', g_id=session['user']+'_'+ad_id)
    except:
        flash('You have already saved this ad')
    return redirect(url_for('ad', ad_id=ad_id))

@app.route("/history")
def history():
    return render_template("history.html", rows=get_seen_ads(session['user']))

@app.route("/delete-view/<view>")
def delete_view(view):
    delete_seen_ad(view)
    return redirect('/history')

@app.route("/saved-ads")
def saved():
    return render_template("saved_ads.html", rows=get_saved_ads(session['user']))

@app.route("/delete-save/<view>")
def delete_saved(view):
    delete_saved_ad(view)
    return redirect('/saved-ads')

@app.route('/edit-profile', methods=["POST", 'GET'])
def edit_profile():
    if request.method == 'POST':
        if auth_password(session['user'], request.form['Old_password']):
            form = dict(request.form)
            del form['Old_password']
            if update_user(session['user'], form):
                flash('Edit success')
            else:
                flash('Edit failed')
        else:
            flash('Incorrect password')
        return redirect(url_for('home'))
    else:
        return render_template('edit_profile.html')


@app.route('/stats', methods=["POST", 'GET'])
def stats():
    if request.method == 'POST':
        form = dict(request.form)
        return render_template('stats.html', rows=get_ads_views(form['Ad_type'])[0], sum_=get_ads_views(form['Ad_type'])[1], tipo=form['Ad_type'])

    return render_template('statistics.html')

if __name__ == "__main__":
    app.run(debug=True)