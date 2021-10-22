# -*- coding: utf-8 -*-

import odoo
import odoo.modules.registry
from odoo.tools.translate import _
from odoo.exceptions import AccessError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo import http
from odoo.http import request

import os
import logging

_logger = logging.getLogger(__name__)

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
db_monodb = http.db_monodb


class AnitaHome(odoo.addons.web.controllers.main.Home):
    '''
    inhere home to extend web.login style
    '''

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        '''
        rewrtie the login go support login style
        :param redirect:
        :param kw:
        :return:
        '''
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
                request.params['login_success'] = True
                return request.redirect(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        # add extra info to login page
        ir_config = request.env['ir.config_parameter'].sudo()
        login_style = ir_config.get_param(
            key='anita_theme_base.login_style', default='login_style1')
        login_template = 'anita_theme_base.{login_style}'.format(login_style=login_style)
        values['title'] = ir_config.get_param(
            "anita_theme_setting.window_default_title", "Anita Odoo")
        values['powered_by'] = ir_config.get_param("powered_by", "Anita Odoo")

        response = request.render(login_template, values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
