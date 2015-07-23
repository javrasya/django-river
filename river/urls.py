from django.conf.urls import patterns, include, url

from django.contrib import admin
from esefpy.web.rest.router import HybridRouter

from apps.riverio.views import DataFormsViewSet, ObjectRegistrationView, TransitionProcessView, ObjectCountWaitingForApprovalView, ObjectsWaitingForApprovalViewSet, IsUserAuthorizedView
from apps.riverio.views.state import StateViewSet

__author__ = 'ahmetdal'

admin.autodiscover()
router = HybridRouter()

router.add_api_view("api-view-data-forms", url(r'^DataForms/$', DataFormsViewSet.as_view(), name='DataForm-name'))
router.register(r'State', StateViewSet, base_name='state')
# router.register(r'Object', ObjectRegistrationView, base_name='object')

objects_waiting_for_approval_list = ObjectsWaitingForApprovalViewSet.as_view({
    'get': 'list',
})

urlpatterns = patterns('',
                       # url(r'', include('esefpy.web.nav.urls')),
                       # url(r'', include('esefpy.web.esefauth.urls')),
                       # url(r'', include('esefpy.web.content.urls')),
                       # url(r'', include('esefpy.audit.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/', include(router.urls)),
                       )

urlpatterns += patterns(
    'apps.riverio.views',
    url(r'^register_object/$', ObjectRegistrationView.as_view(), name='register_object'),
    url(r'^processes_transition/$', TransitionProcessView.as_view(), name='process_transition'),
    url(r'^object_count_waiting_for_approval/(?P<content_type_id>[a-zA-Z0-9]+)/(?P<field_id>[a-zA-Z0-9]+)/(?P<user_id>[a-zA-Z0-9_]+)/$', ObjectCountWaitingForApprovalView.as_view(),
        name='object_count_waiting_for_approval'),
    url(r'^objects_waiting_for_approval/(?P<content_type_id>[a-zA-Z0-9]+)/(?P<field_id>[a-zA-Z0-9]+)/(?P<user_id>[a-zA-Z0-9_]+)/$', objects_waiting_for_approval_list,
        name='objects_waiting_for_approval_list'),
    url(r'^is_user_authorized/(?P<content_type_id>[a-zA-Z0-9]+)/(?P<field_id>[a-zA-Z0-9]+)/(?P<user_id>[a-zA-Z0-9_]+)/$', IsUserAuthorizedView.as_view(), name='is_user_authorized_view'),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
