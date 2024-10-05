import os, warnings

warnings.filterwarnings("ignore")

from ..config import ModelType
from typing import Tuple, Union
from langchain_community.llms import VLLM
from langchain_community.llms import VLLMOpenAI
from langchain_openai import AzureChatOpenAI, ChatOpenAI, AzureOpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

#

from langchain_community.chat_models.azureml_endpoint import AzureMLChatOnlineEndpoint, AzureMLEndpointApiType, LlamaChatContentFormatter


class AzureConfig:
    API_VERSION = "2023-12-01-preview"
    API_KEY_EUS2 = "da5f7e6c846340ebb094bd9ecbd542e8"
    API_KEY_SC = "3bc8e8e74d1841dd98785b2d8b09ae9e"
    URL_SC = "https://regevlab-swedencentral-test.openai.azure.com/"
    URL_EUS2 = "https://regevlab-eastus2-test.openai.azure.com/"


class LlamaConfig:
    API_KEY_3_405B = "kOavVV8Bk9UEr8QvyHNK1DcbM9sJEjC9"
    URL_3_405B = "https://Meta-Llama-3-1-405B-Instruct-vex.eastus.models.ai.azure.com/v1/chat/completions"


def get_azure_config(model: ModelType) -> Tuple[str, str, str]:
    if model in [ModelType.GPT35TURBO, ModelType.GPT4, ModelType.GPT4O, ModelType.GPT4VISION, ModelType.TEXTEMBEDDING3LARGE, ModelType.TEXTEMBEDDINGADA002]:
        return AzureConfig.API_KEY_SC, AzureConfig.URL_SC, AzureConfig.API_VERSION
    elif model == ModelType.TEXTEMBEDDING3SMALL:
        return AzureConfig.API_KEY_EUS2, AzureConfig.URL_EUS2, AzureConfig.API_VERSION
    elif model == ModelType.LLAMA3_405B:
        return LlamaConfig.API_KEY_3_405B, LlamaConfig.URL_3_405B, None
    elif model == ModelType.CLAUDE3:
        return None, None, None
    elif "mistralai" in model.value or "llama" in model.value:
        return None, None, None
    else:
        raise ValueError(f"Model {model.value} not supported")


def make_llm(model: ModelType, temp: float = 0, streaming: bool = False, **kwargs) -> Union[VLLMOpenAI, AzureChatOpenAI, ChatOpenAI, AzureMLChatOnlineEndpoint]:
    if model == ModelType.GENIE:
        # ref: https://python.langchain.com/v0.2/docs/integrations/llms/vllm/
        # ref: https://api.python.langchain.com/en/latest/llms/langchain_community.llms.vllm.VLLMOpenAI.html
        return VLLMOpenAI(
            max_tokens=4000,
            temperature=temp,
            streaming=streaming,
            openai_api_key="spatialx-rocks",
            openai_api_base="http://localhost:8000/v1",
            callbacks=[StreamingStdOutCallbackHandler()],
            model_name=kwargs.get("model_name", "models/geniemodels.dev.gcs.gene.com/models_hf/Meta-Llama-3-8B-Instruct"),
        )
    api_key, url, api_version = get_azure_config(model)

    if model == ModelType.LLAMA3_405B:
        # ref: https://python.langchain.com/v0.2/docs/integrations/chat/llama_api/
        # llama = LlamaAPI(api_key)
        # return ChatLlamaAPI(
        #     client=llama,
        #     url=url,
        #     temp=temp,
        #     streaming=streaming,
        #     callbacks=[StreamingStdOutCallbackHandler()]
        #     )
        # return ChatOpenAI(
        #     openai_api_key=api_key,
        #     openai_api_version=api_version,
        #     openai_api_base=url,
        #     temperature=temp,
        #     max_tokens=4000,
        #     streaming=streaming,
        #     callbacks=[StreamingStdOutCallbackHandler()],
        # )

        # ref: https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/meta-llama-3.1/langchain.ipynb
        return AzureMLChatOnlineEndpoint(
            endpoint_url=url,
            endpoint_api_type=AzureMLEndpointApiType.serverless,
            endpoint_api_key=api_key,
            content_formatter=LlamaChatContentFormatter(),
            temperature=temp,
            streaming=streaming,
            callbacks=[StreamingStdOutCallbackHandler()],
            handle_parsing_errors=True,
        )
    elif model == ModelType.CLAUDE3:
        # ref: https://python.langchain.com/v0.2/docs/integrations/platforms/anthropic/
        from langchain_anthropic import ChatAnthropic
        os.environ["ANTHROPIC_API_KEY"] = "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"
        return ChatAnthropic(model="claude-3-opus-20240229")

    elif "mistral" in model.value or "llama" in model.value or "mosaicml" in model.value:
        return VLLM(
            max_tokens=5000,
            temperature=temp,
            streaming=streaming,
            callbacks=[StreamingStdOutCallbackHandler()],
            trust_remote_code=True,
            model=model.value,  # e.g., "mistralai/Mistral-7B-Instruct-v0.3"
            # model_kwargs={"stop": ["."]},
        )

    return AzureChatOpenAI(
        openai_api_key=api_key,
        azure_endpoint=url,
        azure_deployment=model.value,
        openai_api_version=api_version,
        temperature=temp,
        max_tokens=4000,
        streaming=streaming,
        callbacks=[StreamingStdOutCallbackHandler()],
    )


def make_llm_emb(emb_model: ModelType):
    if emb_model == ModelType.GENIE:
        raise NotImplementedError("Genie embeddings are not implemented")

    api_key, url, api_version = get_azure_config(emb_model)
    os.environ["AZURE_OPENAI_API_KEY"] = api_key

    return AzureOpenAIEmbeddings(
        azure_deployment=emb_model.value,
        azure_endpoint=url,
        openai_api_version=api_version,
        # chunk_size=1
    )


# GenieCookies = {
#     "PrescientAuth":
# }


# class GenieLLM:
#     def __init__(self, api_key, base_url, cookies):
#         self.httpx_client = httpx.Client(cookies=cookies)
#         self.client = OpenAI(
#             api_key=api_key,
#             base_url=base_url,
#             http_client=self.httpx_client,
#         )

#     def get_models(self):
#         return self.client.models.list().data

#     def create_completion(self, model, prompt, max_tokens=4000, temperature=0.7):
#         response = self.client.completions.create(model=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
#         return response.choices[0].text

#     def create_chat_completion(self, model, messages, max_tokens=4000, temperature=0.7):
#         response = self.client.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens, temperature=temperature)
#         return response.choices[0].message.content


# class GenieEmbeddings:
#     def __init__(self, api_key: str, base_url: str, emb_model: str, cookies: Dict[str, str]):
#         self.api_key = api_key
#         self.base_url = base_url
#         self.emb_model = emb_model
#         self.client = httpx.Client(cookies=cookies)

#     def get_embeddings(self, text: str) -> List[float]:
#         response = self.client.post(f"{self.base_url}/embeddings", headers={"Authorization": f"Bearer {self.api_key}"}, json={"model": self.emb_model, "input": text})
#         response.raise_for_status()
#         return response.json().get("data", [])[0].get("embedding", [])


if __name__ == "__main__":
    # Using the make_llm function for Genie
    genie_llm = make_llm("genie", temp=0)

    # Get available models
    models = genie_llm.get_models()
    print("Available models:", models)

    # Request completion from a model
    completion = genie_llm.create_completion(model=models[0]["id"], prompt="Once upon a time")
    print("Completion:", completion)

    # Request chat completion
    chat_completion = genie_llm.create_chat_completion(model=models[0]["id"], messages=[{"role": "user", "content": "Hello world!"}])
    print("Chat Completion:", chat_completion)
