# main.py
import os
from openai import OpenAI
import json

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
        tools=[{"type": "file_search"}],
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
    # Modify the instructions to request JSON output
    run = client.beta.threads.runs.create_and_poll(
        thread_id=conversation_id,
        assistant_id=assistant_id,
        instructions=(
            "You are an assistant helping a suicide hotline volunteer. "
            "Use the conversation history to provide helpful suggestions "
            "and answer any questions the volunteer asks.\n"
            "Please provide your response in the following JSON format:\n"
            "{ 'summary': '...', 'suggestions': '...', 'full_response': '...'}"
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
