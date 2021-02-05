from django.contrib import admin

# Register your models here.
import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, ModelFormAdminView, UpdateAdminView
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from django.conf import settings
from xadmin import views
from .models import VerifyCode


class XadminUEditorWidget(UEditorWidget):
    def __init__(self, **kwargs):
        self.ueditor_options = kwargs
        self.Media.js = None
        super(XadminUEditorWidget,self).__init__(kwargs)


class UeditorPlugin(BaseAdminPlugin):

    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'ueditor':
            if isinstance(db_field, UEditorField):
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.ueditor_settings)
                param.update(widget.attrs)
                return {'widget':XadminUEditorWidget(**param)}
        return attrs

    def block_extrahead(self, context, nodes):
        js  = '<script type="text/javascript" src="%s"></script>' %(settings.STATIC_URL + "ueditor/ueditor.config.js")
        js += '<script type="text/javascript" src="%s"></script>' %(settings.STATIC_URL + "ueditor/ueditor.all.min.js")
        nodes.append(js)


class BaseSetting(object):
    # 添加主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 全局配置，后台管理标题和页脚
    site_title = "阿钰Shop"
    # site_footer = "http://www.cnblogs.com/derek1184405959/"
    # 菜单收缩
    menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]
xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)
xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)
xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)