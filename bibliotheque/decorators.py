from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('bibliotheque:connexion')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('bibliotheque:connexion')
        if not request.user.est_admin():
            messages.error(request, "Accès refusé. Cette page est réservée aux administrateurs.")
            return redirect('bibliotheque:tableau_bord')
        return view_func(request, *args, **kwargs)
    return wrapper


def gestionnaire_ou_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('bibliotheque:connexion')
        if request.user.role not in ['admin', 'gestionnaire']:
            messages.error(request, "Accès refusé.")
            return redirect('bibliotheque:connexion')
        return view_func(request, *args, **kwargs)
    return wrapper
