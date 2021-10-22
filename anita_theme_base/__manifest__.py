# -*- coding: utf-8 -*-
{
    'name': "anita_theme_base",

    'summary': """
        base for anita odoo themes, it support free login for odoo
    """,

    'description': """
        Odoo Login, 
        odoo login page, 
        odoo login theme
        Login, 
        Anita Theme Base,
        Anita Theme,
        Awesome Theme
    """,

    'author': "Anita Odoo",

    'website': "https://www.anitaodoo.com",
    'live_test_url': 'https://awesometheme15.anitaodoo.com/',

    'license': 'OPL-1',
    'images': ['static/description/screen_shot.png', 'static/description/banner.png'],
    'support': 'codercrax@gmail.com',
    'maintainer': 'Anita Odoo',
    'category': 'Theme/Backend',
    'version': '15.0.0.3',

    'installable': True,
    'application': True,
    'auto_install': False,

    'depends': ['base', 'web'],
    'data': [
        "views/login_style1.xml",
        "views/login_style2.xml",
        "views/login_style3.xml",
        "views/login_style4.xml",
        "views/anita_web.xml"
    ],

    'assets': {
        'web.assets_backend': [
            'anita_theme_base/static/css/anita_vars.scss',
            'anita_theme_base/static/css/anita_mixin.scss',
            'anita_theme_base/static/css/anita_list_view.scss',
            'anita_theme_base/static/css/anita_custom_control.scss',
            'anita_theme_base/static/css/anita_form_view.scss',
            'anita_theme_base/static/js/anita_form_controller.js',
        ]
    }
}
