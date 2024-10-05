# HoopStats

`hoopstats` can be accessed [here](https://pypi.org/project/hoopstats/) on PyPi.

This project serves as a proof of concept (POC) for web scraping NBA data from Basketball Reference. The primary motivation is to explore the intersection of data science and software engineering by building a reliable NBA-focused Python package. The long-term objective of this project is to evolve into the backend of a full-stack application, providing users with seamless access to NBA statistics through an intuitive and user-friendly interface.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)
- [Contact](#contact)

## Features

- Scrape NBA player statistics from Basketball Reference
- Access detailed game logs and player splits
- Convenient API for querying player and game data

## Installation

To install `HoopStats`, you can use pip:

```bash
pip install hoopstats
```

## Usage

Here's a basic example of how to use HoopStats:

```python
from hoopstats import PlayerScraper

# Initialize the scraper with player names
player_scraper = PlayerScraper(first_name="Lonzo", last_name="Ball")

# Access the player's data
print(player_scraper.url)

# Access the player's game log stats, based on a given year
print(player_scraper.get_game_log_by_year(2024))
```

To review full functionality of the code, look under the [services folder](./hoopstats/services/).

## Testing

To run the tests for HoopStats, use the following command:

```bash
pytest --cov=.
```

Make sure to add tests for any new features or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contact

Author: Calvin Min (2024)
