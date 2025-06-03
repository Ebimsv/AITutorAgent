#!/usr/bin/env python3
"""
Simple command-line interface for testing the AI Tutorial Agent.
"""

import uuid
from tutorial_agent import TutorialAgent
from database import TutorialDatabase

class CLITutorialDemo:
    """Command-line interface for the tutorial agent."""
    
    def __init__(self):
        self.agent = TutorialAgent()
        self.session_id = str(uuid.uuid4())
        self.current_conversation_id = None
        self.subject = ""
    
    def run(self):
        """Main CLI loop."""
        print("🤖 AI Tutorial Agent - Command Line Interface")
        print("=" * 50)
        print("Type 'help' for commands or 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Happy learning!")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                elif user_input.lower().startswith('learn '):
                    subject = user_input[6:].strip()
                    self.start_tutorial(subject)
                elif user_input.lower() == 'history':
                    self.show_history()
                elif user_input.lower().startswith('load '):
                    conv_id = user_input[5:].strip()
                    self.load_conversation(conv_id)
                elif user_input.lower() in ['test', 'quiz', 'evaluate']:
                    self.request_evaluation()
                elif self.current_conversation_id and user_input:
                    self.ask_question(user_input)
                elif not user_input:
                    continue
                else:
                    print("❌ Please start a tutorial first with 'learn <subject>' or type 'help'")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def show_help(self):
        """Show help information."""
        print("\n📚 Available Commands:")
        print("  learn <subject>  - Start a new tutorial (e.g., 'learn Python functions')")
        print("  test/quiz        - Request an evaluation question")
        print("  history          - Show previous learning sessions")
        print("  load <id>        - Load a previous conversation by ID")
        print("  help             - Show this help message")
        print("  quit/exit/q      - Exit the program")
        print("\nDuring a tutorial session:")
        print("  Just type your questions naturally!")
        print("  Examples: 'Can you explain this further?', 'Show me more examples'\n")
    
    def start_tutorial(self, subject: str):
        """Start a new tutorial session."""
        if not subject:
            print("❌ Please specify a subject to learn about.")
            return
        
        try:
            print(f"🚀 Starting tutorial on: {subject}")
            print("⏳ Generating tutorial content...\n")
            
            result = self.agent.start_tutorial(self.session_id, subject)
            
            self.current_conversation_id = result["conversation_id"]
            self.subject = subject
            
            print("🤖 AI Tutor:")
            print("=" * 40)
            print(result["response"])
            print("=" * 40)
            print("\n💬 You can now ask questions or type 'test' for evaluation!\n")
            
        except Exception as e:
            print(f"❌ Error starting tutorial: {str(e)}")
    
    def ask_question(self, question: str):
        """Ask a question about the current tutorial."""
        try:
            print("⏳ Thinking...\n")
            
            # Determine input type
            input_type = "question"
            if any(word in question.lower() for word in ['test', 'quiz', 'evaluate']):
                input_type = "evaluation_request"
            
            result = self.agent.continue_conversation(
                self.current_conversation_id,
                question,
                input_type
            )
            
            print("🤖 AI Tutor:")
            print("=" * 40)
            print(result["response"])
            print("=" * 40)
            print()
            
        except Exception as e:
            print(f"❌ Error processing question: {str(e)}")
    
    def request_evaluation(self):
        """Request an evaluation question."""
        if not self.current_conversation_id:
            print("❌ Please start a tutorial first with 'learn <subject>'")
            return
        
        self.ask_question("Please test my understanding with a question.")
    
    def show_history(self):
        """Show previous learning sessions."""
        try:
            db = TutorialDatabase()
            conversations = db.get_conversations_by_session(self.session_id)
            
            if not conversations:
                print("📭 No previous learning sessions found.")
                return
            
            print("\n📚 Your Learning History:")
            print("=" * 40)
            for conv in conversations:
                print(f"ID: {conv['id']} | Subject: {conv['subject']}")
                print(f"  Started: {conv['created_at']}")
                print()
            
            print("💡 Use 'load <id>' to continue a previous session.\n")
            
        except Exception as e:
            print(f"❌ Error loading history: {str(e)}")
    
    def load_conversation(self, conv_id_str: str):
        """Load a previous conversation."""
        try:
            conv_id = int(conv_id_str)
            
            db = TutorialDatabase()
            history = db.get_conversation_history(conv_id)
            
            if not history:
                print("❌ Conversation not found.")
                return
            
            # Get conversation subject
            import sqlite3
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT subject FROM conversations WHERE id = ?", (conv_id,))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                print("❌ Conversation not found.")
                return
            
            self.current_conversation_id = conv_id
            self.subject = result[0]
            
            print(f"📖 Loaded conversation about: {self.subject}")
            print("=" * 40)
            
            # Display conversation history
            for msg in history[-5:]:  # Show last 5 messages
                role_icon = "👤" if msg["role"] == "user" else "🤖"
                print(f"{role_icon} {msg['role'].title()}: {msg['content'][:100]}...")
                print()
            
            print("💬 You can continue asking questions!\n")
            
        except ValueError:
            print("❌ Please provide a valid conversation ID (number).")
        except Exception as e:
            print(f"❌ Error loading conversation: {str(e)}")

def main():
    """Run the CLI demo."""
    demo = CLITutorialDemo()
    demo.run()

if __name__ == "__main__":
    main() 