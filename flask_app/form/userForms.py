from wtforms import Form, StringField, IntegerField, validators, PasswordField


class UserForm(Form):
    username = StringField('Username', [validators.Regexp(r'^[\w._@+-]+$'), validators.Length(min=2 ,max=50)])
    firstname = StringField('First name', [validators.Length(min=2, max=30)])
    lastname = StringField('Last name', [validators.Length(min=2, max=30)])
    email = StringField('Email', [validators.Email()])
    password = PasswordField('password', [validators.Length(min=2, max=50)])
    age = IntegerField('Age')