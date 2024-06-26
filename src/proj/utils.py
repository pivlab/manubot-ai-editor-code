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


def simplify_filename(filename: str) -> str:
    """
    Given a filename, it returns a simplified version of it by removing
    special characters and spaces, and converting it to lowercase.
    """
    return "".join(
        c if c.isalnum() or c in ("-", ".") else "_" for c in filename.lower()
    )


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
    model_params: dict = None,
    max_attemps: int = 3,
    throw_if_failed: bool = True,
    verbose: bool = False,
) -> dict:
    if model_params is None:
        model_params = {}

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
    elif model_name.startswith("ollama:"):
        params = {
            "model": model_name[7:],
            **default_model_kwargs,
        }
        model = ChatOllama(**params)
    else:
        raise ValueError(f"Invalid or unsupported model name: {model_name}")

    par0_id = "Paragraph A"
    par1_id = "Paragraph 1"

    section_part = f"the {manuscript_section.capitalize()} section"
    if manuscript_section.lower() == "abstract":
        section_part = "the Abstract"

    system_message = f"You are an expert copyeditor with ample experience in scientific writing. You are assessing the quality of two versions of a paragraph from {section_part} of a scientific article."
    comment_on_paragraph_prompt = "Evaluate the quality of the following paragraph by writing a list with positive (if any) and/or negative (if any) aspects on the following areas: 1) has a clear sentence structure, 2) is easy to follow, 3) is correct in grammar, 4) has no spelling errors.\n\n{text}"
    judge_prompt = (
        'Now, act as an impartial judge and evaluate the quality of these two paragraphs. Your evaluation must only consider the previous areas you commented on above. Compare the two versions and select the best only if one of them is clearly better than the other; if both versions are similar, then it is a tie. Avoid any position biases and ensure that the order in which the paragraphs were presented does not influence your decision. Do not favor certain paragraph identifiers. Be as objective as possible. Provide the output in JSON format with the following schema: {"best": string, "rationale": string}, where "best" can only have the following values: '
        + f'"{par0_id}", "{par1_id}", or "tie".'
    )

    messages = [
        comment_on_paragraph_prompt.format(text=f"{par0_id}: {paragraph0}"),
        comment_on_paragraph_prompt.format(text=f"{par1_id}: {paragraph1}"),
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
                if isinstance(model, ChatOpenAI) and "turbo" in model.model_name:
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

            t = responses[-1].strip()

            t_json_obj = json.loads(t)
        except json.JSONDecodeError:
            t = None
            t_json_obj = None
        finally:
            count += 1

    if throw_if_failed:
        assert (
            t_json_obj is not None
        ), f"Failed to get a response from the chatbot ({count} attempts)"
    else:
        if t_json_obj is None:
            t_json_obj = {
                "best": "Failed",
                "rationale": "Failed to get a response from the chatbot",
            }

    return t_json_obj
