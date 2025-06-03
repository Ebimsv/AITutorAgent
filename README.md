# 🤖 AI Tutorial Agent

An interactive AI-powered tutoring system built with LangGraph that can teach users about any subject through structured tutorials, Q&A sessions, and knowledge evaluation.

## 🌟 Features

### Core Functionality
- **📚 Subject Learning**: Generate comprehensive tutorials on any topic
- **💬 Interactive Q&A**: Ask follow-up questions and get detailed explanations
- **🧠 Knowledge Testing**: Automated evaluation questions to test understanding
- **💾 Conversation Persistence**: All interactions saved to SQLite database
- **🌐 Web Interface**: Beautiful Streamlit UI for easy interaction
- **🖥️ CLI Interface**: Command-line option for quick testing

### Technical Features
- **LangGraph Orchestration**: Sophisticated agent workflow management
- **State Management**: Maintains conversation context and learning progress
- **Database Integration**: SQLite for reliable data persistence
- **Error Handling**: Robust error management throughout the system
- **Modular Design**: Clean, maintainable code structure

## 🚀 Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone git@github.com:Ebimsv/AITutorAgent.git
cd AITutorAgent
pip install -r requirements.txt
```

### 2. Configuration

The system uses your existing OpenRouter API configuration from `LLM_api.py`. Make sure your API key is properly set up.

### 3. Run the Application

#### Streamlit Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```

#### Command Line Interface
```bash
python cli_demo.py
```

## 📖 Usage Examples

### Web Interface
1. Open the Streamlit app in your browser
2. Enter a subject in the sidebar (e.g., "Python functions")
3. Click "Start Tutorial" to begin learning
4. Ask questions in the chat interface
5. Use "Test Me" button for evaluation questions

### CLI Interface
```bash
# Start the CLI
python cli_demo.py

# Commands available:
> learn Python functions        # Start a new tutorial
> Can you explain parameters?   # Ask questions
> test                         # Request evaluation
> history                     # View past sessions
> quit                        # Exit
```

## 🏗️ Project Structure

```
AI-tutor/
├── cli_demo.py          # Command-line interface
├── config.py            
├── database.py          # SQLite database operations
├── LLM_api.py           # OpenRouter API configuration
├── streamlit_app.py      # Main Streamlit web interface
├── tutorial_agent.py     # LangGraph agent implementation
├── requirements.txt     # Python dependencies
└── README.md          
```

## 🔧 Architecture

### LangGraph Workflow
The tutorial agent uses LangGraph to manage conversation flow:

1. **Tutorial Generation**: Creates initial educational content
2. **Question Handling**: Processes user questions with context
3. **Evaluation Creation**: Generates testing questions
4. **Answer Evaluation**: Provides feedback on user responses

### Database Schema
```sql
conversations:
- id (PRIMARY KEY)
- session_id (TEXT)
- subject (TEXT)
- created_at (TIMESTAMP)

messages:
- id (PRIMARY KEY)
- conversation_id (FOREIGN KEY)
- role (TEXT: 'user' | 'assistant')
- content (TEXT)
- message_type (TEXT: 'tutorial' | 'question' | 'answer' | 'evaluation_question' | 'evaluation_answer' | 'evaluation_feedback')
- timestamp (TIMESTAMP)
```

## 💡 Example Interaction Flow

```
User: "I want to learn about Python functions"

Agent: [Generates comprehensive tutorial covering:
        - Introduction to functions
        - Syntax and parameters
        - Return values
        - Examples and use cases]

User: "Can you explain parameters in more detail?"

Agent: [Provides detailed explanation of:
        - Positional parameters
        - Keyword parameters
        - Default values
        - *args and **kwargs]

Agent: "Let me test your understanding: What's the difference 
        between positional and keyword arguments?"

User: [Provides answer]

Agent: [Evaluates response and provides constructive feedback]
```

## 🎯 Core Components

### TutorialAgent Class
- **LangGraph Integration**: Manages conversation workflow
- **Context Management**: Maintains conversation state
- **API Integration**: Handles LLM calls with error handling
- **Database Operations**: Stores and retrieves conversation data

### TutorialDatabase Class
- **SQLite Operations**: Database creation and management
- **Data Persistence**: Conversation and message storage
- **Query Methods**: Retrieve conversation history and sessions

### Streamlit Interface
- **User Experience**: Intuitive web interface
- **Session Management**: Handle multiple concurrent users
- **Real-time Updates**: Dynamic conversation display
- **Quick Actions**: Pre-built interaction buttons

## 🛠️ Customization

### Adding New Question Types
To add new types of interactions, modify the `tutorial_agent.py`:

```python
def _handle_custom_interaction(self, state: TutorialState) -> TutorialState:
    # Your custom logic here
    pass
```

### Modifying Tutorial Structure
Update the tutorial generation prompt in `_generate_tutorial()` method:

```python
prompt = f"""Create a tutorial about {subject} with:
1. Your custom structure
2. Specific requirements
3. Desired format
"""
```

### Database Extensions
Add new tables or fields by modifying `database.py`:

```python
def init_database(self):
    # Add your custom tables here
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS custom_table (
            id INTEGER PRIMARY KEY,
            custom_field TEXT
        )
    ''')
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Database Issues**
   - Delete `tutorial_agent.db` file to reset database
   - Check file permissions in the project directory

3. **API Errors**
   - Verify your OpenRouter API key in `LLM_api.py`
   - Check internet connection and API quota

4. **Streamlit Issues**
   ```bash
   streamlit cache clear
   streamlit run streamlit_app.py --server.port 8501
   ```

## 📊 Features in Detail

### Tutorial Generation
- Structured content creation
- Beginner to intermediate level adaptation
- Multiple learning styles support
- Context-aware explanations

### Interactive Q&A
- Natural language processing
- Context retention across conversation
- Off-topic detection and redirection
- Encouraging and educational responses

### Knowledge Evaluation
- Adaptive difficulty levels
- Constructive feedback system
- Understanding assessment
- Progress tracking

### Data Persistence
- Complete conversation history
- Session management
- Cross-session continuity
- Export capabilities

## 🚦 Getting Started Tips

1. **First Time Users**: Start with simple subjects like "basic math" or "Python basics"
2. **Best Practices**: Ask specific questions for better responses
3. **Evaluation**: Use the "Test Me" feature regularly to reinforce learning
4. **Navigation**: Use the sidebar to manage multiple learning sessions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🎓 Educational Use

This AI Tutorial Agent is designed for:
- **Students**: Supplementary learning support
- **Educators**: Teaching assistant tool
- **Self-learners**: Independent study aid
- **Developers**: Code learning and review

## 🔮 Future Enhancements

Potential improvements and features:
- Multi-language support
- Voice interaction capabilities
- Advanced progress analytics
- Integration with learning management systems
- Collaborative learning features
- Mobile application development

---
