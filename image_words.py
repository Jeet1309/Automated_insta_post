from crewai import Agent, Task, Crew
import os
from crewai_tools import FileReadTool
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_KEY")

# Define LLM
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

# Define the main agent logic
def image_word():
    script_reader_tool = FileReadTool(file_path='script.txt')

    word_extractor = Agent(
        role="Important Word Extractor for Visual Content",
        goal=(
            "Extract one visually meaningful and unique word per line from a tapori Hindi conversation. "
            "These words will be used to search for related images and generate an Instagram-style video."
        ),
        backstory=(
            "You are a creative NLP assistant helping a content creator build short videos for social media. "
            "Given a tapori-style conversation, your job is to pick the most image-relevant, eye-catching word from each line. "
            "These words will be used to scrape images online and create an engaging visual story on Instagram. "
            "Choose nouns or objects over fillers and focus on words that would have a strong visual identity."
        ),
        tools=[script_reader_tool],
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    script_task = Task(
        description="Use the script reading tool and extract one important word from each line in the conversation script. Format output like:\nimportant_word : line_1_word\nimportant_word : line_2_word...",
        expected_output="""a dictonary with keys as important words and values as the corresponding lines, 
                            e.g., {
                            "airport": "Line 3: He rushed to the airport to catch his flight.",
                            "reporter": "Line 5: The reporter asked difficult questions."
                            }""",
        agent=word_extractor,
    )

    crew = Crew(
        agents=[word_extractor],
        tasks=[script_task],
        llm=llm,
        verbose=True,
    )

    result = crew.kickoff()
    return result

# Save output to file
if __name__ == "__main__":
    result = image_word()  # <-- FIXED: was calling undefined 'script_agent'
    
    # Ensure result is a string
    with open("extracted_words.txt", "w", encoding="utf-8") as f:
        f.write(str(result))

    print("\n✅ Extracted words saved to extracted_words.txt!")
