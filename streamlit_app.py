import streamlit as st
import uuid
from datetime import datetime
from tutorial_agent import TutorialAgent
from database import TutorialDatabase

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Tutorial Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "agent" not in st.session_state:
    st.session_state.agent = TutorialAgent()

if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "subject" not in st.session_state:
    st.session_state.subject = ""

if "selected_example_subject" not in st.session_state:
    st.session_state.selected_example_subject = ""

if "quick_action_message" not in st.session_state:
    st.session_state.quick_action_message = ""

def start_new_tutorial(subject_override=None):
    """Start a new tutorial session."""
    # Use override subject if provided, otherwise get from input
    subject = subject_override if subject_override else st.session_state.get("new_subject_input", "")
    
    if subject and subject.strip():
        try:
            # Start new tutorial
            result = st.session_state.agent.start_tutorial(
                st.session_state.session_id, 
                subject.strip()
            )
            
            # Update session state
            st.session_state.current_conversation_id = result["conversation_id"]
            st.session_state.subject = subject.strip()
            st.session_state.chat_history = [
                {"role": "assistant", "content": result["response"], "type": "tutorial"}
            ]
            
            # Clear any stored example subject
            st.session_state.selected_example_subject = ""
            
            st.success(f"Started tutorial on: {subject}")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error starting tutorial: {str(e)}")

def send_message(message_override=None):
    """Send a user message and get AI response."""
    # Use override message if provided, otherwise get from input
    user_input = message_override if message_override else st.session_state.get("user_input", "")
    
    if user_input and user_input.strip() and st.session_state.current_conversation_id:
        try:
            # Determine input type
            input_type = "question"
            if "test me" in user_input.lower() or "quiz" in user_input.lower() or "evaluate" in user_input.lower():
                input_type = "evaluation_request"
            
            # Get AI response
            result = st.session_state.agent.continue_conversation(
                st.session_state.current_conversation_id,
                user_input.strip(),
                input_type
            )
            
            # Update chat history
            st.session_state.chat_history.append({
                "role": "user", 
                "content": user_input.strip(),
                "type": "message"
            })
            
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": result["response"],
                "type": "response"
            })
            
            # Clear quick action message if it was used
            if message_override:
                st.session_state.quick_action_message = ""
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error processing message: {str(e)}")

def load_conversation(conversation_id: int):
    """Load a previous conversation."""
    try:
        db = TutorialDatabase()
        history = db.get_conversation_history(conversation_id)
        
        # Get conversation subject
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT subject FROM conversations WHERE id = ?", (conversation_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            st.session_state.current_conversation_id = conversation_id
            st.session_state.subject = result[0]
            st.session_state.chat_history = []
            
            # Convert database history to chat format
            for msg in history:
                role = msg["role"]
                content = msg["content"]
                msg_type = msg.get("message_type", "message")
                
                st.session_state.chat_history.append({
                    "role": role,
                    "content": content,
                    "type": msg_type
                })
            
            st.success(f"Loaded conversation about: {result[0]}")
            st.rerun()
        
    except Exception as e:
        st.error(f"Error loading conversation: {str(e)}")

def main():
    """Main Streamlit application."""
    
    # Check if an example subject was selected
    if st.session_state.selected_example_subject:
        start_new_tutorial(st.session_state.selected_example_subject)
        return
    
    # Check if a quick action was triggered
    if st.session_state.quick_action_message:
        send_message(st.session_state.quick_action_message)
        return
    
    # Header
    st.title("🤖 AI Tutorial Agent")
    st.markdown("**Learn any subject with interactive AI tutoring!**")
    
    # Sidebar for conversation management
    with st.sidebar:
        st.header("📚 Tutorial Sessions")
        
        # New tutorial section
        st.subheader("Start New Tutorial")
        new_subject = st.text_input(
            "What would you like to learn about?",
            placeholder="e.g., Python functions, Machine Learning, History of Rome...",
            key="new_subject_input"
        )
        
        if st.button("Start Tutorial", type="primary"):
            start_new_tutorial()
        
        # Previous conversations
        st.subheader("📜 Previous Sessions")
        try:
            db = TutorialDatabase()
            conversations = db.get_conversations_by_session(st.session_state.session_id)
            
            if conversations:
                for conv in conversations:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(
                            f"{conv['subject'][:30]}...",
                            key=f"load_{conv['id']}",
                            help=f"Created: {conv['created_at']}"
                        ):
                            load_conversation(conv['id'])
                    
                    with col2:
                        st.caption(f"{conv['created_at'][:10]}")
            else:
                st.info("No previous sessions found.")
                
        except Exception as e:
            st.error(f"Error loading conversations: {str(e)}")
        
        # Help section
        st.subheader("💡 How to Use")
        st.markdown("""
        1. **Start a Tutorial**: Enter any subject you want to learn
        2. **Ask Questions**: Ask follow-up questions about the material
        3. **Get Evaluated**: Say "test me" or "quiz me" for practice questions
        4. **Review History**: Access previous learning sessions
        """)
    
    # Main chat area
    if st.session_state.current_conversation_id:
        st.subheader(f"📖 Learning: {st.session_state.subject}")
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display chat history
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant"):
                        # Add icons based on message type
                        if message.get("type") == "tutorial":
                            st.markdown("### 📚 Tutorial Content")
                        elif message.get("type") == "evaluation_question":
                            st.markdown("### 🤔 Quick Check")
                        elif message.get("type") == "evaluation_feedback":
                            st.markdown("### ✅ Feedback")
                        
                        st.write(message["content"])
        
        # User input
        st.markdown("---")
        col1, col2, col3 = st.columns([6, 1, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask a question or request evaluation:",
                placeholder="e.g., Can you explain this in more detail? or Test my understanding!",
                key="user_input"
            )
        
        with col2:
            if st.button("Send 💬"):
                send_message()
        
        with col3:
            if st.button("Test Me 🧠"):
                if st.session_state.current_conversation_id:
                    st.session_state.quick_action_message = "Please test my understanding with a question."
                    st.rerun()
        
        # Quick action buttons
        st.markdown("### Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📝 More Examples"):
                st.session_state.quick_action_message = "Can you provide more examples?"
                st.rerun()
        
        with col2:
            if st.button("🔍 Explain Further"):
                st.session_state.quick_action_message = "Can you explain this topic in more detail?"
                st.rerun()
        
        with col3:
            if st.button("🎯 Real Applications"):
                st.session_state.quick_action_message = "What are some real-world applications of this?"
                st.rerun()
        
        with col4:
            if st.button("📚 Next Steps"):
                st.session_state.quick_action_message = "What should I learn next?"
                st.rerun()
    
    else:
        # Welcome screen
        st.markdown("## Welcome to the AI Tutorial Agent! 🚀")
        st.markdown("""
        This intelligent tutoring system will help you learn any subject through:
        
        - **📖 Comprehensive Tutorials**: Get structured explanations on any topic
        - **💬 Interactive Q&A**: Ask questions and get detailed answers
        - **🧠 Knowledge Testing**: Practice with evaluation questions
        - **📊 Progress Tracking**: Keep track of your learning journey
        
        **To get started**, enter a subject you'd like to learn about in the sidebar!
        """)
        
        # Example subjects
        st.markdown("### 💡 Popular Learning Topics")
        st.markdown("*Click any topic below to start learning immediately:*")
        
        example_subjects = [
            "Python Programming", "Machine Learning", "Data Science",
            "Web Development", "Statistics", "Linear Algebra",
            "Computer Networks", "Database Design", "API Development",
            "React.js", "Docker", "Git Version Control"
        ]
        
        # Create a grid of buttons using columns
        cols = st.columns(3)
        for i, subject in enumerate(example_subjects):
            col_idx = i % 3
            with cols[col_idx]:
                if st.button(f"📚 {subject}", key=f"example_{i}", use_container_width=True):
                    st.session_state.selected_example_subject = subject
                    st.rerun()

if __name__ == "__main__":
    main() 