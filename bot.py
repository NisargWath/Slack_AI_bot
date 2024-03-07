import slack
import os 
from pathlib import Path
from dotenv import load_dotenv
import ssl
from flask import Flask,render_template, request, jsonify



from IPython.display import display
from IPython.display import Markdown
import textwrap


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

import google.generativeai as genai
import os






from slackeventsapi import SlackEventAdapter
# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



app = Flask(__name__)


# Path to the cacert.pem file on your system
# Update this path to match your system
cacert_path = '/Users/nisargwath/anaconda3/pkgs/ca-certificates-2023.12.12-hca03da5_0/ssl/cacert.pem'

# Create SSL context with certificate verification
ssl_context = ssl.create_default_context(cafile=cacert_path)

# Initialize the Slack WebClient with your token
client = slack.WebClient(token='xoxb-6345240911265-6745852414338-SxeR9GdYeWtImgysw3S1dPi2', ssl=ssl_context)

# Try posting a message to a channel

slack_event_adapter = SlackEventAdapter('1060015b5a1506a69ff40620a5bfd7a1'
                                        ,'/', app)

@app.route('/', methods=['POST'])
def slack_events():
    payload = request.json
    if "challenge" in payload:
        return jsonify({"challenge": payload["challenge"]})
    return '', 200



BOT_ID = client.api_call("auth.test")["user_id"]
@slack_event_adapter.on('message')
def message(payload):
    GOOGLE_API_KEY = "AIzaSyDPAtGf-Rwe5nUQ_uDCiifRGVQxND5cB_c"
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name = "gemini-pro")

    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text') + "give me in 100-200 words only"
    response = model.generate_content(text)
    ans = response.text.strip('"')

    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=ans)



if __name__ == '__main__':
    app.run(debug=True, port=5002)
    slack_event_adapter.start(port=3000)