from markdown import markdown
from app.modules.research.methods import generate_queries, search_web, generate_report
from weasyprint import HTML
from app.celery_app import celery_app


def research(product_description: str):
    research_context = ""
    queries = generate_queries(product_description)
    print(queries.queries)

    for query in queries.queries:
        result = search_web(query)
        research_context += f"Query : {query} \n\n\n Result : {result}"

    print(research_context)
    # with open("research.txt", "w") as f:
    #     f.write(research_context)

    research_result = generate_report(product_description, research_context)
    if not research_result:
        raise ValueError("Research not found")

    result = markdown(research_result)
    HTML(string=result).write_pdf("research.pdf")


@celery_app.task(name="app.modules.research.task.research_task")  # explicit name
def research_task(product_description):
    research(product_description)
