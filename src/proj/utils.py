import json

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI


def process_paragraph(paragraph_text: str | list) -> str:
    """
    Given a paragraph, it returned the same text without any leading or trailing
    whitespaces, and joins the lines (separated with single or multiple newline
    characters) with a single space.
    """
    if isinstance(paragraph_text, list):
        paragraph_text = " ".join(paragraph_text)

    return " ".join(paragraph_text.strip().split())


def llm_pairwise(
    paragraph0: str,
    paragraph1: str,
    manuscript_section: str,
    model_name: str = "mistral:7b-instruct-fp16",
    model_params: dict = {},
    max_attemps: int = 3,
    verbose: bool = False,
) -> dict:
    default_model_kwargs = {
        "temperature": model_params.get("temperature", 0.5),
        "max_tokens": model_params.get("max_tokens", 2000),
        "model_kwargs": model_params.get("model_kwargs", {}),
    }

    if model_name.startswith("openai:"):
        params = {
            "model_name": model_name[7:],
            **default_model_kwargs,
        }
        model = ChatOpenAI(**params)
    else:
        params = {
            "model": model_name,
            **default_model_kwargs,
        }
        model = ChatOllama(**params)

    section_part = f"a paragraph from the {manuscript_section.capitalize()} section"
    if manuscript_section.lower() == "abstract":
        section_part = "the Abstract"

    system_message = f"You are an expert copyeditor with ample experience in scientific writing. You are assessing the quality of two versions of {section_part} of a scientific article."
    comment_on_paragraph_prompt = "Read the following paragraph and write a list with your comments on the following areas: 1) has a clear sentence structure, 2) is easy to follow, 3) is correct in grammar, 4) has no spelling errors, 5) potential areas of improvement.\n\n{text}"
    judge_prompt = 'Act as an impartial judge and evaluate the quality of Paragraph 1 and Paragraph A, which are two versions of an Abstract of a scientific manuscript. Your evaluation should consider whether the text has a clear sentence structure, is easy to follow, is correct in grammar, and has no spelling errors. Compare the two versions and select the best only if one of them is clearly better than the other; if both versions are essentially similar, then it is a tie. Be as objective as possible. Provide the output in JSON format with the following schema: {"best": string, "rationale": string}, where "best" can have values of "Paragraph 1", "Paragraph A", or "tie".'

    messages = [
        comment_on_paragraph_prompt.format(text=f"Paragraph A: {paragraph0}"),
        comment_on_paragraph_prompt.format(text=f"Paragraph 1: {paragraph1}"),
        judge_prompt,
    ]

    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_message),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation = LLMChain(
        llm=model,
        prompt=prompt,
        verbose=verbose,
        memory=memory,
    )

    t = None
    t_json_obj = None
    count = 0
    while t is None and count < max_attemps:
        responses = []

        try:
            for m in messages:
                if isinstance(model, ChatOpenAI):
                    if "JSON" in m:
                        model.model_kwargs["response_format"] = {"type": "json_object"}
                    elif "response_format" in model.model_kwargs:
                        del model.model_kwargs["response_format"]
                elif isinstance(model, ChatOllama):
                    if "JSON" in m:
                        model.format = "json"
                    else:
                        model.format = None

                r = conversation.invoke({"question": m})
                responses.append(r["text"])

            t = (
                responses[-1]
                .strip()
                .replace(": True", ": true")
                .replace(": False", ": false")
            )

            # try to capture a JSON substring
            # tjson = JSON_REGEX.search(t)
            # if tjson:
            #     t = tjson.group(0)

            t_json_obj = json.loads(t)
        except json.JSONDecodeError:
            t = None
            t_json_obj = None
        finally:
            count += 1

    assert (
        t_json_obj is not None
    ), f"Failed to get a response from the chatbot ({count} attempts)"

    return t_json_obj