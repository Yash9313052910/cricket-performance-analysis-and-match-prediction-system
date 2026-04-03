import pandas as pd
import matplotlib.pyplot as plt

# ---------------- LOAD DATA ----------------
# Load matches and deliveries dataset
matches = pd.read_csv("ipl dataset/matches.csv")
deliveries = pd.read_csv("ipl dataset/deliveries.csv")


# ---------------- TEAM NAME CLEANING ----------------
# Old team names ko new names se replace karna
team_map = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Kings XI Punjab': 'Punjab Kings'
}

# Apply mapping on both datasets
matches.replace(team_map, inplace=True)
deliveries.replace(team_map, inplace=True)


# ---------------- GRAPH FUNCTION ----------------
# Reusable function to plot clean bar graphs
def plot_graph(series, title):

    plt.figure(figsize=(16,6))  # graph ka size bada rakha for clarity

    series.plot(kind='bar')  # bar chart create

    # X-axis labels rotate + right align (name cut na ho)
    plt.xticks(rotation=30, ha='right', fontsize=10)

    plt.title(title, fontsize=16)  # graph title

    plt.tight_layout()  # spacing auto adjust

    plt.savefig(title + ".png")  # graph image save (PPT ke liye)

    plt.show()  # graph display


# ================================
# 🔥 TOP BATSMEN (TOTAL RUNS)
# ================================

# Har batsman ke total runs calculate
top_batsman = deliveries.groupby('batter')['batsman_runs'].sum()

# Descending order me sort karke top 10 select
top_batsman = top_batsman.sort_values(ascending=False).head(10)

# Graph plot
plot_graph(top_batsman, "Top 10 Batsmen (Runs - All IPL)")


# ================================
# ⚡ STRIKE RATE (REALISTIC)
# ================================

# Batsman ke runs + total balls calculate
bat_stats = deliveries.groupby('batter').agg({
    'batsman_runs': 'sum',
    'ball': 'count'
}).reset_index()

# Filter: sirf wo players jinhone minimum 300 balls kheli
bat_stats = bat_stats[bat_stats['ball'] >= 300]

# Strike rate formula apply
bat_stats['strike_rate'] = (bat_stats['batsman_runs'] / bat_stats['ball']) * 100

# Top 10 strike rate players
top_sr = bat_stats.sort_values(by='strike_rate', ascending=False).head(10)

# Graph plot
plot_graph(top_sr.set_index('batter')['strike_rate'], "Top 10 Strike Rate (Min 300 balls)")


# ================================
# 🎯 TOP BOWLERS (WICKETS)
# ================================

# Sirf wicket deliveries filter karo
wickets = deliveries[deliveries['is_wicket'] == 1]

# Bowler ke total wickets count
top_bowlers = wickets.groupby('bowler')['is_wicket'].count()

# Top 10 bowlers
top_bowlers = top_bowlers.sort_values(ascending=False).head(10)

# Graph plot
plot_graph(top_bowlers, "Top 10 Bowlers (Wickets)")


# ================================
# 💰 ECONOMY RATE (REALISTIC)
# ================================

# Bowler ke runs conceded + balls bowled
bowl_stats = deliveries.groupby('bowler').agg({
    'total_runs': 'sum',
    'ball': 'count'
}).reset_index()

# Filter: minimum 300 balls (random bowlers hatao)
bowl_stats = bowl_stats[bowl_stats['ball'] >= 300]

# Overs calculate (6 balls = 1 over)
bowl_stats['overs'] = bowl_stats['ball'] / 6

# Economy formula
bowl_stats['economy'] = bowl_stats['total_runs'] / bowl_stats['overs']

# Best economy (lowest values)
top_eco = bowl_stats.sort_values(by='economy').head(10)

# Graph plot
plot_graph(top_eco.set_index('bowler')['economy'], "Top 10 Economy (Min 300 balls)")


# ================================
# 🏏 TEAM TOTAL RUNS
# ================================

# Har team ke total runs
team_runs = deliveries.groupby('batting_team')['batsman_runs'].sum()

# Descending order me sort
team_runs = team_runs.sort_values(ascending=False)

# Graph plot
plot_graph(team_runs, "Team Total Runs (All IPL)")