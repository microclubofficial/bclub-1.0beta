from flask import request
from forums.common.views import IsAuthMethodView as MethodView
from flask_babel import gettext as _
from forums.func import get_json

class PasswordView(MethodView):
    def post(self):
        user = request.user
        old_password = request.json.get('OldPassword')
        if not user.check_password(old_password):
            msg = _('Original password error')
            return get_json(0, msg, {})
        msg = _('success')
        return get_json(1, msg, {})

class EmailView(MethodView):
    def get(self):
        user = request.user
        email = user.email
        if not email:
            msg = _('Email does not exist')
            return get_json(0, msg, {})
        return get_json(1, 'success', email)    