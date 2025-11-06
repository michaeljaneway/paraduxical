# Paraduxical

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
- [Contacts](#contacts)
- [License](#license)

## Game Summary

    Summary here

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

`pip install -r requirements.txt`

**Notes:**

- The **requirements.txt** file is a simply formatted text file that Python uses to find and install all the dependencies of a project, and even allows the developer to specify the precise versions of the dependencies to install.
- This command installs all the dependencies of the game only in the virtual environment you are in now.
  - You will not have access to the same dependencies installed now if you create and use another virtual environment.
  - Python manages virtual environments by isolating them from one another, which means no installed packages from one virtual environment can be shared with another.

### Requirements

- **Python** version 3.9 or higher.
- **textual** framework version 6.5 or higher

### Running the Game

To run the game, open a terminal in this folder, **/paraduxical/**, and run the following: `python src`

## Demo

    Sequence of screenshots/GIF Here

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
