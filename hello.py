import os, time
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

load_dotenv()  # reads .env and puts the keys into environment variables

models = {
    "Claude": ChatAnthropic(model="claude-haiku-5-5"),
    "GPT": ChatOpenAI(model=os.environ["OPENAI_MODEL"]),
}

for name, llm in models.items():
    start = time.time()
    reply = llm.invoke("In one sentence, what is retrieval-augmented generation?")
    print(f"{name} ({time.time() - start:.1f}s): {reply.text}")
