import os
import json
import requests
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from .models import Section, TaskTemplate, Checklist, CheckItem, is_external_user
from .forms import CheckItemFormSet


# ──────────────────────────────────────────────────────────────────────────────
#  Checklist du jour
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def checklist_today(request):
    today = timezone.localdate()
    checklist, _ = Checklist.objects.get_or_create(date=today, defaults={'verifie_par': ''})

    # Synchronisation automatique
    templates = TaskTemplate.objects.select_related('section').order_by('section__ordre', 'ordre')
    existing  = set(checklist.items.values_list('nom', flat=True))
    needed    = set(t.nom for t in templates)
    if existing != needed:
        checklist.items.all().delete()
        for tmpl in templates:
            CheckItem.objects.create(checklist=checklist, nom=tmpl.nom, statut='A_VERIFIER')

    if request.method == 'POST':
        formset = CheckItemFormSet(request.POST, instance=checklist)
        verifie_par = request.POST.get('verifie_par','').strip()
        if formset.is_valid():
            checklist.verifie_par = verifie_par
            checklist.save()
            # On enregistre d'abord les items
            instance = formset.save()

            # Puis on marque chaque tâche modfiée par l'utilisateur courant
            user_label = request.user.get_full_name() or request.user.username
            for form in formset.forms:
                if form.has_changed():
                    # form.instance est le CheckItem correspondant
                    item = form.instance
                    item.verifie_par = user_label
                    item.save(update_fields=['verifie_par'])

            return redirect('historique_checklists')
    else:
        formset = CheckItemFormSet(instance=checklist)
        # Toujours utiliser le nom de l'utilisateur connecté
        full = request.user.get_full_name()
        verifie_par = full if full else request.user.username

    # Crée un lookup rapide nom -> template
    tpl_map = {t.nom: t for t in templates}
    sections = []
    for section in Section.objects.all():
        lst = []
        for f in formset.forms:
            nom = f.initial['nom']
            tpl = tpl_map[nom]
            if tpl.section_id == section.id:
                lst.append((f, tpl))
        if lst:
            sections.append((section, lst))

    # Statistiques journalières
    stats = checklist.items.aggregate(
        total=Count('id'),
        ok   =Count('id', filter=Q(statut='OK')),
        ko   =Count('id', filter=Q(statut='KO')),
        av   =Count('id', filter=Q(statut='A_VERIFIER')),
        ec   =Count('id', filter=Q(statut='EN_COURS')),
    )
    total = stats['total'] or 1
    pct   = {k: round(stats[k]/total*100,1) for k in ('ok','ko','av','ec')}

    return render(request, 'checklist/checklist_today.html', {
        'sections':      sections,
        'management_form': formset.management_form,
        'date':          today,
        'verifie_par':   verifie_par,
        'stats_pct':     pct,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Historique & filtrage
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def historique_checklists(request):
    start = request.GET.get('start')
    end   = request.GET.get('end')

    qs = Checklist.objects.annotate(
        total_av=Count('items', filter=Q(items__statut='A_VERIFIER')),
        total_ok=Count('items', filter=Q(items__statut='OK')),
        total_ko=Count('items', filter=Q(items__statut='KO')),
        total_ec=Count('items', filter=Q(items__statut='EN_COURS')),
    )
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)
    qs = qs.order_by('-date')

    return render(request, 'checklist/historique_checklists.html', {
        'checklists': qs,
        'start':      start,
        'end':        end,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Détail + navigation Prev/Next
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def checklist_detail(request, date):
    checklist = get_object_or_404(Checklist, date=date)
    prev      = Checklist.objects.filter(date__lt=checklist.date).order_by('-date').first()
    nxt       = Checklist.objects.filter(date__gt=checklist.date).order_by('date').first()

    return render(request, 'checklist/checklist_details.html', {
        'checklist': checklist,
        'prev_date': prev.date if prev else None,
        'next_date': nxt.date if nxt else None,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Dashboard statistique interactif
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    # Récupération des filtres de date en GET
    start = request.GET.get('start')
    end   = request.GET.get('end')

    # Nombre total de templates pour calcul %
    total_templates = TaskTemplate.objects.count() or 1

    # Queryset annoté
    qs = Checklist.objects.annotate(
        ok=Count('items', filter=Q(items__statut='OK')),
        ko=Count('items', filter=Q(items__statut='KO')),
        av=Count('items', filter=Q(items__statut='A_VERIFIER')),
        ec=Count('items', filter=Q(items__statut='EN_COURS')),
    )

    # Application des filtres
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)

    qs = qs.order_by('date')

    # Sérialisation des données
    dates  = [c.date.strftime('%Y-%m-%d') for c in qs]
    pct_ok = [round(c.ok/total_templates*100,1) for c in qs]
    pct_ko = [round(c.ko/total_templates*100,1) for c in qs]
    pct_av = [round(c.av/total_templates*100,1) for c in qs]
    pct_ec = [round(c.ec/total_templates*100,1) for c in qs]

    # Moyennes globales
    avg = {
        'ok': round(sum(pct_ok)/len(pct_ok),1) if pct_ok else 0,
        'ko': round(sum(pct_ko)/len(pct_ko),1) if pct_ko else 0,
        'av': round(sum(pct_av)/len(pct_av),1) if pct_av else 0,
        'ec': round(sum(pct_ec)/len(pct_ec),1) if pct_ec else 0,
    }

    return render(request, 'checklist/dashboard.html', {
        'dates':   json.dumps(dates),
        'ok':      json.dumps(pct_ok),
        'ko':      json.dumps(pct_ko),
        'av':      json.dumps(pct_av),
        'ec':      json.dumps(pct_ec),
        'avg_pct': avg,
        'start':   start,
        'end':     end,
    })