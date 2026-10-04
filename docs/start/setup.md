# Setting Up

!!! learn "On this page we will learn"
    - how to install Python and VS Code
    - how to create a project folder for StudyM8
    - how to create a virtual environment
    - how to install Flask and the other libraries we need

We'll build StudyM8 in **VS Code** on our own computer. Before we start coding, we need to install the tools and set up our project folder. Follow each step in order.

## Install Python and VS Code

If Python and VS Code are already on your computer, skip to [Create the project folder](#create-the-project-folder).

1. Download and install Python from [python.org](https://www.python.org/downloads/).
    - **Why:** Flask is a Python library, so we need Python to run our server.
    - **Important:** on the first screen of the installer, tick **Add python.exe to PATH**.
    - **Expected result:** the installer finishes with "Setup was successful".
2. Download and install VS Code from [code.visualstudio.com](https://code.visualstudio.com/).
    - **Why:** VS Code is the editor we'll write our Python, HTML and CSS in.
    - **Expected result:** VS Code opens with a Welcome tab.
3. In VS Code, click the **Extensions** icon in the left bar, search for **Python** and install the extension by Microsoft.
    - **Why:** the extension lets VS Code run Python and use virtual environments.
    - **Expected result:** the Python extension shows as installed.

## Create the project folder

1. Create a new folder called ***studym8*** somewhere easy to find, such as your ***Documents*** folder.
    - **Why:** all of StudyM8's files will live in this folder.
    - **Expected result:** an empty ***studym8*** folder.
2. In VS Code, choose **File** → **Open Folder…** and open the ***studym8*** folder. If VS Code asks whether you trust the authors of the files, choose **Yes**.
    - **Why:** VS Code works with everything in the open folder, and the terminal will start in this folder.
    - **Expected result:** the Explorer panel on the left shows **STUDYM8** with no files.

## Create a virtual environment

A **virtual environment** is a private copy of Python just for this project. The libraries we install go into the virtual environment rather than into the computer's main Python, so different projects can't interfere with each other.

1. Press ++ctrl+shift+p++, type **Python: Create Environment** and press ++enter++. Choose **Venv**, then choose the Python version you installed.
    - **Why:** this creates the virtual environment in a folder called ***.venv*** inside our project.
    - **Expected result:** after a few seconds a ***.venv*** folder appears in the Explorer panel.
2. Choose **Terminal** → **New Terminal**.
    - **Why:** we'll type commands to install libraries and run our server in the terminal.
    - **Expected result:** a terminal opens at the bottom of VS Code. The prompt starts with `(.venv)`, which means the virtual environment is active.

!!! warning "No (.venv) in the terminal"
    If the prompt doesn't start with `(.venv)`, close the terminal with the bin icon and open a new one. Libraries installed without `(.venv)` go into the wrong Python, and Flask won't be found when we run our server.

## Install the libraries

1. In the terminal, type the command below and press ++enter++.

    ```text
    pip install flask flask-login plotly pandas
    ```

    - **Why:** this installs Flask (our web server), Flask-Login (for user accounts), Plotly (for the calendar chart) and pandas (which Plotly needs to organise the chart's data).
    - **Expected result:** lots of downloading messages, ending with a line starting `Successfully installed`.
2. Check Flask installed correctly by typing:

    ```text
    flask --version
    ```

    - **Expected result:** something like the lines below. Your version numbers might be a little different.

    ```text
    Python 3.13.7
    Flask 3.1.3
    Werkzeug 3.1.9
    ```

We don't need to install HTMX or Pico CSS. Our pages will load them straight from the internet.

Our computer is ready. In the next lesson we'll write our first Flask app.
