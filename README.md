# Audio-Music-Player
A simple desktop audio player built with Python, Tkinter, and Pygame. Features include playlist management, volume control, playback navigation, and AI-powered music recognition using Audd.io API.

# Steps to run the program:
1. Create and Activate a Virtual Environment

   For Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

  For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Install the required dependencies
```bash
pip install requests pygame
```
3. Obtain an Audd.io API Token
   - Go to https://audd.io
   - Sign up for an account.
   - Once logged in, visit your dashboard to find your API token.
     
4. Configure the API Token in Code
   
   Open the project file and locate the line in the function get_info_using_AI(), then replace it with your actual token:
   ```bash
   api_token = "YOUR_AUDD_API_KEY"
   ```
5. Running the Program
```bash
python3 Audio_Music_Player.py
```
