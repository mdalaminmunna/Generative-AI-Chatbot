import sqlite3
from datetime import datetime
import plotly.express as px
import pandas as pd

def get_interaction_data():
    conn = sqlite3.connect('database/chatbot.db')
    query = "SELECT * FROM interaction"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def generate_analytics():
    df = get_interaction_data()

    #Convert timestamp for visualization
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    #Generate analytics (Number of interactions over time)
    fig = px.line(
        df,
        x="timestamp",
        y="df.index",
        title="User Interactions Over Time",
        labels={'y': 'Number of Interactions', 'x': 'Timestamp'}
    )
    fig.show()