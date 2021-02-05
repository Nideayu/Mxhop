from .models import Goods, GoodsCategory, GoodsImage, GoodsCategoryBrand, Banner, HotSearchWords
from .models import IndexAd
# Register your models here.

import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, ModelFormAdminView, UpdateAdminView
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from django.conf import settings


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


xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)
xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)


class GoodsAdmin(object):
    # 显示的列
    list_display = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                    "shop_price", "goods_brief", "goods_desc", "is_new", "is_hot", "add_time"]
    # 可以搜索的字段
    search_fields = ['name', ]
    # 列表页可以直接编辑的
    list_editable = ["is_hot", ]
    # 过滤器
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                   "shop_price", "is_new", "is_hot", "add_time", "category__name"]
    # 富文本编辑器
    style_fields = {"goods_desc": "ueditor"}

    # 在添加商品的时候可以添加商品图片
    class GoodsImagesInline(object):
        model = GoodsImage
        exclude = ["add_time"]
        extra = 1
        style = 'tab'

    inlines = [GoodsImagesInline]


class GoodsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


class GoodsBrandAdmin(object):
    list_display = ["category", "image", "name", "desc"]

    def get_context(self):
        context = super(GoodsBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
        return context


class BannerGoodsAdmin(object):
    list_display = ["goods", "image", "index"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


class IndexAdAdmin(object):
    list_display = ["category", "goods"]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(Banner, BannerGoodsAdmin)
xadmin.site.register(GoodsCategoryBrand, GoodsBrandAdmin)

xadmin.site.register(HotSearchWords, HotSearchAdmin)
xadmin.site.register(IndexAd, IndexAdAdmin)