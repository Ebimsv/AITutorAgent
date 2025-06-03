"""
Configuration settings for the AI Tutorial Agent.
"""

# Database Configuration
DATABASE_PATH = "tutorial_agent.db"

# LLM Configuration
LLM_MODEL = "meta-llama/llama-4-scout"
LLM_TEMPERATURE = 0.7
MAX_CONTEXT_MESSAGES = 5  # Number of previous messages to include for context

# Tutorial Generation Settings
TUTORIAL_LENGTH_TARGET = "300-500 words"
TUTORIAL_DIFFICULTY_LEVEL = "beginners to intermediate learners"

# Evaluation Settings
EVALUATION_QUESTION_FORMAT = "1-3 sentences"
MAX_EVALUATIONS_PER_SESSION = 10

# UI Configuration
STREAMLIT_PAGE_TITLE = "AI Tutorial Agent"
STREAMLIT_PAGE_ICON = "🤖"
STREAMLIT_LAYOUT = "wide"

# Response Templates
TUTORIAL_PROMPT_TEMPLATE = """You are an expert AI tutor. Create a comprehensive but concise tutorial about {subject}.

Structure your response as follows:
1. Brief introduction to the topic
2. Key concepts and definitions
3. Important examples
4. Common applications or use cases
5. Tips for further learning

Keep the tutorial engaging, educational, and appropriate for {difficulty_level}.
Use clear examples and explanations. Aim for about {length_target}."""

QUESTION_PROMPT_TEMPLATE = """You are an expert AI tutor teaching about {subject}.

Previous conversation context:
{context}

The student has asked: "{question}"

Provide a clear, detailed explanation that directly answers their question. Use examples where helpful.
Be encouraging and educational. If the question is off-topic, gently guide them back to {subject}."""

EVALUATION_PROMPT_TEMPLATE = """You are an expert AI tutor. Based on the tutorial content about {subject}, create a thoughtful evaluation question.

Tutorial content covered:
{content}

Create ONE evaluation question that:
1. Tests understanding of key concepts
2. Is neither too easy nor too difficult
3. Requires the student to demonstrate comprehension
4. Can be answered in {answer_format}

Format your response as:
QUESTION: [Your question here]

This is evaluation question #{question_number}."""

FEEDBACK_PROMPT_TEMPLATE = """You are an expert AI tutor evaluating a student's answer about {subject}.

Evaluation Question: {question}
Student's Answer: {answer}

Provide constructive feedback that:
1. Acknowledges what the student got right
2. Gently corrects any misconceptions
3. Provides additional clarification if needed
4. Encourages continued learning

Be supportive and educational. Rate their understanding and provide specific feedback."""

# Error Messages
ERROR_MESSAGES = {
    "api_error": "I apologize, but I encountered an error connecting to the AI service. Please try again.",
    "database_error": "There was an issue saving your conversation. Please try again.",
    "conversation_not_found": "I couldn't find that conversation. Please start a new tutorial or check the conversation ID.",
    "no_subject": "Please specify a subject you'd like to learn about.",
    "general_error": "Something went wrong. Please try again or contact support if the issue persists."
}

# Success Messages
SUCCESS_MESSAGES = {
    "tutorial_started": "Great! I've prepared a tutorial on {subject}. Let's start learning!",
    "conversation_loaded": "Welcome back! I've loaded your previous conversation about {subject}.",
    "evaluation_complete": "Well done! You're making good progress in understanding {subject}."
}

# Quick Action Buttons
QUICK_ACTIONS = [
    {
        "label": "📝 More Examples",
        "prompt": "Can you provide more examples?"
    },
    {
        "label": "🔍 Explain Further", 
        "prompt": "Can you explain this topic in more detail?"
    },
    {
        "label": "🎯 Real Applications",
        "prompt": "What are some real-world applications of this?"
    },
    {
        "label": "📚 Next Steps",
        "prompt": "What should I learn next?"
    }
]

# Example Subjects for the welcome screen
EXAMPLE_SUBJECTS = [
    "Python Programming",
    "Machine Learning", 
    "Data Science",
    "Web Development",
    "Statistics",
    "Linear Algebra",
    "Computer Networks",
    "Database Design",
    "API Development",
    "React.js",
    "Docker",
    "Git Version Control"
]

# Logging Configuration
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"
LOG_FILE = "tutorial_agent.log" 