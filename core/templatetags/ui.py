"""
Template tags e filtros de apresentação do tema monocromático.

Somente formatação/markup: nenhuma regra de negócio vive aqui.
"""
from decimal import Decimal, InvalidOperation

from django import template
from django.utils.html import format_html, format_html_join

register = template.Library()

# ---------------------------------------------------------------------------
# Ícones (SVG inline, traço 24x24, herdam currentColor)
# ---------------------------------------------------------------------------
_ICONS = {
    'home': 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
    'cube': 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
    'office': 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
    'switch': 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4',
    'plus': 'M12 4v16m8-8H4',
    'minus': 'M20 12H4',
    'report': 'M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    'users': 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
    'user': 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
    'user-minus': 'M13 7a4 4 0 11-8 0 4 4 0 018 0zM9 14a6 6 0 00-6 6v1h12v-1a6 6 0 00-6-6zM21 12h-6',
    'logout': 'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1',
    'menu': 'M4 6h16M4 12h16M4 18h16',
    'x': 'M6 18L18 6M6 6l12 12',
    'search': 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
    'arrow-left': 'M10 19l-7-7m0 0l7-7m-7 7h18',
    'arrow-right': 'M14 5l7 7m0 0l-7 7m7-7H3',
    'chevron-right': 'M9 5l7 7-7 7',
    'eye': [
        'M15 12a3 3 0 11-6 0 3 3 0 016 0z',
        'M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z',
    ],
    'eye-off': 'M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21',
    'pencil': 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z',
    'trash': 'M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16',
    'warning': 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
    'bell': 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
    'sun': 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z',
    'moon': 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z',
    'lock': 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z',
    'phone': 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z',
    'pin': 'M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z',
    'mail': 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    'calendar': 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z',
    'check': 'M5 13l4 4L19 7',
    'check-circle': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    'x-circle': 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
    'info': 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'alert-circle': 'M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'adjust': 'M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4',
    'inbox-in': 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4',
    'inbox-out': 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12',
    'sparkles': 'M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z',
    'refresh': 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
    'trend-up': 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6',
    'trend-down': 'M13 17h8m0 0V9m0 8l-8-8-4 4-6-6',
    'currency': 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'tag': 'M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z',
    'document': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    'trophy': 'M5 3h14v4a7 7 0 01-14 0V3zm0 2H3a2 2 0 002 4m14-4h2a2 2 0 01-2 4M12 14v4m-4 3h8m-6-3h4',
    'ban': 'M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636',
}


@register.simple_tag
def icon(name, css='w-5 h-5'):
    """Renderiza um SVG inline. Ex.: {% icon 'plus' 'w-4 h-4' %}"""
    paths = _ICONS.get(name)
    if paths is None:
        return ''
    if isinstance(paths, str):
        paths = [paths]
    inner = format_html_join(
        '', '<path stroke-linecap="round" stroke-linejoin="round" d="{}"/>', ((p,) for p in paths)
    )
    return format_html(
        '<svg class="{}" fill="none" stroke="currentColor" stroke-width="1.75" '
        'viewBox="0 0 24 24" aria-hidden="true" focusable="false">{}</svg>',
        css, inner,
    )


# ---------------------------------------------------------------------------
# Formatação pt-BR
# ---------------------------------------------------------------------------
def _to_decimal(value):
    if value is None or value == '':
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _pt_br(number, decimals):
    """1234.5 -> '1.234,50' sem depender do locale do servidor."""
    texto = f'{number:,.{decimals}f}'
    return texto.replace(',', '#').replace('.', ',').replace('#', '.')


@register.filter
def brl(value, decimals=2):
    """Valor monetário: R$ 1.234,56"""
    d = _to_decimal(value)
    if d is None:
        return '—'
    try:
        decimals = int(decimals)
    except (TypeError, ValueError):
        decimals = 2
    return f'R$ {_pt_br(d, decimals)}'


@register.filter
def qtd(value, max_decimals=2):
    """Quantidade com milhar e até N casas, sem zeros à direita: 1.250 / 12,5"""
    d = _to_decimal(value)
    if d is None:
        return '—'
    try:
        max_decimals = int(max_decimals)
    except (TypeError, ValueError):
        max_decimals = 2
    texto = _pt_br(d, max_decimals)
    if max_decimals and ',' in texto:
        texto = texto.rstrip('0').rstrip(',')
    return texto


@register.filter
def iniciais(usuario):
    """Iniciais para o avatar (fallback seguro quando nome vazio)."""
    try:
        a = (usuario.first_name or '')[:1]
        b = (usuario.last_name or '')[:1]
        texto = (a + b).upper()
        return texto or (usuario.username or '?')[:1].upper()
    except AttributeError:
        return '?'


@register.simple_tag
def status_label(status):
    """Rótulo textual do status_estoque do produto."""
    return {
        'normal': 'Normal',
        'alerta': 'Atenção',
        'critico': 'Crítico',
        'zerado': 'Zerado',
    }.get(status, '')


@register.filter
def nivel_estoque(produto):
    """
    Nível de estoque do produto: normal | alerta | critico | zerado.
    Usa produto.status_estoque; se o model levantar TypeError (Decimal * float em
    status_estoque), repete a mesma regra com Decimal. Somente apresentação.
    """
    try:
        return produto.status_estoque
    except TypeError:
        try:
            if produto.quantidade <= 0:
                return 'zerado'
            if produto.quantidade <= produto.estoque_minimo:
                return 'critico'
            if produto.quantidade <= produto.estoque_minimo * Decimal('1.5'):
                return 'alerta'
            return 'normal'
        except (TypeError, AttributeError):
            return 'normal'