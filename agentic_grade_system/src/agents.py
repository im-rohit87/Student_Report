from crewai import Agent

file_agent = Agent(
    role="Quiz File Monitor",
    goal="Detect and validate new quiz files",
    backstory="Expert in file management",
    verbose=True,
    allow_delegation=False
)

data_agent = Agent(
    role="Data Processor",
    goal="Merge student quiz records",
    backstory="Expert in pandas data processing",
    verbose=True
)

analysis_agent = Agent(
    role="Performance Analyst",
    goal="Calculate rank, percentile and grades",
    backstory="Expert statistician",
    verbose=True
)

feedback_agent = Agent(
    role="Student Mentor",
    goal="Generate personalized feedback",
    backstory="Educational performance coach",
    verbose=True
)

email_agent = Agent(
    role="Email Manager",
    goal="Send reports to students",
    backstory="Communication specialist",
    verbose=True
)