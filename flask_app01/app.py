import os.path

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

from form.userForms import UserForm
from form.profileForm import ProfileForm

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(30), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    @staticmethod
    def get_by_id(user_id):
        try:
            user = User.query.get(user_id)
            return user
        except Exception, e:
            return None


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    bday = db.Column(db.String(30), nullable=True)
    sex = db.Column(db.String(5), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    zip_code = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.Integer, nullable=True)

    @staticmethod
    def get_by_id(user_id):
        try:
            profile = Profile.query.get(user_id)
            return profile
        except Exception, e:
            return None

    @staticmethod
    def get_by_user_id(user_id):
        try:
            profile = Profile.query.filter_by(user_id=user_id).first()
            return profile
        except Exception, e:
            return None


class Contact(db.Model):
    owner_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def create(owner_id, user_id):
        contact = Contact(owner_id=owner_id,
                          user_id=user_id)
        db.session.add(contact)
        db.session.commit()

    @staticmethod
    def get(owner_id):
        contacts = Contact.query.filter_by(owner_id=owner_id)
        return contacts


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return """
            <a href='http://localhost:5000/user'>user</a><br>
            <a href='http://localhost:5000/user/add'>add user</a><br>
            """



@app.route('/user', methods=['GET'])
def user_get():
    users = User.query.all()
    return render_template('user.html', users=users)



@app.route('/user/add', methods=['GET', 'POST'])
def user_add():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data,
                    password=form.password.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/user')
    # print form.errors
    return render_template('user_add.html', form=form)


@app.route('/user/<user_id>/delete', methods=['GET'])
def user_del(user_id):
    user = User.get_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect('/user')
    return render_template('error.html', msg_eror="not id {}".format(user_id))



@app.route('/user/<user_id>', methods=['GET','POST'])
def user_update(user_id):
    user = User.get_by_id(user_id)
    if user:
        profile = Profile.get_by_user_id(user.id)
        form = UserForm(request.form)
        if request.method == 'GET':
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.password.data = user.password
            form.email.data = user.email
        if request.method == 'POST' and form.validate():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.password = form.password.data
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()
        return render_template('user_info.html', user=user, profile=profile, form=form)
    return render_template('error.html', msg_eror="not id {}".format(user_id))

@app.route('/user/<user_id>/profile/update', methods=['GET','POST'])
def profile_update(user_id):
    user = User.get_by_id(user_id)
    profile = Profile.get_by_user_id(user_id)
    if user:
        if profile:
            form = ProfileForm(request.form)
            if request.method == 'GET':
                form.bday.data = profile.bday
                form.sex.data = profile.sex
                form.city.data = profile.city
                form.zip_code.data = profile.zip_code
                form.phone.data = profile.phone
            if request.method == 'POST' and form.validate():
                profile.bday = form.bday.data
                profile.sex = form.sex.data
                profile.city = form.city.data
                profile.zip_code = form.zip_code.data
                profile.phone = form.phone.data
                db.session.add(user)
                db.session.commit()
            return render_template('profile_info.html', user=user, profile=profile, form=form)
        return render_template('error.html', msg_eror="not profile for update for id {}".format(user_id))
    return render_template('error.html', msg_eror="not id {}".format(user_id))

@app.route('/user/<user_id>/delete', methods=['GET'])
def user_delete(user_id):
    user = User.get_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect('/user')
    return render_template('error.html', msg_eror="not id {}".format(user_id))


@app.route('/user/<user_id>/add/profile', methods=['GET','POST'])
def profile_post_get(user_id):
    form = ProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        profile = Profile(user_id=user_id,
                          bday=form.bday.data,
                          sex=form.sex.data,
                          city=form.city.data,
                          zip_code=form.zip_code.data,
                          phone=form.phone.data)
        db.session.add(profile)
        db.session.commit()
        _url = '/user/' + str(user_id)
        return redirect(_url)
    return render_template('profile_add.html', form=form)

@app.route('/user/<user_id>/profile', methods=['GET'])
def profile(user_id):
    user = User.get_by_id(user_id)
    if user:
        profile = Profile.get_by_user_id(user.id)
        return render_template('profile.html', user=user, profile=profile)
    return render_template('error.html', msg_eror="not id {}".format(user_id))


@app.route('/user/<owner_id>/contact', methods=['GET'])
def contact(owner_id):
    add_user_id = request.args.get("user_id")
    print "add_user_id", add_user_id
    if add_user_id:
        add = Contact.query.filter_by(owner_id=owner_id, user_id=add_user_id).all()
        print "add:", add
        if not add:
            Contact.create(owner_id, add_user_id)

    contacts = Contact.get(owner_id=owner_id)
    users = User.query.all()

    new_users = []
    for user in users:
        for contact in contacts:
            if user.id == contact.user_id:
                break
        else:
            new_users.append(user)
    return render_template("contact_list.html", contacts=contacts, users=new_users, owner_id=owner_id)


@app.route('/user/<owner_id>/delete/contact', methods=['GET'])
def contact_delete(owner_id):
    user_id = request.args.get("user_id")
    owner_id = int(owner_id)
    if user_id:
        user_id = int(user_id)
        del_contact = Contact.query.filter_by(owner_id=owner_id, user_id=user_id).first()
        db.session.delete(del_contact)
        db.session.commit()
        _url = '/user/' + str(owner_id) + '/contact'
        return redirect(_url)
    return render_template('error.html', msg_eror="not id {}".format(user_id))


@app.route('/user/<user_id>/info', methods=['GET'])
def users_info_one(user_id):
    u = User.query.all()
    p = Profile.get_by_user_id(user_id)
    return render_template('users_info_one.html', users=u, profile=p)


if __name__ == "__main__":
    db.create_all()
    app.run()