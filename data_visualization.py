import pandas as pd
import plotly.express as px

# Read the CSV file into a DataFrame
df = pd.read_csv('twitch_streams.csv', encoding='latin1')

# Group the data by game name and language and count the number of streams in each group
grouped_data = df.groupby(['game_name', 'language']).size().unstack(fill_value=0).reset_index()

# Melt the DataFrame to prepare for Plotly's bar chart
melted_data = pd.melt(grouped_data, id_vars='game_name', var_name='language', value_name='Number of Streams')

# Create a grouped bar chart using Plotly Express
fig = px.bar(melted_data, x='game_name', y='Number of Streams', color='language',
             labels={'game_name': 'ゲーム名', 'Number of Streams': '配信数'},
             title='ゲーム名と言語別のストリーム数')

# Update layout for better readability
fig.update_layout(xaxis_tickangle=-45, xaxis=dict(tickfont=dict(size=8)))

# Show the plot
fig.show()
