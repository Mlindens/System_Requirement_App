# System Requirement App

This program is designed to compare the user's computer system specifications with the minimum and recommended specifications of a variety of popular applications and video games. It provides an easy way for users to determine if their system is capable of running the selected application or game and, if not, provides suggestions for hardware upgrades.

## Features

* Provides a list of popular applications and video games.
* Compares the user's system specifications with the minimum and recommended requirements for the chosen application or game.
* Provides color-coded results indicating if the user's system meets, exceeds, or falls below the minimum or recommended requirements.
* Offers hardware upgrade suggestions if the user's system does not meet the requirements.

## Dependencies

* Python 3.x
* pyodbc
* psutil
* pynvml
* dotenv

## Usage

1. Select an application or video game from the dropdown menu.
2. Click on "Minimum Specs" to compare your system with the minimum requirements or click on "Recommended Specs" to compare with the recommended requirements.
3. View the color-coded results in the text widget. Green indicates your system meets or exceeds the requirement, while red indicates your system falls below the requirement.
4. If your system does not meet the requirements, follow the provided links to browse for hardware upgrades.

## Note

* This program uses a database to pull video game and application data from.
* If you wish to get database login credentials, feel free to send me a message.
* This program will NOT work without login credentials.
