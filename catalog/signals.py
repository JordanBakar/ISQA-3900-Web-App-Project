from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    """Create default groups and permissions."""

    # Create Admin Group
    admin_group, created = Group.objects.get_or_create(name='Admin')
    if created:
        # Assign all permissions to Admin group
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)
        print("Admin group created with all permissions.")

    # Create Employee Group
    employee_group, created = Group.objects.get_or_create(name='Employee')
    if created:
        employee_permissions = [
            'add_order',
            'change_order',
            'delete_order',
            'view_order',
            'add_pizza',
            'change_pizza',
            'delete_pizza',
            'view_pizza',
            'view_member',
            'view_guest',
        ]
        for perm in employee_permissions:
            permission = Permission.objects.filter(codename=perm).first()
            if permission:
                employee_group.permissions.add(permission)
        print("Employee group created with specific permissions.")

    # Create Member Group
    member_group, created = Group.objects.get_or_create(name='Member')
    if created:
        member_permissions = [
            'add_order',
            'view_order',
            'view_pizza',
            'change_member',
            'view_member',
        ]
        for perm in member_permissions:
            permission = Permission.objects.filter(codename=perm).first()
            if permission:
                member_group.permissions.add(permission)
        print("Member group created with specific permissions.")

    # Create Guest Group
    guest_group, created = Group.objects.get_or_create(name='Guest')
    if created:
        guest_permissions = [
            'view_pizza',
        ]
        for perm in guest_permissions:
            permission = Permission.objects.filter(codename=perm).first()
            if permission:
                guest_group.permissions.add(permission)
        print("Guest group created with limited permissions.")
