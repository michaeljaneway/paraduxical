# Paraduxical

![header](./readme_images/header.png)

## Table of Contents

- [Game Summary](#game-summary)
- [Installation Instructions](#installation-instructions)
  - [Setup](#setup)
    - [Creating Virtual Environment](#creating-virtual-environment)
    - [Activating Virtual Environment](#activating-virtual-environment)
    - [Deactivating Virtual Environment](#deactivating-virtual-environment)
    - [Installing Dependencies](#installing-dependencies)
  - [Requirements](#requirements)
  - [Running the Game](#running-the-game)
- [Demo](#demo)
  - [Game Demo](#game-demo)
  - [SOCS Server Install Video](#socs-server-install-video)
- [Contacts](#contacts)
- [License](#license)

## Game Summary

Paraduxical is an implementation of the board game Paradux, made by Team 2 in CIS*3260 @ UOG.

The game is played on a hexagonal board, and each turn a player selects one of their own tokens and an adjacent token belonging to the opposing player and either swaps their positions, or shifts them in an open direction.

The objective is to be the first player to line up FOUR of your tokens in a row, horizontally or diagonally.

## Installation Instructions

### Setup

Python uses virtual environments to manage Python project libraries and frameworks, such as those that come from outside the Python standard library.
Our project/game uses the open-source **textual** terminal user interface (TUI) framework to build its UI.
As such, **textual** is a dependency that is required by our project to function correctly.
Since our project uses dependencies, we must abide by Python's rules for managing dependencies.

**textual** is a Python project with its own set of dependencies, and so these dependencies must be installed for our project to function.
Dependencies of our dependencies are referred to as **indirect dependencies**, whereas dependencies that are explictly imported by our project are referred to as **direct dependencies**.
Python is smart in that it is able to find and install all of a project's **indirect dependencies** in-order for the **direct dependencies** of a project to function correctly.
Thus, virtual environments and **requirements.txt** files are necessary to allow our Python projects to function correctly.

The rest of the setup section of this document will describe how to:

- Create, activate, and deactivate Python virtual environments
- Install all the project dependencies within a Python virtual environment

#### Creating Virtual Environment

From the project's root directory, run the command below:
`python3 -m venv .venv`

This command below will use Python's virtual environment module to create a new virtual environment, called **.venv** in our project's root directory.
This new virtual environment will contain all of our project's dependencies, and will be fully isolated from other Python virtual environments.

#### Activating Virtual Environment

From the project's root directory, run the following commands:

- Windows: `.venv/Scripts/activate.bat`
- Apple Macintosh or GNU/Linux: `source .venv/bin/activate`

Windows has a different syntax than Macintosh or GNU/Linux because it uses PowerShell, and is not a UNIX-based operating system.
Macintosh and GNU/Linux use the same syntax because they use similar default shells: `zsh` for Macintosh and `bash` for GNU/Linux, and they are both UNIX-based operating systems.
The same concept applies to deactivating the virtual environments, which are described next.

#### Deactivating Virtual Environment

From the project's root directory, run the following commands:

- Windows: `.venv/Scripts/deactivate.bat`
- Apple Macintosh or GNU/Linux: `deactivate`

Note: you actually do not need to run the `deactivate` command from the root directory of the project on Macintosh or GNU/Linux because the `deactivate` command is path-agonstic.
We can execute this command anywhere from within the virtual environment, and there will be no need to provide a path argument to it.
However, Windows still requires you to execute the virtual environment deactivation program from a specific directory, so you must be at the project root to correctly execute the Windows command.

#### Installing Dependencies

From the project root, run the following command to install all the dependencies required to run the game:

```sh
pip install -r requirements.txt
```

**Notes:**

- The **requirements.txt** file is a simply formatted text file that Python uses to find and install all the dependencies of a project, and even allows the developer to specify the precise versions of the dependencies to install.
- This command installs all the dependencies of the game only in the virtual environment you are in now.
  - You will not have access to the same dependencies installed now if you create and use another virtual environment.
  - Python manages virtual environments by isolating them from one another, which means no installed packages from one virtual environment can be shared with another.

### Requirements

- **Python** version 3.9 or higher.
- **textual** framework version 6.5 or higher

### Running the Game

Before running the game, refer to the [Setup](#setup) section described prior for creating and activating Python virtual environments, and installing dependencies in them.

First, you must have already successfully created and activated a Python virtual environment.
To make sure that you are inside an activated Python virtual environment, you should see a similar command prompt like the following:

```sh
(.venv) ajawad@linux-01:~/CIS3260/team-project/m2/paraduxical$
```

Notes about the prompt:

- The most important part of this prompt is the `(.venv)` prefix to the rest of the prompt: `ajawad@linux-01:~/CIS3260/team-project/m2/paraduxical$`.
- The `(.venv)` prefix indicates that you are inside a Python virtual environment, if you were following the instructions in [Setup](#setup) correctly.
- This is a good sign that you are ready to ensure that you have all the required dependencies in your virtual environment to play the game.
- The rest of the prompt: `ajawad@linux-01:~/CIS3260/team-project/m2/paraduxical$` is not important because you will likely have a different username, hostname, and working directory.
- If you do not have `(.venv)` as a prefix in your prompt, then you must refer to the steps described in the [Setup](#setup) section to correctly create and activate a Python virtual environment.

Second, you must verify that you have installed all dependencies that the project requires in your Python virtual environment. To do so, run the following command:

```sh
pip freeze
```

Notes about the `pip freeze` command:

- This command will get `pip` (i.e., the Python package manager) to list all the installed packages in the current Python virtual environment.
- This step is important because it will tell you whether you have all the required packages for the project installed.
- Without any of or all the required packages for the project, you will be unable to run the game.
  - Python will likely throw an exception about missing packages in this case, and so you must solve the missing dependencies problem first.

You should see the following output from the `pip freeze` command if you followed the [Setup](#setup) steps correctly:

```txt
aiohappyeyeballs==2.6.1
aiohttp==3.13.2
aiohttp-jinja2==1.6
aiosignal==1.4.0
attrs==25.4.0
click==8.3.0
frozenlist==1.8.0
idna==3.11
jinja2==3.1.6
linkify-it-py==2.0.3
markdown-it-py==4.0.0
markupsafe==3.0.3
mdit-py-plugins==0.5.0
mdurl==0.1.2
msgpack==1.1.2
multidict==6.7.0
platformdirs==4.5.0
propcache==0.4.1
pygments==2.19.2
rich==14.2.0
textual==6.5.0
textual-dev==1.8.0
textual-serve==1.1.3
typing-extensions==4.15.0
uc-micro-py==1.0.3
yarl==1.22.0
```

Notes about the output of the `pip freeze` command:
- The output of the `pip freeze` command will list all the installed packages in the current Python environment.
- Since you should be inside a Python virtual environment, you will see all the installed packages within the currently activated Python virtual environment.
- You must ensure that you have all the packages listed in the sample output of the `pip freeze` command.
  - The precise version numbers for each package may differ in your case, so different version numbers for the packages should be okay so long as they are not major version changes.
- If there are discrepancies between the output of your `pip freeze` command and the one listed above, you may: (1) be in the wrong Python virtual environment, or (2) have not installed all the required dependencies of the project according to the [Setup](#setup) section in your virtual environment.
  - If this is the case, you need to review the instructions in the [Setup](#setup) section again, and follow them closely.

Once you have verified that the packages necessary to run the project have been installed, you can run the game application via the following simple command:
```sh
python src
```

You should now be within the game application, and you should see a user interface like so:

![Paradux Welcome View](./assets/doc-img/readme-img/paradux_welcome_view.png)

After you see a similar view to the above screen (the color scheme may differ depending on the computer you are using, which is fine), you are now ready to play the game however many times you want.
This step now concludes the game running section.

## Demo

### Game Demo

![demo](./readme_images/demo.gif)

### SOCS Server Install Video

![socs_demo](./readme_images/socs_demo.gif)

## Contacts

- Ali Riayde Jawad
  - [GitHub](https://github.com/ariaydejawad)
  - [GitLab](https://gitlab.socs.uoguelph.ca/ajawad)
- Derek Duong
- Michael Janeway
  - [itch.io](https://happyfacemike.itch.io/)
  - [GitHub](https://github.com/michaeljaneway)
  - [LinkedIn](https://www.linkedin.com/in/michael-janeway/)
- Ryan Nguyen

## License

This project uses the [MIT](https://mit-license.org/) license.
