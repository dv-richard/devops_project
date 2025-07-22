from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from checklist import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='checklist_today', permanent=False), name='home'),
    path('admin/', admin.site.urls),

    # Authentification classique
    path('accounts/login/',  auth_views.LoginView.as_view(template_name='checklist/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Vues principales
    path('checklist/',             views.checklist_today,       name='checklist_today'),
    path('checklist/historique/', views.historique_checklists, name='historique_checklists'),
    path('checklist/<date>/',      views.checklist_detail,      name='checklist_detail'),
    path('dashboard/',             views.dashboard,             name='dashboard'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
