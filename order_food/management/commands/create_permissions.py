from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from order_food.models import Food, Order, Wallet


class Command(BaseCommand):
    help = 'Create Student and Moderator groups and assign their permissions'

    def handle(self, *args, **options):
        food_content_type = ContentType.objects.get_for_model(Food)
        order_content_type = ContentType.objects.get_for_model(Order)
        wallet_content_type = ContentType.objects.get_for_model(Wallet)

        # Define a list of permissions to create
        permissions_to_create = [
            ('add_food', 'Can add food', food_content_type),
            ('change_food', 'Can change food', food_content_type),
            ('delete_food', 'Can delete food', food_content_type),
            ('add_order', 'Can add own order', order_content_type),
            ('change_any_order', 'Can change any order', order_content_type),
            ('delete_any_order', 'Can delete any order', order_content_type),
            ('change_own_order', 'Can change own order', order_content_type),
            ('delete_own_order', 'Can delete own order', order_content_type),
            ('view_a_student_order', 'Can view a student order', order_content_type),
            ('view_all_orders', 'Can view all orders', order_content_type),
            ('view_own_order', 'Can view own order', order_content_type),
            ('view_all_own_orders', 'Can view all own orders', order_content_type),
            ('view_a_student_wallet', 'Can view a student wallet', wallet_content_type),
            ('view_own_wallet', 'Can view own wallet', wallet_content_type),
            ('charge_own_wallet', 'Can charge own wallet', wallet_content_type),
        ]

        # Create permissions
        for codename, name, content_type in permissions_to_create:
            try:
                Permission.objects.get(codename=codename, content_type=content_type)
                self.stdout.write(self.style.SUCCESS(f'Permission already exists: {codename}'))
            except Permission.DoesNotExist:
                Permission.objects.create(codename=codename, name=name, content_type=content_type)
                self.stdout.write(self.style.SUCCESS(f'Permission created: {codename}'))

        self.stdout.write(self.style.SUCCESS("All permissions checked/created successfully."))

        self.stdout.write(self.style.SUCCESS("All permissions created successfully."))