# -*- coding: utf-8 -*-
from guillotina import configure
from guillotina.addons import Addon
from guillotina.utils import get_registry
from guillotina.content import create_content_in_container
from guillotina.interfaces import IRolePermissionManager



@configure.addon(
    name="guillotina_chat",
    title="Nuova Guillotina server application chat")
class ManageAddon(Addon):

    @classmethod
    async def install(cls, container, request):
        roleperm = IRolePermissionManager(container)
        roleperm.grant_permission_to_role_no_inherit('guillotina.AccessContent','guillotina.Member')
        if not await container.async_contains('conversazioni'):
            conversations = await create_content_in_container(container,'Folder','Conversazioni',id='conversazioni',creators=('root',),contributors=('root',))
            roleperm = IRolePermissionManager(conversations)
            roleperm.grant_permission_to_role('guillotina.AddContent','guillotina.Member')        
            roleperm.grant_permission_to_role('guillotina.AccessContent','guillotina.Member')        


    @classmethod
    async def uninstall(cls, container, request):
        registry = task_vars.registry.get()
