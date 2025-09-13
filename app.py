import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

@app.post("/blogs")
async def create_blog(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return {"error": "Topic is required"}

    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    graph_builder = GraphBuilder(llm) 
    if topic:
        graph = graph_builder.setup_graph(usecase="blog")
        state = graph.invoke({"topic":topic})
    
    return {"data":state}

@app.post("/language_blogs")
async def create_language_blog(request: Request):
    data = await request.json()
    topic = data.get("topic")
    language= data.get("language")
    print(topic, language)
    if not topic or not language:
        return {"error": "Topic is required and language"}

    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    graph_builder = GraphBuilder(llm) 
    if topic and language:
        graph = graph_builder.setup_graph(usecase="language")
        state = graph.invoke({"topic":topic, "current_language":language})
    
    
    return {"data":state}


if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8000,reload=True)
