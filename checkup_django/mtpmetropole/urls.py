from django.urls import path
from checklist import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='checklist_today', permanent=False), name='home'),
    path('admin/', admin.site.urls),

    # OIDC SSO
    path('oidc/login/',    views.oidc_login,    name='oidc_login'),
    path('oidc/callback/', views.oidc_callback, name='oidc_callback'),

    # API mobile/JS
    path('api/auth/oidc/', views.OIDCAuthView.as_view(), name='oidc_auth'),

    # Vos views protégées
    path('checklist/',         views.checklist_today,       name='checklist_today'),
    path('checklist/historique/', views.historique_checklists, name='historique_checklists'),
    path('checklist/<date>/',  views.checklist_detail,      name='checklist_detail'),
    path('dashboard/',         views.dashboard,             name='dashboard'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)