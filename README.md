# Script to delete images from Discord based on contained text using OCR.

### **Requirements**

- 🐍️ Python 
- 🤖 [Discord bot token](https://discord.com/developers/applications)
- [Tesseract](https://github.com/tesseract-ocr/tesseract)


### **Installation**

- Use pip to install the Python modules
    - [discord.py](https://github.com/Rapptz/discord.py)
    - [pytesseract](https://github.com/madmaze/pytesseract)

- Install [Tesseract](https://github.com/tesseract-ocr/tesseract) 
    - for exemple:  `sudo apt install tesseract-ocr-por`
      to install Tesseract in Ubuntu for the Portuguese language 

    - or follow the [installation guide](https://tesseract-ocr.github.io/tessdoc/Installation.html)
	
	- make sure it is in your PATH

    - Download the files from this repository and fill the configuration file

### **Usage**

- After filling and renaming the config.ini file you can run the script with 
`python3 UndiscordOCR.py`

- By default it will run only in real-time mode, detecting when a message is sent into the chat (all channels) and checking if it has one of the blocked words, and if so, deleting the message

- If the `delete_history` option is set to True, it will search through all the channel history
    Enter only `channel_id` on the config file if you want to scan only one specific channel, otherwise, if `server_id` is provided, all the channels in the server will be scanned 
note: using the single channel option is less prone to problems due to crashes, specially in really big channels

- You also can choose to store the flagged images or not

- A file will be generated to keep track of the progress during the search.
    







