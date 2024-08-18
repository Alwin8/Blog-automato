
# YouTube to Medium Blog Converter

## Introduction

The **YouTube to Medium Blog Converter** is a Python script that automates the process of converting YouTube videos into Medium blog posts. It fetches the latest video from a specified YouTube channel, extracts subtitles, transforms the subtitles into a detailed script, and publishes the content as a blog post on Medium. This tool is perfect for content creators who want to repurpose their video content into engaging written articles.

## Running the Script
1. **Add Api keys**
   
   You need to configure the script with your API keys and tokens. Edit the script and replace the placeholder values with your actual keys in blogautomated.py:

   ```bash
   YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY' # get from google credentials
   CHANNEL_ID = 'YOUR_CHANNEL_ID' # get from this website
   GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY' # get from google ai studio
   MEDIUM_INTEGRATION_TOKEN = 'YOUR_MEDIUM_INTEGRATION_TOKEN' #get from medium in app section of settings
   ```
2. **Install Dependencies**

   First, ensure you have Python installed. Then, install the required packages using:

   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Script**

   Execute the script with:
   ```bash
   python blogautomated.py
   ```
## Donations

If this project makes you happy by reducing your development time, you can make me happy by treating me to a cup of coffee, or become a [Sponsor of this project](https://github.com/sponsors/Alwin8) :)  


