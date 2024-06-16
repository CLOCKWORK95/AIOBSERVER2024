# Beginner's Guide to Git, GitHub, and Setting Up a Python Project

## Step 1: Install Visual Studio Code (VSCode) Locally

1. **Download VSCode**:
    - Go to the [VSCode download page](https://code.visualstudio.com/Download).
    - Download the installer for your operating system (Windows, macOS, or Linux).

2. **Install VSCode**:
    - Follow the installation instructions for your operating system.
    - On Windows, run the downloaded installer and follow the setup wizard.
    - On macOS, open the downloaded `.dmg` file and drag VSCode to your Applications folder.
    - On Linux, follow the instructions provided on the download page for your specific distribution.

3. **Launch VSCode**:
    - Open VSCode after installation.
    - Optionally, sign in with your GitHub account for synchronization of settings and extensions.

4. **Install Python Extension**:
    - In VSCode, go to the Extensions view by clicking the Extensions icon in the Activity Bar on the side of the window or by pressing `Ctrl+Shift+X`.
    - Search for "Python" and install the official Python extension by Microsoft.

## Step 2: Install Git Locally

1. **Download Git**:
    - Go to the [Git download page](https://git-scm.com/downloads).
    - Download the installer for your operating system (Windows, macOS, or Linux).

2. **Install Git**:
    - Follow the installation instructions for your operating system.
    - On Windows, run the downloaded installer and follow the setup wizard. You can use the default settings.
    - On macOS, open the downloaded `.dmg` file and follow the instructions.
    - On Linux, use your package manager to install Git. For example, on Debian-based systems:
    ```sh
    sudo apt-get install git
    ```

3. **Verify Installation**:
    - Open your terminal and run:
    ```sh
    git --version
    ```
    - You should see the Git version number printed.

## Step 3: Create a GitHub Account

1. **Visit GitHub**: Go to [github.com](https://github.com).
2. **Sign Up**: Click on the "Sign up" button.
3. **Fill in the Details**: Enter your email, create a username and password.
4. **Verify Your Email**: Follow the instructions to verify your email address.
5. **Complete Setup**: Follow the on-screen instructions to complete your account setup.

## Step 4: Create a New Repository on GitHub

1. **Log In**: Log into your GitHub account.
2. **New Repository**: Click the "+" icon at the top right and select "New repository".
3. **Repository Details**:
    - **Repository Name**: Choose a name for your repository.
    - **Description**: Optionally, add a description.
    - **Visibility**: Choose between Public or Private.
4. **Initialize Repository**: Check "Initialize this repository with a README" if you want a README file.
5. **Create Repository**: Click on "Create repository".

## Step 5: Clone the Repository Locally

1. **Copy Repository URL**:
    - On your repository page, click the green "Code" button.
    - Copy the URL (e.g., `https://github.com/yourusername/your-repository.git`).
2. **Open Terminal**:
    - On Windows, you can use Command Prompt or PowerShell.
    - On macOS or Linux, use the Terminal.
3. **Clone Repository**:
    ```sh
    git clone https://github.com/yourusername/your-repository.git
    ```
4. **Navigate to Repository Folder**:
    ```sh
    cd your-repository
    ```

## Step 6: Install Python Locally

1. **Download Python**:
    - Go to [python.org](https://www.python.org) and download the latest version of Python.
2. **Install Python**:
    - Follow the installation instructions for your operating system.
    - Ensure you check the box to add Python to your PATH during installation.
3. **Verify Installation**:
    - Open your terminal and run:
    ```sh
    python --version
    ```
    - You should see the Python version number printed.

## Step 7: Initialize a New Python Project Using Poetry and Venv

1. **Install Poetry**:
    - Follow the installation instructions from the [Poetry official website](https://python-poetry.org/docs/#installation).
    - Typically, you can use:
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    - Ensure Poetry's bin directory is in your PATH (the installer will show instructions for this).
2. **Create and Activate a Virtual Environment**:
    - Create a virtual environment using `venv`:
    ```sh
    python -m venv .venv
    ```
    - Activate the virtual environment:
        - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
        - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```
3. **Initialize a New Poetry Project**:
    - In the terminal, run:
    ```sh
    poetry init
    ```
    - Follow the prompts to configure your new Python project.
4. **Configure Poetry to Use the Virtual Environment**:
    - Tell Poetry to use the virtual environment:
    ```sh
    poetry env use $(which python)
    ```
5. **Install Project Dependencies**:
    - Add any necessary dependencies for your project using:
    ```sh
    poetry add <package_name>
    ```

---

You've now set up VSCode, installed Git, created a new GitHub repository, cloned it locally, installed Python, and initialized a new Python project using Poetry and a virtual environment!
