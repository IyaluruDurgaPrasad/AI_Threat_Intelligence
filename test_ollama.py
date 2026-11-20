from ollama  import chat
print('connecting to Ollama....')

try:
    response=chat(
        model='llama3.2',
        messages=[
            {
                'role':'system',
                'content':(
                     "You are a cybersecurity threat intelligence analyst. "
                    "Analyze suspicious messages for defensive purposes. "
                    "Identify potential threats and recommend precautions."             
                )
            },
            {
                "role": "user",
                "content": """
                Analyze this suspicious email:

                Your bank account has been suspended.
                Click the link immediately and enter
                your password.

                Identify:
                1. Threat type
                2. Risk level
                3. Suspicious indicators
                4. Security recommendations
                """
            }
        ]
    )

    print('\n ------- AI Threat Analysis -----------\n')
    print(response.message.content)
    print('\n Ollama Python Integration successful!')

except Exception as e:
    print('Error:', e)