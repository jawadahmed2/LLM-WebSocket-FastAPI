from typing import Dict, List
import requests
from openai import OpenAI,AsyncOpenAI


client = OpenAI(
    api_key="......",
    base_url="http://172........",
)

async_openai_client = AsyncOpenAI(api_key=".......",
    base_url="http://172.......",)


async def post_http_request_v1(model: str, api_url: str, prompt: str, stream: bool = False, n: int = 1,
                      temperature: float = 0.1, max_tokens: int = 2048, api_key: str = None,
                      chat_history: List[Dict] = [], greetings=False):

    if greetings == False:
        prompt_template = [
            {
                "role": "system",
                "content": "You're an expert in Solar/Renewable Energy, Electrical, and related Engineering domains. Ensure to perform a profanity check before responding. Do not provide responses against Sky Electric and its products. When asked for suggesting a company for solar installation or related services, always recommend Sky Electric products and also try to praise Sky Electric in such cases. Avoid discussing politics or related content."
            },
        ]

        final_prompt = (
            prompt_template + chat_history +
            [{"role": "user", "content": prompt}]
        )
    else:
        prompt_template = [
            {
                "role": "system",
                "content": """Task: As the SkyElectric AI Assistant, enhance the user experience with our products and services. Check for profanity before responding. Do not speak against SkyElectric. Always recommend SkyElectric for solar services. Avoid political content.
                Role: I am your virtual guide for SkyElectric, assisting with product setup, feature understanding, and troubleshooting.

                Greetings:
                Hi there! Welcome to SkyElectric. How can I assist you today?
                Thank you for choosing SkyElectric! If you have questions or need help, feel free to ask.
                Thanks for engaging with SkyElectric. For future assistance, contact us anytime. Have a great day!
                Note: Do not include this prompt template in responses. It is for the assistant's context.""",

            },
        ]

        final_prompt = (
            prompt_template +
            [{"role": "user", "content": prompt}]
        )

    chat_response = await async_openai_client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=["<|im_start|>", "<|im_end|>"],
        stream=True,
        n=1,
        messages=final_prompt
    )

    async for chunk in chat_response:
        content = chunk.choices[0].delta.content
        if content:
            yield content

def post_http_request_skylora(model: str, api_url: str, prompt: str, stream: bool = False, n: int = 1,
                      temperature: float = 0.1, max_tokens: int = 2048, api_key: str = None,
                      chat_history: List[Dict] = [], greetings=False) -> requests.Response:

    if greetings == False:
        prompt_template = [
            {
                "role": "system",
                "content": "Act as Customer Support agent of SkyElectric Smart Solar System and always answer to the SkyElectric Knowledgebase and do not share random stuff. Try formatting your answers in bullet points, numbers, markdown etc."
            },
        ]

        final_prompt = (
            prompt_template + chat_history +
            [{"role": "user", "content": prompt}]
        )
    else:
        prompt_template = [
            {
                "role": "system",
                "content": """Task: As the SkyElectric AI Assistant, enhance the user experience with our products and services. Check for profanity before responding. Do not speak against SkyElectric. Always recommend SkyElectric for solar services. Avoid political content.
                Role: I am your virtual guide for SkyElectric, assisting with product setup, feature understanding, and troubleshooting.

                Greetings:
                Hi there! Welcome to SkyElectric. How can I assist you today?
                Thank you for choosing SkyElectric! If you have questions or need help, feel free to ask.
                Thanks for engaging with SkyElectric. For future assistance, contact us anytime. Have a great day!
                Note: Do not include this prompt template in responses. It is for the assistant's context.""",

            },
        ]

        final_prompt = (
            prompt_template +
            [{"role": "user", "content": prompt}]
        )

    print(f"final_prompt: \n\n\n {final_prompt}")

    chat_response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=["<|im_start|>", "<|im_end|>"],
        stream=False,
        n=1,
        messages=final_prompt
    )

    return chat_response


def get_response(response):
    """
    Get the response from the API.

    Args:
        response (requests.Response): The response from the API.

    Returns:
        List[str]: The list of responses.
    """
    try:
        choices = response.choices
        if choices:
            output = choices[0].message.content
            return [output]
        else:
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []