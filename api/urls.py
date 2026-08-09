from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import *
from .maritime_views import MaritimeCourseViewSet, MaritimeEnrollmentViewSet

# ============================================================
# MAIN ROUTER
# ============================================================

router = DefaultRouter()
router.register('programs', ProgramViewSet, basename='program')
router.register('enrollments', EnrollmentViewSet, basename='enrollment')
router.register('lessons', LessonViewSet, basename='lesson')
router.register('videos', VideoViewSet, basename='video')
router.register('content', ContentItemViewSet, basename='content')
router.register('assessments', AssessmentViewSet, basename='assessment')
router.register('student-scores', StudentScoreViewSet, basename='student-score')
router.register('student-intelligence/profiles', StudentIntelligenceViewSet, basename='student-intelligence-profile')
router.register('activity-logs', ActivityLogViewSet, basename='activity-log')
router.register('tasks', TaskViewSet, basename='task')
router.register('notes', NoteViewSet, basename='note')
router.register('discussions', DiscussionViewSet, basename='discussion')
router.register('assignments', AssignmentViewSet, basename='assignment')
router.register('grades', GradeViewSet, basename='grade')
router.register('events', EventViewSet, basename='event')
router.register('study-groups', StudyGroupViewSet, basename='study-group')
router.register('career-sessions', CareerSessionViewSet, basename='career-session')
router.register('feedback', FeedbackViewSet, basename='feedback')
router.register('support/contact', SupportRequestViewSet, basename='support-contact')
router.register('books', BookViewSet, basename='book')
router.register('my-books', MyBookViewSet, basename='my-book')
router.register('achievements', AchievementViewSet, basename='achievement')
router.register('notifications', NotificationViewSet, basename='notification')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')
router.register('lab-projects', LabProjectViewSet, basename='lab-project')
router.register('school-os', SchoolOSResourceViewSet, basename='school-os')
router.register('starter-school', StarterSchoolViewSet, basename='starter-school')
router.register('boarding-pro', BoardingProViewSet, basename='boarding-pro')
router.register('smart-boarding-plus', SmartBoardingPlusViewSet, basename='smart-boarding-plus')
router.register('readathon/reports', ReadathonReportViewSet, basename='readathon-report')
router.register('readathon/interventions', InterventionNoteViewSet, basename='readathon-intervention')
# ============================================================
# 🚢 MARITIME ACADEMY ROUTER
# ============================================================
router.register('maritime-courses', MaritimeCourseViewSet, basename='maritime-course')
router.register('maritime-enrollments', MaritimeEnrollmentViewSet, basename='maritime-enrollment')

# ============================================================
# 🛒 STORE ROUTER
# ============================================================

store_router = DefaultRouter()
store_router.register('products', ProductViewSet, basename='product')
store_router.register('categories', CategoryViewSet, basename='category')
store_router.register('orders', OrderViewSet, basename='order')
store_router.register('reviews', ProductReviewViewSet, basename='product-review')
store_router.register('payments', PaymentViewSet, basename='payment')
store_router.register('addresses', AddressViewSet, basename='address')
store_router.register('coupons', CouponViewSet, basename='coupon')

# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [
    # ============================================================
    # FAVICON
    # ============================================================
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    
    # ============================================================
    # API ROOT
    # ============================================================
    path('', api_root, name='api-root'),
    
    # ============================================================
    # HEALTH CHECK
    # ============================================================
    path('health/', health, name='health'),
    
    # ============================================================
    # AUTHENTICATION
    # ============================================================
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
    path('auth/forgot-password/', PasswordResetRequestView.as_view(), name='auth-forgot-password'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='auth-password-reset'),
    path('auth/reset-password/', PasswordResetConfirmView.as_view(), name='auth-reset-password'),
    path('auth/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
    path('auth/privacy-settings/', PrivacySettingsView.as_view(), name='auth-privacy-settings'),
    path('me/', MeView.as_view(), name='me'),
    
    # ============================================================
    # AI CHAT
    # ============================================================
    path('ai/chat/', AIChatView.as_view(), name='ai-chat'),
    
    # ============================================================
    # M-PESA
    # ============================================================
    path('mpesa/initiate/', MpesaInitiateView.as_view(), name='mpesa-initiate'),
    path('mpesa/status/<str:order_number>/', mpesa_status, name='mpesa-status'),
    
    # ============================================================
    # STUDENT INTELLIGENCE
    # ============================================================
    path('student-intelligence/summary/', StudentIntelligenceViewSet.as_view({'get': 'summary'}), name='student-intelligence-summary'),
    path('student-intelligence/', student_intelligence_summary, name='student-intelligence'),
    
    # ============================================================
    # E2IO
    # ============================================================
    path('e2io/maturity/', e2io_maturity, name='e2io-maturity'),
    path('e2io/', e2io_maturity_alias, name='e2io'),
    
    # ============================================================
    # GAME / GAMIFICATION
    # ============================================================
    path('game/profile/', game_profile, name='game-profile'),
    path('game/leaderboard/', game_leaderboard, name='game-leaderboard'),
    
    # ============================================================
    # READATHON
    # ============================================================
    path('readathon/quiz-score/', save_readathon_quiz, name='readathon-quiz-score'),
    
    # ============================================================
    # ANALYTICS
    # ============================================================
    path('analytics/dashboard/overview/', analytics_overview, name='analytics-overview'),
    path('analytics/dashboard/global_impact/', analytics_overview, name='analytics-global-impact'),
    path('analytics/dashboard/school_rankings/', analytics_overview, name='analytics-school-rankings'),
    path('analytics/enrollments/', analytics_overview, name='analytics-enrollments'),
    path('analytics/enrollments/conversion_rate/', analytics_overview, name='analytics-conversion-rate'),
    path('analytics/reports/generate_report/', generic_ok, name='analytics-generate-report'),
    
    # ============================================================
    # ENVIRONMENTAL (placeholders)
    # ============================================================
    path('environmental/summary/', generic_ok, name='environmental-summary'),
    path('environmental/carbon/', generic_ok, name='environmental-carbon'),
    path('environmental/water/', generic_ok, name='environmental-water'),
    path('environmental/trees/', generic_ok, name='environmental-trees'),
    path('environmental/settings/', generic_ok, name='environmental-settings'),
    path('environmental-challenges/', generic_ok, name='environmental-challenges'),
    path('environmental-goals/', generic_ok, name='environmental-goals'),
    path('environmental-impact/', generic_ok, name='environmental-impact'),
    path('environmental/impacts/calculate_impact/', generic_ok, name='environmental-calculate-impact'),
    path('environmental/impacts/daily_summary/', generic_ok, name='environmental-daily-summary'),
    path('environmental/impacts/weekly_summary/', generic_ok, name='environmental-weekly-summary'),
    path('environmental/milestones/', generic_ok, name='environmental-milestones'),
    path('environmental/milestones/progress/', generic_ok, name='environmental-milestones-progress'),
    path('environmental/trees/plant_real_tree/', generic_ok, name='environmental-plant-tree'),
    
    # ============================================================
    # PARTNERS
    # ============================================================
    path('partners/enrollment_programs/', generic_ok, name='partners-enrollment-programs'),
    path('partners/organizations/', generic_ok, name='partners-organizations'),
    path('partners/projects/', generic_ok, name='partners-projects'),
    
    # ============================================================
    # STUDENTS
    # ============================================================
    path('students/create_from_enrollment/', generic_ok, name='students-create-from-enrollment'),
    
    # ============================================================
    # CERTIFICATES
    # ============================================================
    path('certificates/enrollment/generate/', generic_ok, name='certificates-enrollment-generate'),
    path('blockchain/certificates/generate/', generic_ok, name='blockchain-certificates-generate'),
    
    # ============================================================
    # READATHON REPORTS & INSIGHTS
    # ============================================================
    
    # Parent Reports
    path('readathon/parent-reports/history/', parent_reports_history, name='parent-reports-history'),
    path('readathon/parent-reports/save/', parent_reports_save, name='parent-reports-save'),
    path('readathon/parent-reports/email/', parent_reports_email, name='parent-reports-email'),
    
    # Teacher Insights
    path('readathon/teacher-insights/history/', teacher_insights_history, name='teacher-insights-history'),
    path('readathon/teacher-insights/save/', teacher_insights_save, name='teacher-insights-save'),
    path('readathon/teacher-insights/email/', teacher_insights_email, name='teacher-insights-email'),
    
    # Interventions
    path('readathon/interventions/history/', interventions_history, name='interventions-history'),
    path('readathon/interventions/save/', interventions_save, name='interventions-save'),
    
    # ============================================================
    # 🏆 READATHON RANKING & REPORTING
    # ============================================================
    
    path('readathon/leaderboard/', readathon_leaderboard, name='readathon-leaderboard'),
    path('readathon/student-report/<int:user_id>/', student_readathon_report, name='readathon-student-report'),
    path('readathon/school-ranking/', readathon_school_ranking, name='readathon-school-ranking'),
    path('readathon/export-report/', readathon_export_report, name='readathon-export-report'),
    path('readathon/summary-stats/', readathon_summary_stats, name='readathon-summary-stats'),
    
    # ============================================================
    # 📄 PDF REPORT EXPORT (Admin only)
    # ============================================================
    
    path('readathon/export-pdf/<int:user_id>/', readathon_export_pdf, name='readathon-export-pdf-student'),
    path('readathon/export-pdf/', readathon_export_pdf, name='readathon-export-pdf-all'),
    
    # ============================================================
    # 📊 STUDENT SELF-REPORT ENDPOINTS (Students only)
    # ============================================================
    
    path('readathon/my-report/', student_my_report, name='student-my-report'),
    path('readathon/my-pdf/', student_export_my_pdf, name='student-my-pdf'),
    
    # ============================================================
    # 🆕 ADMIN MONITORING ENDPOINTS
    # ============================================================
    
    path('admin/students/progress/', student_progress_dashboard, name='admin-student-progress'),
    path('admin/students/<int:user_id>/track/', track_student, name='admin-track-student'),
    path('admin/students/export-csv/', export_progress_csv, name='admin-export-csv'),
    path('admin/students/activity-feed/', activity_feed, name='admin-activity-feed'),
    path('admin/students/statistics/', reading_statistics, name='admin-reading-statistics'),
    path('admin/students/top-readers/', top_readers, name='admin-top-readers'),
    path('admin/books/popularity/', book_popularity, name='admin-book-popularity'),
    
    # ============================================================
    # 📊 ADMIN DASHBOARD
    # ============================================================
    
    path('admin/dashboard/stats/', admin_dashboard_stats, name='admin-dashboard-stats'),
    
    # ============================================================
    # 🛒 STORE URLS
    # ============================================================
    
    # Product and Category APIs
    path('store/', include(store_router.urls)),
    
    # Cart
    path('store/cart/', CartView.as_view(), name='store-cart'),
    path('store/cart/clear/', CartClearView.as_view(), name='store-cart-clear'),
    
    # Wishlist
    path('store/wishlist/', WishlistView.as_view(), name='store-wishlist'),
    
    # Coupon Validation
    path('store/coupon/validate/', CouponViewSet.as_view({'post': 'validate'}), name='store-coupon-validate'),
    
    # Store Statistics (Admin only)
    path('store/stats/', store_stats, name='store-stats'),
    
    # ============================================================
    # ROUTER URLS
    # ============================================================
    
    path('', include(router.urls)),
]

# ============================================================
# AI E-Lab v2 routes
# ============================================================

from django.urls import path as _path, include as _include
urlpatterns += [_path("", _include("api.elab_ai_urls"))]

# ============================================================
# SERVE STATIC FILES
# ============================================================

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
