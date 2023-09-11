# WaitMate Discord Bot

## Overview

WaitMate is a Discord bot designed to streamline the moderation process on Discord servers, offering a simple and fair queue system for users and supporters. It comes handy especially in environments where users are required to wait in line for their turn to be attended to by a supporter.

## Features

- **Fair Queue System**: Ensures users are attended to on a first-come, first-serve basis, promoting a fair and efficient system.
- **Special Attention Handling**: The bot recognizes users with a "@" in their name and can differentiate between those who are waiting for specific moderation and those who are open to being attended by any supporter.
- **Automatic User Moving**: Supporters can use the "/next" command to automatically move the next user in the queue to their channel.
- **Easy-to-use Commands**: Simplified commands such as "/next" make it easy for supporters to perform actions without manual efforts.

## Setting Up

### Prerequisites

- Python 3.10
- Discord.py library

### Installation

1. Clone the repository to your local machine
```sh
git clone https://github.com/MaikeruDev/WaitMate.git
```
2. Install the necessary Python packages
```sh
pip install -r requirements.txt
```
3. Change the Discord Token Bot at the end of the file just as all the other 3 ID's in the file

4. Run the bot
```sh
python bot.py
```

## Usage

- Users with "@" in their name can specify the moderator they wish to be attended by.
- Supporters can use the "/next" command to call upon the next user in line.

## Contribution

Feel free to fork the project and submit your contributions through pull requests.

## License

This project is under the MIT license. See the [LICENSE](LICENSE.md) file for details.

## Contact

If you have any questions, feel free to reach out to us.

- GitHub: [Your GitHub Profile](https://github.com/MaikeruDev)
- Discord: maikeru.dev
