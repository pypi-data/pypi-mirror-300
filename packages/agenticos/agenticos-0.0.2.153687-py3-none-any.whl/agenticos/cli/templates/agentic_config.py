from agenticos.node.models import AgenticConfig, Workflow

workflows : dict[Workflow] = {}

# Example workflow
# Import the Crew class. If you used the flow from CrewAI docs the following import should work
from {{folder_name}}.crew import {{class_name}}Crew as Crew

my_crew = Crew()

# Define the workflow name
my_workflow_name = "research_and_report"

# Define the workflow
workflows[my_workflow_name] = Workflow(
    # Name of the workflow
    name=my_workflow_name,
    # Description of the workflow
    description="This workflow will research and report on a given topic",
    # Inputs of the workflow. This is what you pass to Crew.kickoff function
    inputs={"topic": "The topic to research and report on"},
    # Pass the kickoff function of the crew. It has to accept dict of inputs
    kickoff_function=my_crew.crew().kickoff,
    # This function will be called to get the output of the workflow
    # Usually it will be the output of the last task in the workflow
    output_function=lambda: my_crew.reporting_task().output.raw
    )

config = AgenticConfig(name="Test Node", workflows=workflows)
