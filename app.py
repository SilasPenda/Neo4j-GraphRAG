import os
from dotenv import load_dotenv
from langchain.graphs import Neo4jGraph
from langchain.prompts import PromptTemplate
from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_openai import ChatOpenAI
import streamlit as st

from templates import generate_template

load_dotenv()

url = os.getenv("url")
username = os.getenv("username")
password = os.getenv("password")
database = os.getenv("database")
os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(model_name="gpt-4o")
graph = Neo4jGraph(url=url, username=username, password=password, database=database)


def process(graph, llm, question):
    # Retrieve the graph schema
    schema = graph.get_schema
    template = generate_template(schema, question)

    question_prompt = PromptTemplate(
        template=template,
        input_variables=["schema", "question"]
    )

    qa = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        cypher_prompt=question_prompt,
        verbose=True,
        allow_dangerous_requests=True
    )

    result = qa.invoke({"query": question})["result"]

    return result


def main():

    st.title('Neo4j GraphRAG')
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    question = st.text_input("Ask question...")


    answer = process(graph, llm, question)

    st.write(answer)


if __name__ == "__main__":
    main()