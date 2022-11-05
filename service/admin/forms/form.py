from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     TextAreaField, SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from service.database.models import user


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['ru']


def length_check(form, field):
    if len(field.data) > 80:
        raise ValidationError('Field must be less than 80 characters')


class LoginForm(MyBaseForm):
    username = StringField('Логин', validators=[DataRequired(), length_check])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    def validate_email(self, email):
        user_check = user.query.filter_by(email=email.data).first()
        if user_check is None:
            raise ValidationError('Данный E-mail не существует!')


class RegistrationForm(MyBaseForm):
    username = StringField('Логин', validators=[DataRequired(), length_check])
    first_name = StringField('Имя', validators=[DataRequired(), length_check])
    last_name = StringField('Фамилия', validators=[DataRequired(), length_check])
    email = StringField('E-mail', validators=[Optional(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    # def validate_email(self, email):
    #     user_check = user.query.filter_by(email=email.data).first()
    #     if user_check is not None:
    #         raise ValidationError('Данный E-mail уже занят!')
