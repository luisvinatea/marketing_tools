# A quick tool to find who is not following you back on instagram

Could be useful for digital marketing campaign managers, or to ensure requirements for a giveaway are being followed, without risking to use third party acess to the app, which could have your account restricted or banned.

Just request the csv file from Accounts Center containing the data from your user account and replace it inside the read_csv function.

Have fun!


````
pip install openpyxl
import pandas as pd

# Load the CSV files
following_df = pd.read_csv('following.csv')
followers_df = pd.read_csv('followers.csv')

# Drop NaN values
following_df = following_df.dropna().reset_index(drop=True)
followers_df = followers_df.dropna().reset_index(drop=True)

# Define a regular expression pattern to match valid usernames
username_pattern = r'^[a-z0-9._]+$'

# Filter rows that match the username pattern
following_df = following_df[following_df['Following'].str.contains(username_pattern, na=False)]
followers_df = followers_df[followers_df['Followers'].str.contains(username_pattern, na=False)]

# Display the cleaned DataFrames to verify
print(following_df.head())
print(followers_df.head())

# Create sets of usernames from each file
following_usernames = set(following_df['Following'])
followers_usernames = set(followers_df['Followers'])

# Find usernames in 'following' but not in 'followers'
unfollowers = following_usernames - followers_usernames

# Create a DataFrame to display the result
unfollowers_df = pd.DataFrame(list(unfollowers), columns=['username'])

# Display the DataFrame with all rows
unfollowers_df
    
# Save the unfollowers DataFrame to an Excel file
unfollowers_df.to_excel('unfollowers_list.xlsx', index=False)

print("The list of unfollowers has been exported to 'unfollowers_list.xlsx'.")
````

    
