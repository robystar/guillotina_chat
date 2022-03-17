from guillotina import configure
from guillotina.component import get_utility
from guillotina.interfaces import IObjectAddedEvent, IObjectModifiedEvent, IPrincipalRoleManager
from guillotina.utils import get_authenticated_user_id, get_current_request
from guillotina_chat.content import IConversation, IMessage
from guillotina_chat.utility import IMessageSender

@configure.subscriber(for_=(IConversation, IObjectAddedEvent))
@configure.subscriber(for_=(IConversation, IObjectModifiedEvent))
async def container_added(conversation, event):
    user_id = get_authenticated_user_id()
    if user_id not in conversation.users:
        conversation.users.append(user_id)

    manager = IPrincipalRoleManager(conversation)
    for user in conversation.users:
        manager.assign_role_to_principal(
            'guillotina_chat.ConversationParticipant', user)


@configure.subscriber(for_=(IMessage, IObjectAddedEvent))
async def message_added(message, event):
    utility = get_utility(IMessageSender)
    await utility.send_message(message)