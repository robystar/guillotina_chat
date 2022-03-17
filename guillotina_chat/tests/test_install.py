import pytest


pytestmark = [pytest.mark.asyncio]


async def test_install(guillotina_chat_requester):  # noqa
    async with guillotina_chat_requester as requester:
        response, _ = await requester('GET', '/db/guillotina/@addons')
        assert 'guillotina_chat' in response['installed']
