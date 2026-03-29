# **AI Chat**
A chat application that uses the OpenRouter API to interact with various artificial intelligence models.

## Getting Started

### Installation and Setup

1. **Install Required Software**
   - Install [Git](https://git-scm.com/downloads)
   - Install [Python 3.9+](https://www.python.org/downloads/)
   - Install [Visual Studio Code](https://code.visualstudio.com/download)

2. **Cloning the Project**

   ```bash
   # Clone the repository
   git clone https://github.com/Saverof/AIChat.git
   # Navigate to the project directory
   cd AIChat
   ```

3. **VSCode Configuration**
   - Open VSCode
   - Install recommended extensions:
     - Python (ms-python.python)
     - Python Environment Manager
     - Python Extension Pack
   - Open the project: **File** → **Open Folder** → Select the `AIChat` folder
   - Select the Python interpreter:
     1. Press **F1** or **Ctrl+Shift+P**
     2. Type **"Python: Select Interpreter"**
     3. Choose **Python 3.9** or higher

4. **Virtual Environment Setup**

   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # For Windows:
   .\venv\Scripts\activate
   # For Linux/Mac:
   source venv/bin/activate
   ```

5. **Environment Variables Configuration**
   - Copy the `.env.example` file to a new `.env` file
   - Open `.env` and replace `your_api_key_here` with your OpenRouter API key
   - The remaining settings can be left as default

## **Building the Application**

### Requirements
- Python 3.9 or higher

### Windows Build

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the executable:
   ```bash
   python build.py
   ```

   The executable will be created at `bin/AIChat.exe`.

---

### Linux Build

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the executable:
   ```bash
   python3 build.py
   ```

   The executable will be created at `bin/aichat`.

3. Set execution permissions:
   ```bash
   chmod +x bin/aichat
   ```

---

### Configuration

Create a `.env` file in the root directory with the following content:
```
OPENROUTER_API_KEY=your_api_key
BASE_URL=https://openrouter.ai/api/v1
DEBUG=False
LOG_LEVEL=INFO
MAX_TOKENS=1000
TEMPERATURE=0.7
```

## **Project Structure**

```
├── assets/                # Application resources
│   └── icon.ico           # Application icon
├── bin/                   # Compiled executables
├── build/                 # Temporary build files
├── exports/               # Directory for exported chats
├── logs/                  # Application logs
├── src/                   # Source code
│   ├── api/               # API integration
│   │   ├── __init__.py
│   │   └── openrouter.py  # OpenRouter API interaction
│   ├── ui/                # User interface
│   │   ├── __init__.py
│   │   ├── components.py  # UI components
│   │   └── styles.py      # Interface styles
│   ├── utils/             # Utilities
│   │   ├── __init__.py
│   │   ├── analytics.py   # Usage analytics
│   │   ├── cache.py       # Caching
│   │   ├── logger.py      # Logging system
│   │   └── monitor.py     # System monitoring
│   ├── main_simple.py     # Simplified version of main.py with limited functionality
│   └── main.py            # Application entry point
├── .env.example           # Configuration example
├── .gitignore             # Git exclusions
├── build.py               # Build script
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

## **Detailed Feature Description**
### **Core Features**

1. **Chat with AI Models**
   - Support for various models via the OpenRouter API
   - Contextual dialogues with history retention
   - Customizable generation parameters (temperature, maximum token count)

2. **Chat History Management**
   - Automatic saving of dialogue history
   - Ability to view previous conversations
   - Exporting dialogues in various formats

3. **Usage Analytics**
   - Tracking usage of different models
   - Statistics on the number of requests
   - Monitoring token consumption

4. **System Functions**
   - Caching for performance optimization
   - Detailed logging of application operation
   - System resource monitoring

### **Technical Features**

- **Caching (utils/cache.py)**
  - Local storage of chat history
  - Optimization of repeated requests
  - Cache size management

- **Logging (utils/logger.py)**
  - Customizable logging levels
  - Log file rotation
  - Detailed error information

- **Analytics (utils/analytics.py)**
  - Collection of usage statistics
  - Analysis of model popularity
  - Resource usage reports

- **Monitoring (utils/monitor.py)**
  - Performance tracking
  - Control of system resource usage
  - Notifications for critical events

- **User Interface (ui/)**
  - Modern design
  - Customizable themes
  - Responsive interface

- **API Integration (api/)**
  - Secure interaction with OpenRouter
  - Error handling and retries
  - Support for various AI models (over 215 models, including more than 20 free ones)
