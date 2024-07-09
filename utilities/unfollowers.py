# A quick tool to find who is not following you back on Instagram

pip install openpyxl
import pandas as pd

def load_and_clean_csv(file_path, column_name, username_pattern):
    """
    Load a CSV file and clean the data by removing NaN values and filtering
    rows that match a valid username pattern.

    Parameters:
    file_path (str): Path to the CSV file.
    column_name (str): Name of the column containing usernames.
    username_pattern (str): Regular expression pattern to match valid usernames.

    Returns:
    pd.DataFrame: Cleaned DataFrame.
    """
    df = pd.read_csv(file_path)
    df = df.dropna().reset_index(drop=True)
    df = df[df[column_name].str.contains(username_pattern, na=False)]
    return df

# Load the CSV files
following_df = load_and_clean_csv('following.csv', 'Following', r'^[a-z0-9._]+$')
followers_df = load_and_clean_csv('followers.csv', 'Followers', r'^[a-z0-9._]+$')

# Display the cleaned DataFrames to verify
print(following_df.head())
print(followers_df.head())

def find_unfollowers(following, followers):
    """
    Find usernames that are in the 'following' list but not in the 'followers' list.

    Parameters:
    following (set): Set of usernames you are following.
    followers (set): Set of usernames that are following you.

    Returns:
    set: Set of usernames that are not following you back.
    """
    return following - followers

# Create sets of usernames from each file
following_usernames = set(following_df['Following'])
followers_usernames = set(followers_df['Followers'])

# Find usernames in 'following' but not in 'followers'
unfollowers = find_unfollowers(following_usernames, followers_usernames)

# Create a DataFrame to display the result
unfollowers_df = pd.DataFrame(list(unfollowers), columns=['username'])

# Display the DataFrame with all rows
print(unfollowers_df)

def export_to_excel(df, file_name):
    """
    Export a DataFrame to an Excel file.

    Parameters:
    df (pd.DataFrame): DataFrame to be exported.
    file_name (str): Name of the Excel file to save the DataFrame.
    """
    df.to_excel(file_name, index=False)
    print(f"The list of unfollowers has been exported to '{file_name}'.")

# Save the unfollowers DataFrame to an Excel file
export_to_excel(unfollowers_df, 'unfollowers_list.xlsx')
