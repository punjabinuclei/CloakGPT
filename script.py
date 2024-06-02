# !pip install groq
from transformers import pipeline
from huggingface_hub import login
from groq import Groq



# hf login
login(token="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")

# groq api key
client = Groq(
    api_key="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",
)


# Replace with your specific model if it's available on Hugging Face
classifier = pipeline("ner", model="bigcode/starpii", aggregation_strategy="simple")
text = input("Enter your prompt: ") 
result = classifier(text)
print(result)



def replace_pii(text, result):
    # Sort entities by start index in descending order to handle replacements from the end of the string
    result = sorted(result, key=lambda x: x['start'], reverse=True)
    
    for entity in result:
        placeholder = entity['entity_group']
        start = entity['start']
        end = entity['end']

        # Replace the PII in the text, and add spaces if necessary
        if start > 0 and text[start - 1] != ' ':
            placeholder = ' ' + placeholder
        if end < len(text) and text[end] != ' ':
            placeholder = placeholder + ' '

        text = text[:start] + placeholder + text[end:]
        
    return text



modified_text = replace_pii(text, result)
print(modified_text)

# Groq
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Repeat whatever i write next after fullstop." + modified_text,
        }
    ],
    model="llama3-8b-8192",
)


print(chat_completion.choices[0].message.content)
