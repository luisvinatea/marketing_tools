# A quick tool to find who is not following you back on instagram

Could be useful for digital marketing campaign managers, or to ensure requirements for a giveaway are being followed, without risking to use third party acess to the app, which could have your account restricted or banned.

Just request the csv file from Accounts Center containing the data from your user account and replace it inside the read_csv function.

Have fun!


```python
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
```

               Following
    1           wtfelixx
    3  _tamiresalmeida03
    5           maa.brrt
    7    taisevieirarosa
    9           shaamay1
             Followers
    0     thais.viiera
    2  taisevieirarosa
    4  kari_delprado._
    6         choas_11
    8      mariarosinn
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>username</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>insolito.pe</td>
    </tr>
    <tr>
      <th>1</th>
      <td>tanta_peru</td>
    </tr>
    <tr>
      <th>2</th>
      <td>topclosings</td>
    </tr>
    <tr>
      <th>3</th>
      <td>brasofficiel</td>
    </tr>
    <tr>
      <th>4</th>
      <td>enissonfotos</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>617</th>
      <td>luigi.di.domenico</td>
    </tr>
    <tr>
      <th>618</th>
      <td>jkundee</td>
    </tr>
    <tr>
      <th>619</th>
      <td>janhartwig_official</td>
    </tr>
    <tr>
      <th>620</th>
      <td>isadora.dantasm</td>
    </tr>
    <tr>
      <th>621</th>
      <td>jeffim_rueda</td>
    </tr>
  </tbody>
</table>
<p>622 rows × 1 columns</p>
</div>




```python
!pip install openpyxl

# Save the unfollowers DataFrame to an Excel file
unfollowers_df.to_excel('unfollowers_list.xlsx', index=False)

print("The list of unfollowers has been exported to 'unfollowers_list.xlsx'.")
```

    Collecting openpyxl
      Downloading openpyxl-3.1.2-py2.py3-none-any.whl.metadata (2.5 kB)
    Collecting et-xmlfile (from openpyxl)
      Downloading et_xmlfile-1.1.0-py3-none-any.whl.metadata (1.8 kB)
    Downloading openpyxl-3.1.2-py2.py3-none-any.whl (249 kB)
       ---------------------------------------- 0.0/250.0 kB ? eta -:--:--
       - -------------------------------------- 10.2/250.0 kB ? eta -:--:--
       ---- ---------------------------------- 30.7/250.0 kB 435.7 kB/s eta 0:00:01
       --------- ----------------------------- 61.4/250.0 kB 544.7 kB/s eta 0:00:01
       --------------------- ---------------- 143.4/250.0 kB 944.1 kB/s eta 0:00:01
       ---------------------------------------  245.8/250.0 kB 1.2 MB/s eta 0:00:01
       ---------------------------------------- 250.0/250.0 kB 1.1 MB/s eta 0:00:00
    Downloading et_xmlfile-1.1.0-py3-none-any.whl (4.7 kB)
    Installing collected packages: et-xmlfile, openpyxl
    Successfully installed et-xmlfile-1.1.0 openpyxl-3.1.2
    The list of unfollowers has been exported to 'unfollowers_list.xlsx'.
    
