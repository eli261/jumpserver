# -*- coding: utf-8 -*-
#
from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver

from common.utils import get_logger
from common.decorator import on_transaction_commit
from .models import AssetPermission


logger = get_logger(__file__)


@receiver(post_save, sender=AssetPermission, dispatch_uid="my_unique_identifier")
@on_transaction_commit
def on_permission_created(sender, instance=None, created=False, **kwargs):
    pass
    # AssetPermissionUtil.expire_all_cache()


@receiver(post_save, sender=AssetPermission)
def on_permission_update(sender, **kwargs):
    pass
    # AssetPermissionUtil.expire_all_cache()


@receiver(post_delete, sender=AssetPermission)
def on_permission_delete(sender, **kwargs):
    pass
    # AssetPermissionUtil.expire_all_cache()


@receiver(m2m_changed, sender=AssetPermission.nodes.through)
def on_permission_nodes_changed(sender, instance=None, **kwargs):
    # AssetPermissionUtil.expire_all_cache()
    if isinstance(instance, AssetPermission) and kwargs['action'] == 'post_add':
        logger.debug("Asset permission nodes change signal received")
        nodes = kwargs['model'].objects.filter(pk__in=kwargs['pk_set'])
        system_users = instance.system_users.all()
        for system_user in system_users:
            system_user.nodes.add(*tuple(nodes))


@receiver(m2m_changed, sender=AssetPermission.assets.through)
def on_permission_assets_changed(sender, instance=None, **kwargs):
    # AssetPermissionUtil.expire_all_cache()
    if isinstance(instance, AssetPermission) and kwargs['action'] == 'post_add':
        logger.debug("Asset permission assets change signal received")
        assets = kwargs['model'].objects.filter(pk__in=kwargs['pk_set'])
        system_users = instance.system_users.all()
        for system_user in system_users:
            system_user.assets.add(*tuple(assets))


@receiver(m2m_changed, sender=AssetPermission.system_users.through)
def on_permission_system_users_changed(sender, instance=None, **kwargs):
    # AssetPermissionUtil.expire_all_cache()
    if isinstance(instance, AssetPermission) and kwargs['action'] == 'post_add':
        logger.debug("Asset permission system_users change signal received")
        system_users = kwargs['model'].objects.filter(pk__in=kwargs['pk_set'])
        assets = instance.assets.all()
        nodes = instance.nodes.all()
        for system_user in system_users:
            system_user.nodes.add(*tuple(nodes))
            system_user.assets.add(*tuple(assets))
