# InputTimeout Crew

The InputTimeout Crew project utilizes a multi-agent AI system powered by crewAI. The system comprises two agents: a Researcher and an Article Writer, working together and using a custom Google Search tool to perform Google-based research and generate a concise 300-word report on a given topic.

## How It Works

Google Research: The Researcher agent uses a custom Google search tool to gather research on the given topic. It retrieves the top 2 organic search links and feeds them to the Article Writer.
Report Creation: The Article Writer then synthesizes the gathered information into a well-structured 300-word report.

## Key Feature: InputTimeoutTool

One of the key innovations in this project is the custom InputTimeoutTool, which somehow replaces crewAI's default human_input=True feature. This tool has a default 10-second input timeout and prompts the user to provide feedback on the generated article before timeout. 

```python
class InputTimeoutTool(BaseTool):
    name: str = "Input Timeout Tool"
    description: str = "Tool for timing human input with a timeout mechanism"
    timeout_seconds: int = Field(default=10)

    def __init__(self, timeout_seconds: int = 10):
        super().__init__(timeout_seconds=timeout_seconds)
        self.timeout_seconds = timeout_seconds
```

But the users can set the timeout to their preference at the tool's configuration here: 

```python
@task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
            tools=[InputTimeoutTool(timeout_seconds=15)] 
        )
```

## Here’s how it works:

**Timeout Mechanism**: If the user doesn’t start typing within 10 seconds, the tool automatically approves the article as is and moves to the next task.
**User Feedback**: If the user starts typing during the timeout, the tool pauses the timeout and waits for feedback. Users can take as much time as needed to provide their input.
**Final Approval**: After the user provides feedback, they press Enter to forward it to the agent for inclusion in the final report. If no feedback is required, the user can simply press Enter within the timeout to approve the article.

This custom tool is crucial for improving workflow efficiency, especially for workflows where human input is necessary but typing inputs at every prompt can stall the workflow. This tool ensures the process doesn’t stall indefinitely while still allowing for user feedback when needed.

**Note**: As of now, they cannot coexist with the built-in human_input=True feature in CrewAI because if you bring in the built-in input taker it will stall the process again. 

**Star**: Dont forget to Star this repo if you find the tool impressive. 

