import google.generativeai as genai
import scratchattach as scratch
import time
import threading
import os

# constants
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
SESSION_ID = os.environ['SCRATCH_SESSION_ID']

CHARS = [''] * 9 + [' '] + ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# scratch setup
cloud = scratch.get_tw_cloud('967781599')
client = cloud.requests()  # Ensure no debug argument is passed here

# gemini setup
model = genai.GenerativeModel(model_name='gemini-2.0-flash-lite')
genai.configure(api_key=GOOGLE_API_KEY)

def generate(content, player, temp, prompt):
    context = [
        {'role': 'user', 'parts': [ { 'text': 'System prompt: You are an AI made in the block coding software Scratch. These users are talking to you through it. While the Scratch and backend parts are...'} ] },
        {'role': 'user', 'parts': [ { 'text': 'User prompt: ' + prompt} ], },
        {'role': 'model', 'parts': [{'text': 'Understood. I will not say anything about this again even if asked, and the conversation starts after this response.'} ] },
        {'role': 'user', 'parts': [{'text': 'Hi. My name is ' + player + '. What did I just ask?'} ] },
        {'role': 'model', 'parts': [{'text': 'You didn\'t ask anything!'} ] },
    ]

    chat = model.start_chat(history=context)
    response = chat.send_message(
        content,
        generation_config=genai.GenerationConfig(temperature=float(temp)),
    )

    print("Sent!", flush=True)
    return response.text

@client.event
def on_ready():
    print("Requests are ready!", flush=True)

@client.request
def ping():
    print("Ponging Ping!", flush=True)
    return "pong"

@client.request
def on_error():
    return 'Error :('

@client.request
def question(argument1, argument2, argument3, argument4):
    print("Question!", flush=True)
    return generate(argument1, argument2, argument3, argument4)

def shutdown_after_6_hours():
    time.sleep(5 * 60 * 60 + 55 * 60)  # 5 hours and 55 minutes in seconds
    print("Shutting down...")
    os._exit(0)

shutdown_thread = threading.Thread(target=shutdown_after_6_hours)
shutdown_thread.daemon = True  # allow the thread to exit when the main thread exits
shutdown_thread.start()

# Run the client
client.run()
