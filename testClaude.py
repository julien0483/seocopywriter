import anthropic

# Initialize the client
client = anthropic.Anthropic(
    api_key="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"  # You can omit this line if you set the environment variable
)

# Create a message
response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    system="You only speak arabic",
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)

print(response.content[0].text)
# Print the response content
