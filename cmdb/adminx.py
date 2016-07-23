# -*- coding: utf-8 -*-
import xadmin
from xadmin import views
from models import IDC, Host, MaintainLog, HostGroup, AccessRecord
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
from deploy.models import Deploy

class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "Test Widget", "content": "<h3> Welcome to ops system! </h3><p>Join Online Group: <br/>QQ xxxxxxx</p>"},
            {"type": "list", "model": "cmdb.host", 'params': {'o':'-create_time'}},
        ],
        [
            {"type": "qbutton", "title": "Quick Start", "btns": [{'model': Host}, {'model':IDC}, {'title': "baidu", 'url': "http://www.baidu.com"}]},
            {"type": "addform", "model": MaintainLog},
        ]
    ]
xadmin.sites.site.register(views.website.IndexView, MainDashboard)


class BaseSetting(object):
    enable_themes = False
    use_bootswatch = False
xadmin.sites.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    site_title = 'hdfax运维管理平台'
    site_footer  = '2016恒大金服'
    global_search_models = [Host]
    global_models_icon = {
        Host: 'fa fa-laptop', IDC: 'fa fa-cloud', MaintainLog: 'fa fa-wrench'
    }
    def get_site_menu(self):
        return (
            {'title': '资产管理', 'perm': self.get_model_perm(Host, 'change'), 'menus':(
                {'title':'主机管理', 'icon': 'fa fa-laptop', 'url': self.get_model_url(Host, 'changelist')},
                {'title': '主机组管理',  'url': self.get_model_url(HostGroup, 'changelist')},
                {'title':'IDC管理', 'icon': 'fa fa-cloud', 'url': self.get_model_url(IDC, 'changelist')},
                {'title':'维修日志', 'icon': 'fa fa-wrench', 'url': self.get_model_url(MaintainLog, 'changelist')},
                {'title':'访问日志','url': self.get_model_url(AccessRecord, 'changelist')},
            )},
            {'title': '部署管理', 'perm': self.get_model_perm(Deploy, 'change'), 'menus':(
                {'title':'线上发布','url': self.get_model_url(Deploy, 'changelist')},
            )},
            {'title': '页面测试', 'perm': '', 'menus':(
                {'title':'ansible','url': "/ansible/"},
            )},
        )
    menu_style = 'default'#'accordion'
xadmin.sites.site.register(views.CommAdminView, GlobalSetting)


class MaintainInline(object):
    model = MaintainLog
    extra = 1
    style = 'accordion'


class IDCAdmin(object):
    list_display = ('name', 'address', 'description', 'create_time')
    list_display_links = ('name',)
    wizard_form_list = [
        ('First\'s Form', ('name', 'address')),
        ('Second Form', ('contact', 'telphone', 'qq', 'customer_id', 'description' )),
    ]

    search_fields = ['name']
    #relfield_style = 'fk-ajax'
    relfield_style = 'fk-select'
    reversion_enable = True

    actions = [BatchChangeAction, ]
    #batch_fields = ('contact', 'create_time')
    batch_fields = ('contact', 'groups')


class HostAdmin(object):
    #def open_web(self, instance):
    #    return "<a href='http://%s' target='_blank'>Open</a>" % instance.ip
    #open_web.short_description = "Acts"
    #open_web.allow_tags = True
    #open_web.is_column = True

    list_display = ('name', 'mip', 'bip', 'vip', 'service_type',
                    'status', 'description')
    list_display_links = ('name',)

    raw_id_fields = ('idc',)
    style_fields = {'system': "radio-inline"}

    search_fields = ['name', 'bip', 'mip', 'vip']
    list_filter = ['idc', 'status', 'core_num', 'hard_disk', 'memory', ('service_type',xadmin.filters.MultiSelectFieldListFilter)]
    
    list_quick_filter = ['service_type',{'field':'idc__name','limit':10}]
#    list_bookmarks = [{'title': "Need Guarantee", 'query': {'status__exact': 2}, 'order': ('-guarantee_date',), 'cols': ('brand', 'guarantee_date', 'service_type')}]

    show_detail_fields = ('idc',)
    list_editable = (
        'name', 'bip', 'mip', 'vip', 'service_type', 'status', 'description')
    save_as = True

    #aggregate_fields = {"guarantee_date": "min"}
    grid_layouts = ('table', 'thumbnails')

    form_layout = (
        Main(
            TabHolder(
                Tab('Comm Fields',
                    Fieldset('主机信息',
                             Row('name', 'system'),
                             Row('bip', 'mip', 'vip'),
                             description=""
                             ),
                    Inline(MaintainLog),
                    ),
                Tab('Extend Fields',
                    Fieldset('扩展信息',
                             Row('idc', 'service_type'),
                             Row('core_num', AppendedText(
                                 'hard_disk', 'G'), AppendedText('memory', "G")),
                             'status'
                             ),
                    ),
            ),
        ),
    )
    inlines = [MaintainInline]
    reversion_enable = True
    
#    data_charts = {
#        "host_service_type_counts": {'title': u"Host service type count", "x-field": "service_type", "y-field": ("service_type",), 
#                              "option": {
#                                         "series": {"bars": {"align": "center", "barWidth": 0.8,'show':True}}, 
#                                         "xaxis": {"aggregate": "count", "mode": "categories"},
#                                         },
#                              },
#    }
    
class HostGroupAdmin(object):
    list_display = ('name', 'description')
    list_display_links = ('name',)

    search_fields = ['name']
#    style_fields = {'hosts': 'checkbox-inline'}


class MaintainLogAdmin(object):
    list_display = (
        'host', 'maintain_type', 'time', 'operator', 'note')
    list_display_links = ('host',)

    list_filter = ['host', 'maintain_type', 'time', 'operator']
    search_fields = ['note']

    form_layout = (
        Col("col2",
            Fieldset('Record data',
                     'time', 'note',
                     css_class='unsort short_label no_title'
                     ),
            span=9, horizontal=True
            ),
        Col("col1",
            Fieldset('Comm data',
                     'host', 'maintain_type'
                     ),
            Fieldset('Maintain details',
                     'operator'
                     ),
            span=3
            )
    )
    reversion_enable = True


class AccessRecordAdmin(object):
    def avg_count(self, instance):
        return int(instance.view_count / instance.user_count)
    avg_count.short_description = "Avg Count"
    avg_count.allow_tags = True
    avg_count.is_column = True

    list_display = ('date', 'user_count', 'view_count', 'avg_count')
    list_display_links = ('date',)

    list_filter = ['date', 'user_count', 'view_count']
    actions = None
    aggregate_fields = {"user_count": "sum", 'view_count': "sum"}

    refresh_times = (3, 5, 10)
    data_charts = {
        "user_count": {'title': u"User Report", "x-field": "date", "y-field": ("user_count", "view_count"), "order": ('date',)},
        "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)},
        "per_month": {'title': u"Monthly Users", "x-field": "_chart_month", "y-field": ("user_count", ), 
                              "option": {
                                         "series": {"bars": {"align": "center", "barWidth": 0.8,'show':True}}, 
                                         "xaxis": {"aggregate": "sum", "mode": "categories"},
                                         },
                            },
    }
    
    def _chart_month(self,obj):
        return obj.date.strftime("%B")


xadmin.sites.site.register(Host, HostAdmin)
xadmin.sites.site.register(HostGroup, HostGroupAdmin)
xadmin.sites.site.register(MaintainLog, MaintainLogAdmin)
xadmin.sites.site.register(IDC, IDCAdmin)
xadmin.sites.site.register(AccessRecord, AccessRecordAdmin)
