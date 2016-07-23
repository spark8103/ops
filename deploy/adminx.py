# -*- coding: utf-8 -*-
import xadmin
from xadmin import views
from models import Deploy
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction

from xadmin.views.base import CommAdminView, filter_hook
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _
#from django.shortcuts import render
#from django.utils.encoding import force_unicode, smart_unicode
#from django import forms

import pprint
import os


class DeployAdmin(object):
    list_display = ('name', 'deploy_time', 'version', 'disconf', 'lts', 'mq', 'description')
    list_editable = ('deploy_time', 'version', 'description')
    list_display_links = ('name',)
    show_detail_fields = ("description")
    show_all_rel_details = ("xxxxx")
    relfield_style = 'fk-ajax'
    wizard_form_list = [
        ('First\'s Form', ('name', 'deploy_time', 'version', 'description')),
        ('Second Form', ('db', 'disconf', 'lts', 'mq')),
#        ('Thread Form', ('customer_id',))
    ]

    search_fields = ['name']
    relfield_style = 'fk-ajax'
    reversion_enable = True

#    actions = [BatchChangeAction, ]
#    batch_fields = ('contact', 'create_time')

xadmin.sites.site.register(Deploy, DeployAdmin)


class Ansible(CommAdminView):
    #verbose_name = 'ansible'
    title = _(u"ansible")
    icon = None

    def get_page_id(self):
        return self.request.path

    def get_portal_key(self):
        return "dashboard:%s:pos" % self.get_page_id()

    @filter_hook
    def get_title(self):
        return self.title

    @filter_hook
    def get_context(self):
        new_context = {
            'title': self.get_title(),
            'icon': self.icon,
            'portal_key': self.get_portal_key(),
            'content': "aaa",
            'breadcrumbs': self.get_breadcrumb(),
            #'columns': [('col-sm-%d' % int(12 / len(self.widgets)), ws) for ws in self.widgets],
            #'has_add_widget_permission': self.has_model_perm(UserWidget, 'add') and self.widget_customiz,
            #'add_widget_url': self.get_admin_url('%s_%s_add' % (UserWidget._meta.app_label, UserWidget._meta.model_name)) +
            #"?user=%s&page_id=%s&_redirect=%s" % (self.user.id, self.get_page_id(), urlquote(self.request.get_full_path()))
        }
        context = super(Ansible, self).get_context()
        context.update(new_context)
        print context
        return context

    @filter_hook
    def get_breadcrumb(self):
        bcs = super(Ansible, self).get_breadcrumb()
        item = {'title': self.get_title()}
        bcs.append(item)
        return bcs

    @never_cache
    def get(self, request, *args, **kwargs):
        return self.template_response('ansible.html', self.get_context())

xadmin.sites.site.register_view(r'^ansible/$', Ansible, name='ansible')
