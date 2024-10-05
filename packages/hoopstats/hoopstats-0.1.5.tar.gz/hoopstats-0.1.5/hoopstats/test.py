from hoopstats import PlayerScraper
import matplotlib.pyplot as plt


"""
The purpose of this file is to test the package code locally.
It provides a way to execute and verify functionality during development,
but should not be used as part of the package's core functionality or deployment.

@Calvin Min 2024
"""


def main():
    print("NBA Player Stats Fetcher")

    while True:
        try:
            # Continuously ask for input
            name = (
                input("Enter player name or type 'exit' to quit): ").strip().split(" ")
            )
            if name[0].lower() == "exit":
                print("Exiting program.")
                break

            playerScraper = PlayerScraper(name[0], name[1])

            stat_type = input(
                "Enter stat type (e.g., 'per_game', 'totals', 'advanced'): "
            ).strip()

            # Fetch and display player stats
            if stat_type:
                # Fetch player stats based on type
                data_frame = playerScraper.get_stats_by_year(stat_type=stat_type)

                if data_frame.empty:
                    print(f"No data found for {stat_type}.")
                else:
                    print(data_frame)

                    visualize = (
                        input("Would you like to visualize the data? (yes/no): ")
                        .strip()
                        .lower()
                    )
                    if visualize == "yes":
                        # Create a basic plot from the DataFrame
                        filtered_data = data_frame[
                            ~data_frame["Season"].str.contains("Career", na=False)
                        ]
                        filtered_data.plot(kind="bar", x="Season", figsize=(10, 6))
                        plt.title(
                            f"{name[0]} {name[1]} - {stat_type.capitalize()} Stats"
                        )
                        plt.xlabel("Season")
                        plt.ylabel("PTS")
                        plt.tight_layout()
                        plt.show()
            else:
                print(playerScraper.get_stats_by_year())

            print(playerScraper.get_game_log_by_year(2024))
        except KeyboardInterrupt:
            print("\nKeyboard exit. Exiting program.")
            break


if __name__ == "__main__":
    main()
