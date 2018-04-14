# Homework
A Flask Web App to extract data from storefront product pages

## Instructions for Mac based local deploy

- Install/Verify Python v2.7+ is installed.
- Open Terminal
  - git clone https://github.com/bchukwuma/SFDataExtractor
- **Optional** Setup Virtual Environment
  - Activate Environment
    - **source bin/activate**
- Install Flask
  - **pip install flask**
- Install modules
  - **pip install -r requirements.txt**
- python main.py 

## Instructions for a Windows based local deploy

- Install Python 3.6+
- Install Editor of choice **I'm using VS Code with Python Extensions
- Open terminal
- **git clone https://github.com/bchukwuma/SFDataExtractor**
- ** If  you are using VS Code **
  - Set your Python Interpreter 
    - **Ctrl + Shft + P** & Type "Python select interpreter"
    - Select the instance of Python you installed in Step 1.
- Setup virtual environment.
  - **python -m venv venv**
- Activate new virtual environment.
  - **.\venv\scripts\activate**
- Install relevant modules.
  - **pip install -r requirements.txt**
- ** On Windows Machines **
  - You will need to set your FLASK_APP global variable to your main file in command line.
  - Type **cmd** to switch your current terminal session to command line.
    - **set FLASK_APP=main.py** 
  - Reactivate Python virtual environment. I suggest switching back to a PowerShell Instance.
    - **powershell**
  - **.\venv\scripts\activate**
- **flask run**

## Outstanding Items - In Progress - x
- [x] Moving inline styling to static css file.
- [ ] Card img src not always center aligned.
- [ ] Get_products and get_related_products share a lot of functionality. Consider rewrite to minimize duplicate code blocks.
