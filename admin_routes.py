from flask import render_template, request, session, redirect, url_for

ADMIN_USERNAME = "Caleb"
ADMIN_PASSWORD = "hi"

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['username'] = username
            return redirect(url_for('admin_dashboard_route'))  # Changed this line
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    return render_template('login.html')

def admin_dashboard():
    if 'username' in session and session['username'] == ADMIN_USERNAME:
        return render_template('admin_dashboard.html', username=session['username'])
    else:
        return redirect(url_for('admin_login'))

def logout():
    session.clear()
    return redirect(url_for('admin_login'))

# Other admin-related functions or routes can be defined here
