import re
import logging
import unicodedata

from typing import List
from rapidfuzz import process
from .request_utils import get_wrapper
from .pandas_utils import create_pd_data_frame_from_html_table

# --- Global Variables --- #
active_players = []


def normalize_name(name: str) -> str:
    """
    Remove special characters from a name

    Args:
        name (str): Name

    Returns:
        str: Normalized Name
    """
    normalized_name = unicodedata.normalize("NFD", name)
    normalized_name = re.sub(r"[^\w\s]", "", normalized_name)
    return normalized_name.lower()


def scrape_active_players() -> None:
    """
    Scrapes from an active players table from Basketball Reference

    Returns:
        _type_: None, changes a global variable
    """
    global active_players
    active_player_url = (
        "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
    )

    try:
        response = get_wrapper(active_player_url)
        if response and response.content:
            df = create_pd_data_frame_from_html_table(
                response.content, "per_game_stats"
            )

            # Clean and process the DataFrame
            df = df[
                df["Player"] != "Player"
            ]  # Remove repeated headers within the table
            df.reset_index(drop=True, inplace=True)

            # Convert all player names to lowercase and update global variable
            active_players = [
                normalize_name(name) for name in df["Player"].str.lower().tolist()
            ]

            logging.info("Active players list set successfully.")
    except Exception as e:
        logging.error(
            f"Error fetching active players from {active_player_url}. Exception: {e}"
        )


def auto_correct_player_name(first_name: str, last_name: str) -> List[str]:
    """
    Auto corrects a package input to a web scraped database

    Args:
        first_name (str): First name of a basketball player
        last_name (str): Last name of a basketball player

    Returns:
        List[str]: A list containing first and last name of a player
    """
    global active_players

    if not active_players:
        scrape_active_players()  # Ensure active players list is populated

    full_name_input = normalize_name(f"{first_name} {last_name}")

    corrected_player_name, score, _ = process.extractOne(
        full_name_input, active_players
    )

    # --- Threshold for Similarity Score ---
    if score > 70:
        return corrected_player_name.split(" ")
    else:
        logging.error(f"No match found for: {last_name}, {first_name}")
        return None


# Basic Suffix Formula: <first_letter_of_last_name>/<first_five_letters_of_last_name><first_two_letters_of_first_name><unique_id>
def create_player_suffix(first_name: str, last_name: str, unique_id: str) -> str:
    """
    Utilizes the Suffix Formula above to construct the Basketball Reference Player Suffix

    Args:
        first_name (str): First Name of a Player
        last_name (str): Last Name of a Player
        unique_id (str): Unique ID for a Player (Used in the case of if two players have the same suffix)

    Returns:
        str: Basketball Reference Suffix
    """
    # Process last name
    last_name_part = last_name[:5].lower()
    if len(last_name) > 1:
        last_name_prefix = last_name[0].lower()
    else:
        last_name_prefix = ""

    # Process first name
    first_name_part = first_name[:2].lower()

    # Construct suffix
    suffix = f"{last_name_prefix}/{last_name_part}{first_name_part}{unique_id}"

    return suffix
