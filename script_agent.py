from crewai import Agent,Task,Crew 
import os
from crewai_tools import FileReadTool
from dotenv import load_dotenv
load_dotenv()
from crewai import LLM
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_KEY")
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
) 
def script_agent():
    news_reader_tool = FileReadTool(file_path='news_full.txt')
    munna_circuit_agent = Agent(
        role="Script Writer",
        goal="Turn boring news into a hilarious Munna Bhai and Circuit conversation",
        backstory="""
    You are a Mumbai-based Bollywood scriptwriter deeply inspired by the Munna Bhai MBBS movie.
    You write conversations where Circuit is the clueless but loyal friend who asks questions, 
    and Munna Bhai responds in a street-smart, tapori, yet wise way.
    You use Mumbaiya Hindi written in Roman script, like 'apun', 'bole to', 'bhai', 'kya re buddhu' etc.
    """,
        tools=[news_reader_tool],
        allow_delegation=False,
        verbose=True,
        llm=llm
    )


    script_task = Task(
        description="Generate a one minute conversation between Munna and Circuit in tapori Hindi about the given news article.",
        expected_output="""
    Mumma: ...
    Circuit: ...
    Mumma: ...
    ... (one minute conversation in Hindi written in Roman script, funny and exaggerated)
    """,
        agent=munna_circuit_agent,
    )
    crew = Crew(
        agents=[munna_circuit_agent],   
        tasks=[script_task],
        llm=llm,
        verbose=True,
    )
    result = crew.kickoff()
    return result
if __name__ == "__main__":
    result = script_agent()
    print(result)
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(str(result))

    print("\n✅ Munna Bhai Script saved to script.txt!")
