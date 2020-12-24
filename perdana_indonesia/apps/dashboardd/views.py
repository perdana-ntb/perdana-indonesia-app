from core.permissions import PERDANA_MANAGEMENT_USER_ROLE
from core.views import RoleBasesAccessTemplateView


class DashboardTemplateView(RoleBasesAccessTemplateView):
    template_name = 'dashboardd/dashboard.html'
    allowed_groups = PERDANA_MANAGEMENT_USER_ROLE
