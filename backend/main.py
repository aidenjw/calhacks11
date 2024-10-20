# main.py
import os
from openai import OpenAI
import json
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    DeepgramClientOptions,
    PrerecordedOptions
)
import ast
import subprocess
import threading
import time
import requests

# Get API keys from environment variables
openai_api_key = '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'
deepgram_api_key = 'b8914720e80100689c2d3d53e54088bbc9772b6e'

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Function to create the assistant
def createAssistant():
    assistant = client.beta.assistants.create(
        name="Mental Health Assistant", 
        instructions=(
            "You are an assistant helping a suicide hotline volunteer. "
            "Use the conversation history to provide helpful suggestions "
            "and answer any questions the volunteer asks."
        ),
        tools=[{"type": "file_search", "type" : "code_interpreter"}],
        model="gpt-4o"  # Ensure this model name is correct
    )
    return assistant


# Function to upload files to the assistant's vector store
def uploadFiles(assistantname, files):
    vector_store = client.beta.vector_stores.create(name="Mental Health Documents")
    file_paths = files
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    assistant = client.beta.assistants.update(
        assistant_id=assistantname.id, 
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
    )

# Function to open a new conversation thread
def openConversation():
    thread = client.beta.threads.create()
    return thread

# Function to ask a question in the conversation
def askQuestion(thread, query):
    # Ask a question in the conversation
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=[{"type": "text", "text": query}]  # Corrected format
    )


# Main logic to create an assistant, upload files, and handle a conversation
# main.py

# ... existing imports and code ...

# Function to handle the conversation
# main.py

def handleConversation(conversation_id, assistant_id, query):
    print(f"Adding user message to conversation {conversation_id}: {query}")
    # Add the user's message to the conversation
    client.beta.threads.messages.create(
        thread_id=conversation_id,
        role="user",
        content=[{"type": "text", "text": query}]
    )

    # Fetch the updated conversation messages
    messages = client.beta.threads.messages.list(thread_id=conversation_id).data

    # Prepare the messages for the assistant
    assistant_messages = []
    for msg in messages:
        content_text = ''.join(
            part.text.value for part in msg.content if part.type == 'text'
        )
        assistant_messages.append({
            "role": msg.role,
            "content": content_text
        })

    print("Conversation messages:")
    for msg in assistant_messages:
        print(f"{msg['role']}: {msg['content']}")

    # Run the assistant with the conversation messages
    run = client.beta.threads.runs.create_and_poll(
        thread_id=conversation_id,
        assistant_id=assistant_id,
        instructions=(
            "You are an assistant helping a suicide hotline volunteer. "
            "Use the conversation history to provide helpful suggestions "
            "and answer any questions the volunteer asks. Only the hotline worker/volunteer can view your responses.\n"
            "Please provide your response in the following JSON format:\n"
            "{ \"summary\": \"...\", \"suggestions\": \"...\", \"full_response\": \"...\"}\n"
            "Make the summary less than 30 words. Summarise the entire history of conversation\n"
            "Make the suggestions a bullet-point list of suggestions like this:\n"
            "- suggestion one\n- suggestion two\n- suggestion three\n"
            "For a total of less than 30 words. For the full_response make it less than 30 words. "
            "The full response is the ongoing conversation that you are having with the hotline volunteer/worker."
        ),
    )

    print(f"Run status: {run.status}")

    if run.status == 'completed':
        # Fetch the latest assistant message
        messages = client.beta.threads.messages.list(thread_id=conversation_id)
        assistant_messages = [msg for msg in messages.data if msg.role == 'assistant']
        if assistant_messages:
            latest_message = assistant_messages[0]
            content_parts = latest_message.content
            text_parts = [part.text.value for part in content_parts if part.type == 'text']
            response = ''.join(text_parts)
            print(f"Assistant response: {response}")

            # Parse the assistant's response as JSON
            try:
                response_dict = json.loads(response)
                return response_dict
            except json.JSONDecodeError:
                print("Failed to parse assistant response as JSON.")
                # Return the full response under 'full_response' key
                return {
                    'summary': '',
                    'suggestions': '',
                    'full_response': response
                }
        else:
            print("No assistant response found.")
            return {
                'summary': '',
                'suggestions': '',
                'full_response': "No assistant response found."
            }
    else:
        print("Failed to generate a response.")
        return {
            'summary': '',
            'suggestions': '',
            'full_response': "Failed to generate a response."
        }

# Transcription Tools
def words_until(recording1, recording2, time):
    rec1 = recording1
    rec2 = recording2
    print(deepgram_api_key)
    command = [
        'curl',
        '--request', 'POST',
        '--header', f'Authorization: Token {deepgram_api_key}',
        '--header', 'Content-Type: audio/mp3',
        '--data-binary', f'@{rec1}',
        '--url', 'https://api.deepgram.com/v1/listen?diarize=true'
    ]
    temp1 = subprocess.run(command, stdout=subprocess.PIPE)
    result1 = ast.literal_eval(temp1.stdout.decode())['results']['channels'][0]['alternatives'][0]['words']
    command = [
        'curl',
        '--request', 'POST',
        '--header', f'Authorization: Token {deepgram_api_key}',
        '--header', 'Content-Type: audio/mp3',
        '--data-binary', f'@{rec2}',
        '--url', 'https://api.deepgram.com/v1/listen?diarize=true'
    ]
    temp2 = subprocess.run(command, stdout=subprocess.PIPE)
    result2 = ast.literal_eval(temp2.stdout.decode())['results']['channels'][0]['alternatives'][0]['words']
    temporary1 = result1
    result1 = []
    for entry in temporary1:
        if entry['end'] <= time:
            result1.append(entry)
    temporary2 = result2
    result2 = []
    for entry in temporary2:
        if entry['end'] <= time:
            result2.append(entry)
    word = []
    def run(res1, res2, lis):
        if len(res1) == 0 or len(res2) == 0:
            return []
        mod1 = res1
        mod2 = res2
        lis.append("")
        while True:
            if mod1[0]['start'] <= res2[0]['start']:
                lis[-1] += " " + mod1[0]['word'] 
                mod1 = mod1[1:]
            else:
                lis.extend(run(mod2,mod1,[]))
                break
            if len(mod1) == 0 and len(mod2) != 0:
                lis.append("")
                for i in mod2:
                    lis[-1] += " " + i['word']
                return lis
                
        return lis
    
    return run(result1, result2, word)
    
def currTranscription(rec1, rec2, time):
    res = words_until(rec1, rec2, time)[1:]
    for i in range(len(res)):
        if i % 2 == 0:
            res[i] = "Operator: " + res[i]
        else:
            res[i] = "Caller: " + res[i]
    ret = ""
    for i in res:
        ret += i + "\n"


    return ret

# a