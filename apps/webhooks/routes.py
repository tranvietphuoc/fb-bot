from flask import request, Blueprint
from apps.webhooks.utils import (verify_webhook, get_list_img,
                                 respond_img, respond_text)
from apps import PIXABAY_API_KEY


webhooks = Blueprint('webhooks', __name__)


@webhooks.route('/', methods=['GET'])
def verify():
    """
    Before allowing people to message your bot, Facebook has implemented
    a verify token that confirm all requests that your bot recieves came
    from Facebook.
    """
    return verify_webhook(request)


@webhooks.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    print("Handling...")
    data = request.get_json()
    print(data)
    for entry in data['entry']:
        messaging_events = entry['messaging']
        for event in messaging_events:
            if event.get('message') and event.get('message')['text']:
                recipient_id, text = event['recipient']['id'], event['message']['text']
                respond_text(recipient_id, text)


    # list_response_img = get_list_img(PIXABAY_API_KEY, 'teddy bear')
    # if data["object"] == "page":

    #     for sender_id, _ in messaging_events(data):
    #         # respond_text(sender_id, "hello my bot")
    #         for response_img in list_response_img:
    #             respond_img(sender_id, response_img['largeImageURL'])
    return 'OK', 200
