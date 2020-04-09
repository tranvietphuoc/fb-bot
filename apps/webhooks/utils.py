from apps.webhooks.bot import bot
from flask import request
from pixabay import Image
from apps import VERIFY_TOKEN, PAGE_ACCESS_TOKEN
import requests
import json
import sys


quick_replies_list = [
    {
        "content-type": "text",
        "title": "example",
        "payload": "<postback_payload>",
        "image_url": "https://example.com/img/example.png"
    },
    {
        "content-type": "text",
        "title": "example 1",
        "payload": "<postback_payload>",
        "image_url": "https://example.com/img/example1.png"
    }
]


def get_list_img(api_token, keyword):
    """Get the list of image objects from pixabay.com follow keyword"""
    image = Image(api_token)
    imgs = image.search(
        q=keyword,
        image_type='photo',
        order='latest'
    )
    return imgs['hits']


def verify_webhook(req):
    """
    This function take a flask request object sent by Facebook
    and verify it matches the verify token you sent if they match,
    allow request, else return an error
    """
    if req.args.get('hub.mode') == 'subscribe' and req.args.get('hub.challenge'):
        if req.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge'), 200
        return 'Invalid verification token', 403
    return "Welcome to my bot", 200


def pymessenger_respond(recipient_id, img_url):
    """
    use Pymessenger to send response to user
    """
    bot.send_image_url(recipient_id, img_url)
    return 'Success.'


# def is_user_message(event):
#     """Check if the message is a message from the user"""
#     return (event.get('message') and
#             event['message'].get('text') and not
#             event['message']('is_echo'))


def respond_text(recipient_id, text):
    graph_api = 'https://graph.facebook.com/v6.0/me/messages'
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
            "quick_replies": quick_replies_list
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    return requests.post(graph_api, headers=headers,
                         params=params, data=json.dumps(payload)).json()


def respond_img(recipient_id, response_img_url):
    """Sending response back to the user using facebook grap API"""
    graph_api = 'https://graph.facebook.com/v6.0/me/messages'
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": response_img_url,
                    "is_reusable": True
                }
            }
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    return requests.post(graph_api, headers=headers,
                         params=params, data=json.dumps(payload)).json()


def messaging_events(data):
    """Generate tuples of (sender_id, message_text) from the provided payload"""
    entry = data['entry']
    messaging_events = entry['messaging']
    for event in messaging_events:
        if event.get('message') and event['message'].get('text'):
            yield event['sender']['id'], event['message']['text'].encode('unicode_escapse')
        else:
            yield event['sender']['id'], "Cannot echo this"


def log(message):
    print(message)
    sys.stdout.flush()