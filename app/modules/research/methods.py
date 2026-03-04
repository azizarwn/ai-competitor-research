from app.modules.research.prompt import (
    GENERATE_REPORT_PROMPT,
    REPORT_SYSTEM_PROMPT,
    SEARCH_SYSTEM_PROMPT,
)
import json
from app.utils.client_tavily import tavily_client
from app.utils.client_oa import client
from app.modules.research.schema import QueriesSchema


def generate_queries(product_description: str) -> QueriesSchema:
    response = client.chat.completions.parse(
        model="google/gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful research assistant that generates 5 queries to research a given business idea.",
            },
            {
                "role": "user",
                "content": f"Generate 5 queries to research the following business idea: {product_description}",
            },
        ],
        response_format=QueriesSchema,
    )

    if response is None:
        raise ValueError("Failed to generate queries")

    return QueriesSchema(**response.choices[0].message.parsed.model_dump())  # type: ignore


def search_web(query: str) -> str:
    result = tavily_client.search(
        query=query, search_depth="advanced", include_raw_content="markdown"
    )

    response = client.chat.completions.create(
        model="deepseek/deepseek-v3.2",
        messages=[
            {
                "role": "system",
                "content": SEARCH_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"Query: {query}\n\nSearch Result: {json.dumps(result)}",
            },
        ],
        extra_body={"reasoning": {"enable": True}},
    )

    return response.choices[0].message.content  # type: ignore


def generate_report(product_description: str, research_context: str):
    response = client.chat.completions.create(
        model="deepseek/deepseek-v3.2",
        messages=[
            {
                "role": "system",
                "content": REPORT_SYSTEM_PROMPT.format(
                    research_context=research_context
                ),
            },
            {
                "role": "user",
                "content": GENERATE_REPORT_PROMPT.format(
                    product_description=product_description
                ),
            },
        ],
        extra_body={"reasoning": {"enable": True}},
    )
    return response.choices[0].message.content
