import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from io import StringIO


def create_pd_data_frame_from_html_table(
    html_content: str, html_id: str
) -> pd.DataFrame:
    """
    This function takes in html table content and produces a pandas data frame

    Raises:
        ValueError: Given HTML content does not have a table

    Returns:
        pd.DataFrame: Pandas Data Frame
    """
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", {"id": html_id})

    if table is None:
        raise ValueError("Failed to retrieve table data.")

    # Read in data and replace values for json compliancy
    df = pd.read_html(StringIO(str(table)))[0]
    df.replace([np.inf, -np.inf, np.nan], None, inplace=True)
    return df
