# Vietnamese Historical Chatbot

## Overview

A Streamlit-based chatbot application that enables users to interact with historical Vietnamese figures through AI-powered conversations. The application uses GROQ's LLaMA 3 language model to simulate conversations with personalities like Hồ Chí Minh, Lý Thường Kiệt, and Trần Hưng Đạo. Each character has unique speaking styles, historical context, and personality traits defined through custom system prompts.

## Recent Changes (September 30, 2025)

- **Gemini-style UI**: Redesigned interface with rolling chat and sidebar character selection
- **Enhanced Readability**: Added glowing text effects and improved contrast for better visibility against background
- **Background Image**: Embedded Vietnamese warrior statue image as base64 for reliable display
- **Red Button Greeting**: "Xin chào!" welcome message now displayed in a red button-style badge
- **Gold Greeting Text**: Changed introductory greeting text to gold color for better visibility
- **Sample Questions**: Moved from sidebar to below text input, displayed in 3 columns for easy access
- **Form-based Input**: Converted text input to Streamlit form for proper Enter key support and auto-clear functionality
- **Fixed Config Order**: Moved st.set_page_config to top of file to ensure layout settings apply correctly
- **Sidebar Toggle Fix**: Removed CSS hiding header/menu to restore sidebar toggle functionality
- **Centered Layout**: Input area and sample questions capped at 1100px max-width for Gemini-like appearance
- **Updated Button Styling**: Send button now has gradient red styling matching Vietnamese theme; sidebar buttons maintain gold highlight when selected
- **Custom Sidebar Toggle**: Added floating red circular button (☰) using CSS-only solution (hidden checkbox + label) that reliably toggles sidebar without JavaScript
- **Multi-Conversation History**: Implemented timestamp-based conversation management system supporting multiple saved conversations
- **Past Conversations Sidebar**: Added "Lịch sử trò chuyện" section showing up to 10 recent conversations with load/delete options
- **Scroll-to-Bottom Button**: Added floating button (⬇️) that appears when scrolling up, enabling quick return to latest messages
- **Minimal White Space**: Reduced padding to 20px between messages and input box, removed unnecessary spacing for compact ChatGPT-like layout
- **Slow Smooth Scrolling**: Implemented 1.2-second animated scroll with ease-in-out easing for graceful navigation
- **Fixed Spacing Bug**: Added 120px spacer div after messages to ensure exactly 20px visual gap before fixed input box
- **Fixed Scroll Button Bug**: Refactored scroll-to-bottom button to use consistent parent document context with proper event management and reliable cross-frame operation

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: Streamlit web application with custom CSS styling
- **Layout**: Wide layout with expandable sidebar for character selection
- **Styling Approach**: Custom CSS with background image overlay and translucent white layer for readability
- **UI Components**: Chat interface with message history, suggested questions, and character-specific greetings
- **Design Pattern**: Single-page application with dynamic content based on selected personality

### Backend Architecture

**Core Components**:

1. **Personality System** (`personalities.py`)
   - Object-oriented design using `HistoricalPersonality` class
   - Each personality contains: name, description, system prompt, and greeting
   - System prompts define character behavior, historical context, and speaking style
   - Extensible dictionary-based storage (`PERSONALITIES`) for easy addition of new characters

2. **Conversation Management** (`app.py`)
   - Session state management for chat history persistence
   - Message history stored as list of dictionaries with role and content
   - System prompt injection at conversation initialization
   - Context-aware responses using full conversation history

3. **Data Layer** (`data.json`)
   - Character-specific suggested questions stored in JSON format
   - Keyed by personality identifier for easy retrieval
   - General questions available for the default historian character

**AI Integration**:
- GROQ API client for LLaMA 3 model access
- Streaming responses for real-time user feedback
- System prompts guide model behavior to match historical personalities
- Temperature and other parameters configurable per request

**State Management**:
- Streamlit session state for maintaining conversation context
- Selected personality tracked across reruns
- Chat messages persisted throughout user session

### External Dependencies

**Third-Party Services**:
1. **GROQ API** (Required)
   - Purpose: LLaMA 3 language model inference
   - Authentication: API key via environment variable or Streamlit secrets
   - Configuration: `GROQ_API_KEY` stored in secrets or environment

**Python Packages**:
- `streamlit`: Web application framework
- `groq`: Official GROQ API client
- `pandas`: Data manipulation (listed but not actively used in provided code)
- `json`: Built-in, for loading suggested questions
- `os`: Built-in, for environment variable access
- `base64`: Built-in, for encoding background images

**Static Assets**:
- Background image: `attached_assets/z7055735395182_b42d68da9f2bdba54b1a9c73c7841e86_1759215395425.jpg`
- Custom CSS file: `style.css` (embedded in `app.py` via base64 encoding)

**Configuration Files**:
- `.devcontainer/devcontainer.json`: VS Code devcontainer configuration for Python 3.11
- `requirements.txt`: Python dependencies specification
- `.streamlit/secrets.toml`: Optional secrets management file (not in repository, user-created)

**Deployment Environment**:
- Designed for Replit deployment
- Supports both environment variables and Streamlit secrets for API key management
- Auto-forwarding on port 8501 configured in devcontainer