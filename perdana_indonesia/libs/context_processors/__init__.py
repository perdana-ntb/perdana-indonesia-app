from typing import Dict

from core.choices import PERDANA_USER_ROLE_CHOICES
from django.http import HttpRequest
from django.urls import reverse


def mappedSidebarMenu(request: HttpRequest) -> Dict:
    defaultKwargs = {'province_code': request.user.archer.region_code_name}
    return {
        PERDANA_USER_ROLE_CHOICES[0][0]: [
            {
                'type': 'group',
                'title': 'Dashboard',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Dashboard',
                            'icon': 'fa fa-dashboard',
                            'href': reverse('dashboardd:router', kwargs=defaultKwargs),
                            'is_active': bool(reverse('dashboardd:router', kwargs=defaultKwargs) == request.path)
                        }
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Pemanah',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Pemanah',
                            'icon': 'fa fa-bullseye',
                            'href': reverse('archer:club-members', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('archer:club-members', kwargs=defaultKwargs) == request.path
                            )
                        }
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Organisasi',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Pusat Latihan',
                            'icon': 'fa fa-user',
                            'href': reverse('club:clubs', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('club:clubs', kwargs=defaultKwargs) == request.path
                            )
                        },
                ]
            },
        ],
        PERDANA_USER_ROLE_CHOICES[1][0]: [
            {
                'type': 'group',
                'title': 'Dashboard',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Dashboard',
                            'icon': 'fa fa-dashboard',
                            'href': reverse('dashboardd:router', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('dashboardd:pengprov', kwargs=defaultKwargs) == request.path
                            )
                        }
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Pemanah',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Pemanah',
                            'icon': 'fa fa-bullseye',
                            'href': reverse('archer:club-members', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('archer:club-members', kwargs=defaultKwargs) == request.path
                            )
                        }, {
                            'type': 'item',
                            'title': 'Pendaftar',
                            'icon': 'fa fa-align-left',
                            'href': reverse('archer:club-applicants', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('archer:club-applicants', kwargs=defaultKwargs) == request.path
                            )
                        }
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Organisasi',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Pusat Latihan',
                            'icon': 'fa fa-user',
                            'href': reverse('club:clubs', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('club:clubs', kwargs=defaultKwargs) == request.path
                            )
                        },
                ]
            },
        ],
        PERDANA_USER_ROLE_CHOICES[2][0]: [
            {
                'type': 'group',
                'title': 'Dashboard',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Dashboard',
                            'icon': 'fa fa-dashboard',
                            'href': reverse('dashboardd:router', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('dashboardd:pengcab', kwargs=defaultKwargs) == request.path
                            )
                        }
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Pemanah',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Pemanah',
                            'icon': 'fa fa-bullseye',
                            'href': reverse('archer:club-members', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('archer:club-members', kwargs=defaultKwargs) == request.path
                            )
                        }, {
                            'type': 'item',
                            'title': 'Pendaftar',
                            'icon': 'fa fa-align-left',
                            'href': reverse('archer:club-applicants', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('archer:club-applicants', kwargs=defaultKwargs) == request.path
                            )
                        }
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Organisasi',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Pusat Latihan',
                            'icon': 'fa fa-user',
                            'href': reverse('club:clubs', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('club:clubs', kwargs=defaultKwargs) == request.path
                            )
                        },
                ]
            },
        ],
        PERDANA_USER_ROLE_CHOICES[3][0]: [
            {
                'type': 'group',
                'title': 'Dashboard',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Dashboard',
                            'icon': 'fa fa-dashboard',
                            'href': reverse('dashboardd:router', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('dashboardd:puslat', kwargs=defaultKwargs) == request.path
                            )
                        }
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Pemanah',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Pemanah',
                            'icon': 'fa fa-bullseye',
                            'href': reverse('archer:club-members', kwargs=defaultKwargs),
                        }, {
                            'type': 'item',
                            'title': 'Pendaftar',
                            'icon': 'fa fa-align-left',
                            'href': reverse('archer:club-applicants', kwargs=defaultKwargs),
                        }
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Organisasi',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Pusat Latihan',
                            'icon': 'fa fa-user',
                            'href': reverse('club:clubs', kwargs=defaultKwargs),
                            'is_active': bool(
                                reverse('club:clubs', kwargs=defaultKwargs) == request.path
                            )
                        },
                ]
            },
        ],
        PERDANA_USER_ROLE_CHOICES[4][0]: [
            {
                'type': 'group',
                'title': 'Dashboard',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Dashboard',
                            'icon': 'fa fa-dashboard',
                            'href': reverse('dashboardd:router', kwargs=defaultKwargs)
                        }
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Pemanah',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Informasi Pribadi',
                            'icon': 'fa fa-user',
                            'href': reverse('archer:club-members', kwargs=defaultKwargs)
                        },
                ]
            },
            {
                'type': 'group',
                'title': 'Informasi Organisasi',
                'items': [
                        {
                            'type': 'item',
                            'title': 'Informasi Pusat Latihan',
                            'icon': 'fa fa-user',
                            'href': reverse('club:clubs', kwargs=defaultKwargs)
                        },
                ]
            },
        ]
    }


def sidebar(request: HttpRequest):
    if not request.user.is_authenticated:
        return {}

    if not hasattr(request.user, 'archer') or not request.user.archer:
        return {}

    return {
        'sidebars': mappedSidebarMenu(request)[request.user.archer.role]
    }
