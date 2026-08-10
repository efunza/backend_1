@@
 router.register('maritime-courses', MaritimeCourseViewSet, basename='maritime-course')
 router.register('maritime-enrollments', MaritimeEnrollmentViewSet, basename='maritime-enrollment')
+router.register('maritime-materials', MaritimeMaterialViewSet, basename='maritime-material')
+router.register('maritime-sessions', MaritimeSessionViewSet, basename='maritime-session')
@@
 from django.urls import path as _path, include as _include
 urlpatterns += [_path("", _include("api.elab_ai_urls"))]
+
+# Expose store_router under /store/
+urlpatterns += [path('store/', include(store_router.urls))]
