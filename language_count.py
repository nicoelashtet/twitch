import requests
import csv

# Replace 'YOUR_CLIENT_ID' with your actual Twitch Client ID
client_id = ''

# Replace 'YOUR_OAUTH_TOKEN' with your actual Twitch OAuth token
oauth_token = ''

# Set the API endpoint for getting live streams
endpoint = 'https://api.twitch.tv/helix/streams'

# Set headers with necessary information, including the authentication token
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {oauth_token}'
}

# Initialize an empty list to store stream data
low_viewer_streams = []

# Function to get follower count for a user
def get_follower_count(user_id):
    follower_endpoint = f'https://api.twitch.tv/helix/users/follows?to_id={user_id}'
    response = requests.get(follower_endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['total']
    return 0  # Default value if follower count cannot be fetched

# Define a list of languages to retrieve data for (e.g., 'ja' for Japanese and 'en' for English)
languages = ['ja', 'en','es','pt','ru','ko']

for language in languages:
    # Set parameters for the API request with the current language
    params = {
        'first': 100,  # Maximum number of streams per page
        'language': language,
        'type': 'live',  # Only retrieve live streams
        'sort': 'viewers'  # Sort by viewers in descending order
    }

    # Iterate through pages of results
    while True:
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()

            if data.get('data'):
                for stream in data['data']:
                    if stream['viewer_count'] > 1000:
                        user_id = stream['user_id']
                        user_login = stream['user_login']
                        user_name = stream['user_name']
                        game_id = stream['game_id']
                        game_name = stream['game_name']
                        title = stream['title']
                        viewer_count = stream['viewer_count']
                        follower_count = get_follower_count(user_id)
                        language = stream['language']

                        low_viewer_streams.append({
                            'user_login': user_login,
                            'game_name': game_name,
                            'title': title,
                            'viewer_count': viewer_count,
                            'follower_count': follower_count,
                            'language': language
                        })

            # Check if there are more pages
            if 'cursor' in data.get('pagination', {}):
                params['after'] = data['pagination']['cursor']
            else:
                break
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

# Save the data to a CSV file
csv_filename = 'twitch_streams.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['user_login', 'game_name', 'title', 'viewer_count', 'follower_count', 'language']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for stream in low_viewer_streams:
        writer.writerow(stream)

print(f'Data saved to {csv_filename}')
