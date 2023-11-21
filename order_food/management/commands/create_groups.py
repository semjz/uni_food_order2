from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create Student and Moderator groups and assign their permissioms'

    def handle(self, *args, **options):
        moderator_group, created = Group.objects.get_or_create(name="Moderator")
        student_group, created = Group.objects.get_or_create(name="Student")

        moderator_permissions = [
            "add_food", "change_food", "delete_food",
            "change_any_order", "delete_any_order",
            "view_a_student_order", "view_all_orders",
            "view_a_student_wallet"
        ]
        for permission_name in moderator_permissions:
            permission = Permission.objects.get(codename=permission_name)
            moderator_group.permissions.add(permission)

        student_permissions = [
            "add_order", "change_own_order", "delete_own_order",
            "view_own_order", "view_all_own_orders",
            "view_own_wallet", "charge_own_wallet"
        ]
        for permission_name in student_permissions:
            permission = Permission.objects.get(codename=permission_name)
            student_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS("Student and Moderator group created successfully."))
