# Discord YouTube Bot

![Python](https://img.shields.io/badge/Python-3.x%2B-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0.0%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Overview
**Discord YouTube Bot** is a feature-rich Discord bot that allows users to interact with YouTube directly from their Discord servers. The bot can fetch channel statistics, search for videos, retrieve video details, and display the latest video from a specified YouTube channel.

## Features
- **YouTube Channel Stats:** Get detailed statistics about a YouTube channel, including subscriber count, total views, and video count.
- **YouTube Video Search:** Search for the top 5 YouTube videos matching a query.
- **YouTube Video Details:** Retrieve detailed information about a specific YouTube video, including views, likes, and comments.
- **Latest Video:** Get the latest video from a YouTube channel.

## Commands

### `!hello`
- Greets the user with a friendly message.
- **Example:** `!hello`

### `!ytstats <channel_identifier>`
- Fetches and displays statistics for a specified YouTube channel.
- Supports both new-style usernames (starting with `@`) and channel IDs.
- **Example:** `!ytstats UC_x5XG1OV2P6uZZ5FSM9Ttw` or `!ytstats @username`

### `!ytsearch <query>`
- Searches YouTube for the top 5 videos matching the specified query.
- **Example:** `!ytsearch Python tutorials`

### `!ytvideo <video_id>`
- Retrieves detailed information about a YouTube video using its video ID.
- **Example:** `!ytvideo dQw4w9WgXcQ`

### `!ytlatest <channel_id>`
- Fetches the latest video from a specified YouTube channel.
- **Example:** `!ytlatest UC_x5XG1OV2P6uZZ5FSM9Ttw`

## Setup

### Prerequisites
- Python 3.x or higher
- [pip](https://pip.pypa.io/en/stable/installation/)