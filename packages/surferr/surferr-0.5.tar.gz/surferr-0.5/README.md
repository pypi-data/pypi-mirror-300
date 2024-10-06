# Surfer: AI-Powered Website & Webpage Summarizer

![Python](https://img.shields.io/badge/python-3.12-blue)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
![License](https://img.shields.io/badge/license-MIT-red)
![Together-AI](https://img.shields.io/badge/Together%20AI-0f6fff)
![BART](https://img.shields.io/badge/BART-8A2BE2)

## What is it?

Surfer is an AI-powered Chrome extension designed to make web browsing faster and smarter by summarizing both website overviews and webpage content. 
Whether you're doing in-depth research or just exploring a new site, 
Surfer delivers concise summaries tailored to your needs.
With Surfer, you can :
 - Get brief website summaries with just two lines of information.
 - Generate detailed webpage content summaries from articles, blogs, and more.
 - Choose between paragraph summaries or bullet points for a customized reading experience.

## Main Features

Here’s what makes **Surfer** essential :

 - **Website Information Summarization** : Receive a 2-line overview of any website for a quick glance at its purpose and content.
 - **Webpage Content Summarization** : Get comprehensive summaries of webpage content in a concise format. 
 - **Real-time API Integration** : Surfer uses Together API and state-of-the-art models like BART for real-time summarization. 

## New Features

- **Dark/Light Theme Toggle**: Surfer now includes a theme toggle button, allowing users to switch between light and dark modes for a comfortable browsing experience.
- **Improved UI**: The UI has been enhanced for better and a more intuitive user experience. All elements, including the radio buttons and submit button, are now more user-friendly and visually appealing.
- **Copy Summary**: Now, to make it easier for user to copy the generated summary, The user can simply click on the Summary to copy it to the clipoard.

## Where to get it?

The extension is hosted on GitHub at : https://github.com/gautamxgambhir/surferr

## Package

#### Links
 - [PyPi](https://pypi.org/project/surferr/0.3/)
 - [Source code](https://github.com/gautamxgambhir/surferr)

#### Package Installation
    pip install surferr

### Upgrade
    pip install surferr --upgrade

#### Package Features
 - Summarize any text
 - Extract text from a webpage
 - Summarize a webpage from a URl
 - Get website information summary

##### Setup of Package

```
from surferr import Surfer, version

# Make sure to provide your API key of Together AI
API_KEY = "YOUR_API_KEY"

# Create an instance of the Surfer class by providing the API key
surfer = Surfer(api_key=API_KEY)
```

##### Check Version

```
# Display the current version of the package
print(version())
```

##### Summarize a block of text

```
text = """
YOUR_TEXT
"""
# Call the summarize_text method to generate summary
text_summary = surfer.summarize_text(text)
print(text_summary)
```

##### Extracting text content from a webpage

```
# Make sure to provide the URL
url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

# Call the extract_text_from_webpage method to fetch and extract text content from the webpage
webpage_text = surfer.extract_text_from_webpage(url)
print(webpage_text)
```

##### Summarizing a webpage's content

```
# Call the summarize_webpage method to generate a summary of the webpage's content
webpage_summary = surfer.summarize_webpage(url)
print(webpage_summary)
```

##### Getting Information about a website 

```
# Use the website_info_summary method to get summary of the website
website_info = surfer.website_info_summary(url)
print(website_info)
```

## Installation and Setup

#### 1. Clone the repository :
``` 
git clone https://github.com/gautamxgambhir/Surferr.git 
```

#### 2. Backend setup (Make sure the ```app.py``` server is running) :
 - Navigate to the project directory.
 - Install the required Python dependencies :
    ```
    pip install -r requirements.txt
    ```
 - Make sure to enter your [Together AI](https://www.together.ai/) API key in ```api_key.txt```.

 - Start the Flask server :
    ```
    python app.py
    ```
#### 2. Load the extension in Chrome :
 - Go to **chrome://extensions/** in your browser.
 - Enable **Developer Mode** in the top-right corner.
 - Click **Load unpacked** and select the ```surfer``` directory.

## Usage
Once installed, Surfer can summarize websites and webpage content directly from your Chrome browser :

[Download Video Tutorial for Surfer Usage](https://cdn.discordapp.com/attachments/924595995252232222/1290820853075808307/Project_Video.mp4?ex=66fdda19&is=66fc8899&hm=0fde6035c0fdcc04517fa4554bd821535504d7e0f23bb829355c7622c2263bbc&)

#### 1. Open the Surfer Extension :
 - Click on the Surfer icon in your Chrome toolbar.
#### 2. Select a Radio Button :
 - **Website Information** : Summarizes the website's core details.
- **Webpage Content Summary** : Summarizes the visible content of the webpage you're currently on.
#### 3. Submit Button :
 - Click **Submit** to get the summary of the webpage or website information directly in the extension's popup.

## Dependencies
 - [**Flask** : Backend server for handling summarization requests.](https://flask.palletsprojects.com/en/3.0.x/)
 - [**Together API** : Real-time AI API for generating summaries.](https://www.together.ai/)
 - [**BART Model** : Summarization model for content extraction.](https://huggingface.co/docs/transformers/en/model_doc/bart)

## Contact

- `Email` - ggambhir1919@gmail.com
- `Instagram` - https://www.instagram.com/gautamxgambhir/
- `Twitter` - https://www.twitter.com/gautamxgambhir/