from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,HiddenField, IntegerField

from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    nomeutilizador = StringField('nomeUtilizador',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    nomeutilizador = StringField('nomeUtilizador',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Registrar')

class ItemForm(FlaskForm):
    artigoId = HiddenField(validators=[DataRequired()])
    quantidade = HiddenField(validators=[DataRequired()])
