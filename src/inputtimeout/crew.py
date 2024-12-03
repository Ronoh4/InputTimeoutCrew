from crewai.project import CrewBase, agent, crew, task
from crewai import Agent, Crew, Process, Task
from .tools.input_timeout_tool import InputTimeoutTool
from .tools.google_search_tool import OrganicSearchTool
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv
import os

load_dotenv()
serper_api_key = os.getenv('SERPER_API_KEY')

@CrewBase
class InputTimeoutCrew:
    @agent
    def topic_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['topic_researcher'],
            tools=[OrganicSearchTool(), ScrapeWebsiteTool()],
            verbose=True,
            llm="openai/gpt-4o-mini" 
        )

    @agent
    def article_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['article_writer'],
            verbose=True,
            llm="openai/gpt-4o-mini"  
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
            tools=[InputTimeoutTool(timeout_seconds=15)] 
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  
            verbose=True,
        )
