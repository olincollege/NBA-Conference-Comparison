import matplotlib.pyplot as plt
import pandas as pd


def plot_wins_over_40_from_csv(seasons_back):
    """
    Plot the aggregated number of wins over 40 by conference from a CSV file.

    Args:
        seasons_back (int): The number of past seasons to include in the plot.

    This function reads aggregated data from a CSV file and plots the number of
    wins over 40 for the Eastern and Western Conferences.
    """
    # Construct the CSV filename from the number of seasons back
    csv_filename = f"data/aggregated_wins_over_40_last_{seasons_back}_seasons.csv"

    # Read the aggregated data from the CSV file
    data = pd.read_csv(csv_filename, index_col=0)

    # Plot the data
    fig, ax = plt.subplots()
    data.plot(kind="bar", ax=ax, rot=0)

    # Customize the plot with labels and title
    ax.set_ylabel("Wins Over 40")
    ax.set_title(
        f"Aggregated Wins Over 40 by Conference for the Last {seasons_back} Seasons"
    )
    ax.legend()

    # Show the plot
    plt.show()


def plot_conference_win_loss_records_from_csv(seasons_back):
    """
    Plot the win-loss records by conference from a CSV file.

    Args:
        seasons_back (int): The number of past seasons to include in the plot.

    This function reads win-loss records from a CSV file and plots them for the
    Eastern and Western Conferences.
    """
    csv_filename = f"data/conference_win_loss_records_last_{seasons_back}_seasons.csv"
    data = pd.read_csv(csv_filename, index_col=0)

    # Prepare data for plotting
    east_wins = data.loc["Eastern Conference", "Wins"]
    west_wins = data.loc["Western Conference", "Wins"]

    # Set up the bar chart
    fig, ax = plt.subplots()
    ax.bar("Eastern Conference", east_wins, label="Eastern Conference")
    ax.bar("Western Conference", west_wins, label="Western Conference")

    # Add some text for labels and title
    ax.set_ylabel("Wins")
    ax.set_title(
        f"NBA Win-Loss Records by Conference Over the Past {seasons_back} Seasons"
    )
    ax.legend()

    plt.show()


def plot_inter_conference_win_loss_records_from_csv(seasons_back):
    """
    Plot the inter-conference win-loss records from a CSV file.

    Args:
        seasons_back (int): The number of past seasons to include in the plot.

    This function reads inter-conference win-loss records from a CSV file and
    plots them, showing the performance of Eastern and Western Conferences
    against each other.
    """
    csv_filename = (
        f"data/inter_conference_win_loss_records_last_{seasons_back}_seasons.csv"
    )
    data = pd.read_csv(csv_filename, index_col=0)

    fig, ax = plt.subplots()
    data.plot(kind="bar", ax=ax, stacked=True)

    ax.set_ylabel("Number of Games")
    ax.set_title(
        f"NBA Inter-Conference Win-Loss Records Over the Last {seasons_back} Seasons"
    )
    ax.legend()

    plt.show()


def plot_hof_by_conference_from_csv(
    csv_filename="data/hall_of_famers_by_conference.csv",
):
    """
    Plot the number of Hall of Famers by conference from a CSV file.

    Args:
        csv_filename (str): The path to the CSV file containing the data.
                            Defaults to 'data/hall_of_famers_by_conference.csv'

    This function reads the number of Hall of Famers for each conference from a
    CSV file and plots them.
    """
    data = pd.read_csv(csv_filename)
    data.set_index("Conference", inplace=True)
    data.plot(kind="bar")
    plt.ylabel("Number of Hall of Famers")
    plt.title("Number of Hall of Famers by Conference")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def plot_championships_by_conference_from_csv(
    csv_filename="data/championships_by_conference.csv",
):
    """
    Plot the number of NBA championships by conference from a CSV file.

    Args:
        csv_filename (str): The path to the CSV file containing the data.
                            Defaults to 'data/championships_by_conference.csv'.

    This function reads the number of NBA championships won by each conference
    from a CSV file and plots them.
    """
    # Read the championships data from the CSV file
    data = pd.read_csv(csv_filename)

    # Set up the bar chart
    fig, ax = plt.subplots()
    ax.bar(data["Conference"], data["Championships"], color=["blue", "red"])

    # Add some text for labels and title
    ax.set_ylabel("Number of Championships")
    ax.set_title("NBA Championships by Conference")
    ax.set_xticks(data["Conference"])
    ax.set_xticklabels(data["Conference"])

    # Show the plot
    plt.show()
