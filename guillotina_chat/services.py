from guillotina import configure
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IContainer, IResourceSerializeToJsonSummary
from guillotina.utils import get_authenticated_user_id
from guillotina_chat.content import IConversation

@configure.service(context=IContainer, name='@conversations',
                   permission='guillotina.AccessContent')
async def get_conversations(context, request):
    results = []
    conversations = await context.async_get('Conversazioni')
    user_id = get_authenticated_user_id()
    async for conversation in conversations.async_values():
        if user_id in getattr(conversation, 'users', []):
            summary = await get_multi_adapter(
                (conversation, request),
                IResourceSerializeToJsonSummary)()
            results.append(summary)
    results = sorted(results, key=lambda conv: conv['creation_date'])
    return results


@configure.service(context=IConversation, name='@messages',
                   permission='guillotina.AccessContent')
async def get_messages(context, request):
    results = []
    async for message in context.async_values():
        summary = await get_multi_adapter(
            (message, request),
            IResourceSerializeToJsonSummary)()
        results.append(summary)
    results = sorted(results, key=lambda mes: mes['creation_date'])
    return results