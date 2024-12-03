#!/usr/bin/env python
import sys
from .crew import InputTimeoutCrew 

def run():
    """
    Run the content research crew.
    """
    print("Initializing Content Research Crew...")  
    crew = InputTimeoutCrew()

    # Define the inputs you want to provide to the crew's tasks or agents
    inputs = {
        "topic": "Bitcoin"  
    }

    # Kick off the crew's tasks and pass the inputs
    response = crew.crew().kickoff(inputs=inputs)  
    return {"response": response}

if __name__ == "__main__":
    run()
