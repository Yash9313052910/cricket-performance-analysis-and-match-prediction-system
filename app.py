import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# ---------------- PAGE ----------------
st.set_page_config(page_title="Cricket Performance Analysis and Match Prediction System")

st.markdown("""
<h1 style='text-align:center; color:#0E4D92; font-size:36px;'>
🏏 Cricket Performance Analysis and Match Prediction System
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; padding:10px; background-color:#f0f2f6; border-radius:10px;'>
<h4>Analyze team performance and predict match outcomes using IPL data</h4>
</div>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
matches = pd.read_csv("ipl dataset/matches.csv")
deliveries = pd.read_csv("ipl dataset/deliveries.csv")

team_map = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Kings XI Punjab': 'Punjab Kings',
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru'
}

matches.replace(team_map, inplace=True)
deliveries.replace(team_map, inplace=True)

data = matches[['id','team1','team2','toss_winner','toss_decision','winner','date']].dropna()
data = data[data['winner'] != 'no result']
data = data[(data['winner'] == data['team1']) | (data['winner'] == data['team2'])]

data['year'] = pd.to_datetime(data['date']).dt.year
teams = sorted(list(set(data['team1'])))

data['result'] = (data['winner'] == data['team1']).astype(int)
data['toss_team1'] = (data['toss_winner'] == data['team1']).astype(int)

le = LabelEncoder()
for col in ['team1','team2','toss_winner']:
    data[col] = le.fit_transform(data[col])

data['toss_decision'] = data['toss_decision'].map({'bat':0,'field':1})

X = data[['team1','team2','toss_winner','toss_decision','toss_team1','year']]
y = data['result']

model = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42)
model.fit(X, y)

# ======================================================
# 🔮 MATCH PREDICTION (UNCHANGED)
# ======================================================

st.markdown("---")
st.subheader("Match Prediction")

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Team 1", teams)
    team2 = st.selectbox("Team 2", teams)

with col2:
    toss_winner = st.selectbox("Toss Winner", [team1, team2])
    toss_decision = st.selectbox("Toss Decision", ["bat", "field"])

year = st.selectbox("Year", sorted(data['year'].unique()))

if team1 == team2:
    st.error("Same team selected")
    st.stop()

if st.button("Predict Winner"):
    input_data = [[
        le.transform([team1])[0],
        le.transform([team2])[0],
        le.transform([toss_winner])[0],
        0 if toss_decision == "bat" else 1,
        1 if toss_winner == team1 else 0,
        year
    ]]

    pred = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0]

    if pred == 1:
        winner = team1
        confidence = prob[1]
    else:
        winner = team2
        confidence = prob[0]

    st.success("Predicted Winner: " + winner)
    st.progress(float(confidence))
    st.write("Confidence:", round(confidence*100,2), "%")

# ---------------- HEAD TO HEAD ----------------
st.markdown("### Head-to-Head Comparison")

h2h = matches[
    ((matches['team1'] == team1) & (matches['team2'] == team2)) |
    ((matches['team1'] == team2) & (matches['team2'] == team1))
]

if h2h.shape[0] == 0:
    st.warning("No head-to-head matches found")
else:
    st.write("Total Matches:", h2h.shape[0])
    st.write(team1, "Wins:", h2h[h2h['winner']==team1].shape[0])
    st.write(team2, "Wins:", h2h[h2h['winner']==team2].shape[0])

# ======================================================
# 📊 PERFORMANCE ANALYSIS
# ======================================================

st.markdown("---")
st.subheader("Performance Analysis")

data_merge = deliveries.merge(matches[['id','date']], left_on='match_id', right_on='id')
data_merge['year'] = pd.to_datetime(data_merge['date']).dt.year

year_sel = st.selectbox("Select Year", sorted(data_merge['year'].unique()))

bat1 = data_merge[(data_merge['year']==year_sel) & (data_merge['batting_team']==team1)]
bowl1 = data_merge[(data_merge['year']==year_sel) & (data_merge['bowling_team']==team1)]

bat2 = data_merge[(data_merge['year']==year_sel) & (data_merge['batting_team']==team2)]
bowl2 = data_merge[(data_merge['year']==year_sel) & (data_merge['bowling_team']==team2)]

# -------- GRAPH FUNCTION --------
def plot_bar(series):
    fig, ax = plt.subplots(figsize=(10,4))
    series.plot(kind='bar', ax=ax)
    plt.xticks(rotation=30, ha='right')
    st.pyplot(fig)

# ================= TEAM 1 =================
st.markdown(f"### {team1}")

st.write("Top Batsmen")
top_bat1 = bat1.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(5)
plot_bar(top_bat1)

st.markdown("---")

st.write("Strike Rate")
bat_stats1 = bat1.groupby('batter').agg({'batsman_runs':'sum','ball':'count'}).reset_index()
bat_stats1 = bat_stats1[bat_stats1['ball'] >= 30]
bat_stats1['sr'] = (bat_stats1['batsman_runs']/bat_stats1['ball'])*100
plot_bar(bat_stats1.sort_values(by='sr', ascending=False).head(5).set_index('batter')['sr'])

st.markdown("---")

st.write("Top Bowlers")
top_bowl1 = bowl1[(bowl1['is_wicket']==1) & (bowl1['dismissal_kind']!='run out')]
top_bowl1 = top_bowl1.groupby('bowler')['is_wicket'].count().sort_values(ascending=False).head(5)
plot_bar(top_bowl1)

st.markdown("---")

st.write("Economy")
bowl_stats1 = bowl1.groupby('bowler').agg({'total_runs':'sum','ball':'count'}).reset_index()
bowl_stats1 = bowl_stats1[bowl_stats1['ball'] >= 30]
bowl_stats1['overs'] = bowl_stats1['ball']/6
bowl_stats1['eco'] = bowl_stats1['total_runs']/bowl_stats1['overs']
plot_bar(bowl_stats1.sort_values(by='eco').head(5).set_index('bowler')['eco'])

# BEST PERFORMANCE
st.markdown("### Best Performance")

best_bat1 = f"{top_bat1.idxmax()} ({int(top_bat1.max())} runs)" if not top_bat1.empty else "N/A"
best_bowl1 = f"{top_bowl1.idxmax()} ({int(top_bowl1.max())} wickets)" if not top_bowl1.empty else "N/A"
best_sr1 = bat_stats1.sort_values(by='sr', ascending=False)['batter'].iloc[0] if not bat_stats1.empty else "N/A"
best_eco1 = bowl_stats1.sort_values(by='eco')['bowler'].iloc[0] if not bowl_stats1.empty else "N/A"

st.success(f"Best Batsman: {best_bat1}")
st.success(f"Best Bowler: {best_bowl1}")
st.info(f"Best Strike Rate: {best_sr1}")
st.info(f"Best Economy: {best_eco1}")

# ================= TEAM 2 =================
st.markdown(f"### {team2}")

st.write("Top Batsmen")
top_bat2 = bat2.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(5)
plot_bar(top_bat2)

st.markdown("---")

st.write("Strike Rate")
bat_stats2 = bat2.groupby('batter').agg({'batsman_runs':'sum','ball':'count'}).reset_index()
bat_stats2 = bat_stats2[bat_stats2['ball'] >= 30]
bat_stats2['sr'] = (bat_stats2['batsman_runs']/bat_stats2['ball'])*100
plot_bar(bat_stats2.sort_values(by='sr', ascending=False).head(5).set_index('batter')['sr'])

st.markdown("---")

st.write("Top Bowlers")
top_bowl2 = bowl2[(bowl2['is_wicket']==1) & (bowl2['dismissal_kind']!='run out')]
top_bowl2 = top_bowl2.groupby('bowler')['is_wicket'].count().sort_values(ascending=False).head(5)
plot_bar(top_bowl2)

st.markdown("---")

st.write("Economy")
bowl_stats2 = bowl2.groupby('bowler').agg({'total_runs':'sum','ball':'count'}).reset_index()
bowl_stats2 = bowl_stats2[bowl_stats2['ball'] >= 30]
bowl_stats2['overs'] = bowl_stats2['ball']/6
bowl_stats2['eco'] = bowl_stats2['total_runs']/bowl_stats2['overs']
plot_bar(bowl_stats2.sort_values(by='eco').head(5).set_index('bowler')['eco'])

# BEST PERFORMANCE TEAM 2
st.markdown("### Best Performance")

best_bat2 = f"{top_bat2.idxmax()} ({int(top_bat2.max())} runs)" if not top_bat2.empty else "N/A"
best_bowl2 = f"{top_bowl2.idxmax()} ({int(top_bowl2.max())} wickets)" if not top_bowl2.empty else "N/A"
best_sr2 = bat_stats2.sort_values(by='sr', ascending=False)['batter'].iloc[0] if not bat_stats2.empty else "N/A"
best_eco2 = bowl_stats2.sort_values(by='eco')['bowler'].iloc[0] if not bowl_stats2.empty else "N/A"

st.success(f"Best Batsman: {best_bat2}")
st.success(f"Best Bowler: {best_bowl2}")
st.info(f"Best Strike Rate: {best_sr2}")
st.info(f"Best Economy: {best_eco2}")