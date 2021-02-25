from django.urls import path, include, re_path
from django.views.generic import TemplateView

import xadmin
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token

from Mxhop.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from goods.view_base import GoodsListViewSet, CategoryViewSet, BannerViewset, IndexCategoryViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from trade.views import ShoppingCartViewset, OrderViewset, AlipayView
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from users.views import SmsCodeViewset, UserViewset

router = DefaultRouter()

# 首页系列商品展示url
router.register(r'indexgoods', IndexCategoryViewset, basename="indexgoods")
# 配置goods的url
router.register(r'goods', GoodsListViewSet)
# 配置Category的url
router.register(r'categorys', CategoryViewSet)
# 配置用户收藏的url
router.register(r'userfavs', UserFavViewset, basename="userfavs")
# 配置codes的url
router.register(r'code', SmsCodeViewset,basename='code')
# 配置用户注册url
router.register(r'users', UserViewset, basename="users")
# 配置用户留言的url
router.register(r'messages', LeavingMessageViewset, basename="messages")
# 配置收货地址
router.register(r'address', AddressViewset, basename="address")
# 配置购物车的url
router.register(r'shopcarts', ShoppingCartViewset, basename="shopcarts")
# 配置订单的url
router.register(r'orders', OrderViewset, basename="orders")
# 首页轮播图
router.register(r'banners', BannerViewset, basename="banners")
urlpatterns = [
    path('xadmin/', xadmin.site.urls),

    path('api-auth/',include('rest_framework.urls')),
    path('ueditor/',include('DjangoUeditor.urls' )),
    # 文件
    path('media/<path:path>',serve,{'document_root': MEDIA_ROOT}),
    # drf文档，title自定义
    path('docs',include_docs_urls(title='阿钰Shop')),
    # 商品列表页
    re_path('^', include(router.urls)),
    # token
    path('api-token-auth/', views.obtain_auth_token),
    # jwt的token认证接口
    path('login/', obtain_jwt_token),
    path('alipay/return/', AlipayView.as_view()),
    # 首页
    path('index/', TemplateView.as_view(template_name='index.html'), name='index')
]

