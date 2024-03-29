# NBA Conference Comparison
## Summary
We analyzed NBA franchise team and player data to determine which conference is better, the Eastern or Western Conference based on the following criteria metrics:
- Performance
- Awards
- Intangibles
NBA statistics were plotted and stored in the folder labeled `data`. See `essay.ipynb` for a full breakdown of the project in computational essay format.
## Installation
**Necessary Libraries:**
1. pandas
2. matplotlib
3. datetime
4. nba_api
## Data Obtaining and Plotting Instructions
To obtain the necessary data for this project, follow these steps:
1. **NBA API Usage:**  
   - Install the `nba_api` package using pip:  
     ```
     pip install nba_api
     ```  
   - Utilize endpoints such as `LeagueStandings`, `LeagueGameFinder`, `TeamDetails`, and `FranchiseHistory` to fetch data.  
   - Example call to fetch standings data:  

from nba_api.stats.endpoints import leaguestandings

standings = leaguestandings.LeagueStandings(season='2022-23')

standings_df = standings.get_data_frames()[0]


2. **Seasons Data:**  
   - Specify the NBA seasons you are interested in, formatted as 'YYYY-YY' (e.g., '2022-23').  
   - Use these season identifiers when calling the API to retrieve data for the desired seasons.  
3. **Storing Data:**  
   - After fetching data, it can be saved to CSV files for later use, aiding in analysis and plot generation.
   - Example of saving to CSV:  

     ```
standings_df.to_csv('nba_standings_2022_23.csv')

     ```  
### Generating Plots
To generate plots as shown in the computational essay, follow these instructions:  
1. **Plotting Functions:**  
   - Use matplotlib to generate plots from the aggregated data.  
   - Functions like `plot_conference_win_loss_records_from_csv` or `plot_wins_over_40_from_csv` can be used to read the stored CSV data and generate plots.  
   - All plotting functions can be found in the `plots.py` file.  
   - Example to generate a plot:  

import matplotlib.pyplot as plt

def plot_data_from_csv(csv_file):

    data = pd.read_csv(csv_file, index_col=0)

    data.plot(kind='bar')

    plt.show()

2. **Visualization:**  
   - Customize your plots with titles, labels, and legends to make the data easily understandable.  
   - Save the plots using `plt.savefig('filename.png')` if you need to include them in your essay or reports.  
3. **Execution:**  
   - Ensure all required libraries are installed and import them at the beginning of your program.  
   - Execute your plotting functions after the data has been aggregated and stored in CSV files.  

By following these steps, you can successfully obtain the necessary NBA data and generate insightful plots!