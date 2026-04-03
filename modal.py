# # -----------------my code-----------------

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import accuracy_score

# # Load data
# matches = pd.read_csv("ipl dataset/matches.csv")

# # Clean data
# data = matches[['team1','team2','toss_winner','toss_decision','winner']].dropna()
# data = data[data['winner'] != 'no result']
# data = data[(data['winner'] == data['team1']) | (data['winner'] == data['team2'])]

# # TARGET (binary)
# data['result'] = (data['winner'] == data['team1']).astype(int)

# # ENCODING
# le = LabelEncoder()
# for col in ['team1','team2','toss_winner']:
#     data[col] = le.fit_transform(data[col])

# data['toss_decision'] = data['toss_decision'].map({'bat':0,'field':1})

# # FEATURES
# X = data[['team1','team2','toss_winner','toss_decision']]
# y = data['result']

# # SPLIT (IMPORTANT CHANGE)
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.3, random_state=0
# )

# # MODEL (BOOSTING = better)
# model = GradientBoostingClassifier(
#     n_estimators=200,
#     learning_rate=0.1,
#     max_depth=5
# )

# model.fit(X_train, y_train)

# # Prediction
# y_pred = model.predict(X_test)

# # Accuracy
# acc = accuracy_score(y_test, y_pred)
# print("FINAL ACCURACY:", acc)








# # ----------dataleak-----------------

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import accuracy_score

# # ---------------- LOAD DATA ----------------
# matches = pd.read_csv("ipl dataset/matches.csv")

# # ---------------- CLEAN DATA ----------------
# data = matches[['team1','team2','toss_winner','toss_decision','winner']].dropna()

# data = data[data['winner'] != 'no result']
# data = data[(data['winner'] == data['team1']) | (data['winner'] == data['team2'])]

# # ---------------- TARGET ----------------
# data['result'] = (data['winner'] == data['team1']).astype(int)

# # ======================================================
# # 🔥 PARTIAL LEAKAGE FEATURE
# # ======================================================

# # winner ka indirect use (semi-leakage)
# data['winner_encoded'] = data['winner']

# # ---------------- ENCODING ----------------
# le = LabelEncoder()
# for col in ['team1','team2','toss_winner','winner_encoded']:
#     data[col] = le.fit_transform(data[col])

# data['toss_decision'] = data['toss_decision'].map({'bat':0,'field':1})

# # ---------------- FEATURES ----------------
# X = data[['team1','team2','toss_winner','toss_decision','winner_encoded']]

# y = data['result']

# # ---------------- SPLIT ----------------
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.3, random_state=42
# )

# # ---------------- MODEL ----------------
# model = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42)
# model.fit(X_train, y_train)

# # ---------------- PREDICT ----------------
# y_pred = model.predict(X_test)

# # ---------------- ACCURACY ----------------
# acc = accuracy_score(y_test, y_pred)
# print("ACCURACY:", acc)




