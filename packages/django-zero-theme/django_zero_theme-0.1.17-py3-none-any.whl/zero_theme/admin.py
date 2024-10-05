from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from zero_theme.widgets import zero_widget_registry

USER_MODEL = get_user_model()
app_name = USER_MODEL._meta.app_label


class UserWidget:
    template_name = 'widget/user_widgets.html'
    priority = 1
    app_name = app_name

    def get_user_data(self):
        total_user = USER_MODEL.objects.all().count()

        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        users_last_30_days = USER_MODEL.objects.filter(date_joined__gte=thirty_days_ago)
        users_last_30_days_join_count = users_last_30_days.count()

        users_logged_in_last_30_days = USER_MODEL.objects.filter(last_login__gte=thirty_days_ago)
        last_30_days_login_count = users_logged_in_last_30_days.count()

        total_groups = Group.objects.count()

        context = {
            'total_user': total_user,
            'total_groups': total_groups,
            'last_30_days_login_count': last_30_days_login_count,
            'last_30_days_users': users_last_30_days_join_count
        }
        return context


zero_widget_registry.register(UserWidget)
