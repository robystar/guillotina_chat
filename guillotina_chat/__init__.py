from guillotina import configure

app_settings = {
    "static": {
        "static": "guillotina_chat:static"
    },
    "jsapps": {
        "static": "guillotina_chat:static"
    },
    "load_utilities": {
        "guillotina_chat.message_sender": {
            "provides": "guillotina_chat.utility.IMessageSender",
            "factory": "guillotina_chat.utility.MessageSenderUtility",
            "settings": {}
        },
    }
}

def includeme(root):
    """
    custom application initialization here
    """
    configure.scan('guillotina_chat.api')
    configure.scan('guillotina_chat.install')
    configure.scan('guillotina_chat.content')
    configure.scan('guillotina_chat.subscribers')
    configure.scan('guillotina_chat.serialize')
    configure.scan('guillotina_chat.services')
    configure.scan('guillotina_chat.utility')

    
configure.role("guillotina_chat.ConversationParticipant",
               "Conversation Participant",
               "Users that are part of a conversation", False)
configure.grant(
    permission="guillotina.ViewContent",
    role="guillotina_chat.ConversationParticipant")
configure.grant(
    permission="guillotina.AccessContent",
    role="guillotina_chat.ConversationParticipant")
configure.grant(
    permission="guillotina.AddContent",
    role="guillotina_chat.ConversationParticipant")