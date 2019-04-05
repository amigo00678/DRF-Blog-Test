from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from app import views
from rest_framework_jwt.views import obtain_jwt_token, \
    refresh_jwt_token, verify_jwt_token
from rest_framework_swagger.views import get_swagger_view


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.BlogPostViewSet)

schema_view = get_swagger_view(title='Pastebin API')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', schema_view),
    path('accounts/', include('django.contrib.auth.urls'))
]
