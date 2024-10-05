import pandas as pd
import logging
from typing import Optional

from ..utils.request_utils import get_wrapper
from ..utils.pandas_utils import create_pd_data_frame_from_html_table
from ..utils.team_utils import TEAM_ABBREVIATIONS


class TeamScraper:
    def __init__(self, team_name: str) -> None:
        self.team_name = team_name
        self.abbreviation = TEAM_ABBREVIATIONS.get(self.team_name)
        if not self.abbreviation:
            raise ValueError(f"Team abbreviation not found for team name: {team_name}")
        self.url = f"https://www.basketball-reference.com/teams/{self.abbreviation}"

    def _fetch_and_process(self, endpoint: str, html_id: str) -> Optional[pd.DataFrame]:
        """
        Fetches data from a given URL endpoint and processes it into a DataFrame.

        Args:
            endpoint (str): The endpoint URL to fetch data from.
            table_type (str): The type of data to process (used in `create_pd_data_frame_from_html_table`).

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

    def get_team_stats_by_year(
        self, table_type: str, year: int
    ) -> Optional[pd.DataFrame]:
        """
        Given a dynamic variable, compute a pandas Data Frame for a given team.

        Args:
            table_type (str): Table type associated on the website.
            year (int): Year.

        Returns:
            Optional[pd.DataFrame]: Pandas DataFrame, or None if an error occurs.
        """
        valid_stats = ["roster"]
        if table_type not in valid_stats:
            logging.error(
                f"Invalid table type: {table_type}. Try one of these: {valid_stats}"
            )
            return None

        endpoint = f"{self.url}/{year}.html"
        return self._fetch_and_process(endpoint, table_type)
