import pandas as pd
import logging
import matplotlib.pyplot as plt
from typing import Optional

from ..utils.request_utils import get_wrapper
from ..utils.players_utils import create_player_suffix, auto_correct_player_name
from ..utils.pandas_utils import create_pd_data_frame_from_html_table


class PlayerScraper:
    def __init__(self, first_name: str, last_name: str):
        try:
            name = auto_correct_player_name(first_name=first_name, last_name=last_name)
            if name is None:
                raise ValueError(f"No match found for: {first_name} {last_name}")
        except Exception as e:
            logging.error(f"Error in auto correcting player name: {e}")
            raise

        self.first_name = name[0]
        self.last_name = name[1]

        self.suffix = create_player_suffix(self.first_name, self.last_name, "01")
        self.url = f"https://www.basketball-reference.com/players/{self.suffix}"

    def _fetch_and_process(self, endpoint: str, html_id: str) -> Optional[pd.DataFrame]:
        """
        Fetches data from a given URL endpoint and processes it into a DataFrame.

        Args:
            endpoint (str): The endpoint URL to fetch data from.
            data_type (str): The type of data to process (used in `create_pd_data_frame_from_html_table`).

        Returns:
            Optional[pd.DataFrame]: Pandas Data Frame, or None if an error occurs.
        """
        try:
            r = get_wrapper(endpoint)
            if r and r.content:
                return create_pd_data_frame_from_html_table(r.content, html_id)
            else:
                raise ValueError(f"No data available at endpoint: {endpoint}")
        except Exception as e:
            logging.error(f"Error fetching data from {endpoint}: {e}")
            return None

    def get_stats_by_year(self, stat_type: str = "per_game") -> Optional[pd.DataFrame]:
        """
        Web scrapes a player's aggregate stats grouped by the year.

        Args:
            stat_type (str, optional): 'per_game', 'totals', and 'advanced' are viable options. Defaults to "per_game".

        Returns:
            Optional[pd.DataFrame]: Pandas Data Frame.
        """
        if stat_type not in ["per_game", "totals", "advanced"]:
            logging.info(f"Invalid stat type: {stat_type}")
            return None

        endpoint = f"{self.url}.html"
        return self._fetch_and_process(endpoint, stat_type)

    def get_stats_by_year_visualization(
        self, stat_type: str = "per_game"
    ) -> Optional[plt.Figure]:
        """
        Visualizes a player's statistics for a given stat type by season in a bar chart.

        Args:
            stat_type (str): The type of statistics to fetch and visualize (e.g., 'per_game', 'totals', 'advanced').
                            Defaults to 'per_game'.

        Returns:
            Optional[plt.Figure]: Matplotlib Figure object containing the plot if data exists, or None if the data frame is empty.
        """
        data_frame = self.get_stats_by_year(stat_type=stat_type)
        if data_frame.empty:
            logging.error(
                f"No data available to visualize for {self.first_name} {self.last_name} in this stat: {stat_type}"
            )
            return None
        else:
            data_frame.plot(kind="bar", x="Season", y="PTS", figsize=(10, 6))
            plt.title(
                f"{self.first_name} {self.last_name} - {stat_type.capitalize()} Stats"
            )
            plt.xlabel("Season")
            plt.ylabel("PTS")
            plt.tight_layout()
            return plt

    def get_game_log_by_year(self, year: int) -> Optional[pd.DataFrame]:
        """
        Web scrapes a player's game log based on the year.

        Args:
            year (int): Numerical value that represents a year.

        Returns:
            Optional[pd.DataFrame]: Pandas Data Frame.
        """
        endpoint = f"{self.url}/gamelog/{year}"
        return self._fetch_and_process(endpoint, "pgl_basic")

    def get_splits_by_year(self, year: int) -> Optional[pd.DataFrame]:
        """
        Web scrapes a player's splits based on the year.

        Args:
            year (int): Numerical value that represents a year.

        Returns:
            Optional[pd.DataFrame]: Pandas Data Frame.
        """
        endpoint = f"{self.url}/splits/{year}"
        return self._fetch_and_process(endpoint, "splits")
