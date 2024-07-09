# Finding the Most Cost Effective Marketing Strategy for Inca Sushi

## Understanding Meta's Definition of Page Engagement

Meta (formerly Facebook) defines "Page Engagement" as a broad metric that encompasses various types of interactions users can have with a Facebook or Instagram page. This metric is designed to capture the full range of activities users perform that indicate their interest and interaction with the page's content.

### Types of Page Engagements

- **Likes:** Users liking the page itself or individual posts/photos.
- **Comments:** Users commenting on posts, photos, or videos.
- **Shares:** Users sharing posts, photos, or videos to their own or others' timelines.
- **Reactions:** Users reacting to posts, photos, or videos with different reaction types (e.g., Love, Haha, Wow, Sad, Angry).
- **Clicks:** Link clicks on the content, including "See More" clicks to expand posts, clicks on the page name or profile picture, and clicks to play a video.
- **Video Views:** Users viewing a video for a specific duration (typically 3 seconds or more).
- **Photo Views:** Users viewing photos or albums.
- **Post Saves:** Users saving posts for later viewing.
- **Message Sends:** Users sending messages to the page through Messenger or Instagram Direct.
- **Follows:** Users following the page to receive updates in their feed.

### Implications for the Restaurant's Advertising Strategy

Given the broad definition of page engagement, focusing on maximizing this metric can provide a comprehensive view of how users are interacting with the page. For the restaurant, this means that activities like liking posts, commenting, sharing, clicking on links, watching videos, and sending messages all contribute to the engagement metric.

## Some Data Cleaning

```python
df_campaigns = pd.read_csv('campaigns_inca_sushi.csv')

df_copy = df_campaigns

# Apply renaming of columns
df_copy.rename(columns={
    'Nome da campanha': 'Campaign Name',
    'Alcance': 'Reach',
    'Impressões': 'Impressions',
    'Valor usado (BRL)': 'Investment',
    'Custo por 1.000 contas da Central de Contas alcançadas (BRL)': 'CPR (1K)',
    'CPM (custo por 1.000 impressões) (BRL)': 'CPM (1K)',
    'Engajamento com a Página': 'Page Engagement',
    'Engajamentos com a publicação': 'Post Engagement',
    'Reações à publicação': 'Post Reactions',
    'Incrementalidade estimada na lembrança do anúncio (pessoas)': 'Ad Recall Lift',
    'Objetivo': 'Objective'
}, inplace=True)
```

### Creating a Total Ad Duration Column

```python
# Calculate the duration between 'Data de criação' and 'Data da última edição', convert to days
df_copy['Duration'] = (pd.to_datetime(df_campaigns['Data da última edição'], format='%Y-%m-%d') - 
                            pd.to_datetime(df_campaigns['Data de criação'], format='%Y-%m-%d')).dt.days

# Drop the original date columns
df_copy.drop(columns=['Data de criação', 'Data da última edição'], inplace=True)
df_copy.drop(columns=['Início dos relatórios', 'Término dos relatórios'], inplace=True)
print(df_copy.head())
```

| Campaign Name            | Reach | Impressions | Investment | CPR (1K) | CPM (1K) | Page Engagement | Post Engagement | Post Reactions | Ad Recall Lift | Objective   | Duration |
|--------------------------|-------|-------------|------------|----------|----------|-----------------|-----------------|----------------|----------------|-------------|----------|
| Publicação do Instagram: | 1908  | 1947        | 7.52       | 15.26    | 7.997904 | 81              | 9.0             | NaN            | NaN            | Tráfego     | 0        |
| Publicação do Instagram: | 998   | 1010        | 3.40       | 11.764706| 11.564626| 25.0            | 4.0             | NaN            | NaN            | Tráfego     | 0        |
| Inca Sushi Culinária     | 289   | 294         | 27.41      | 8.541602 | 8.218891 | 25.0            | 25.0            | NaN            | NaN            | Engajamento | 1        |
| Publicação do Instagram: | 3209  | 3335        | 85.83      | 14.813600| 13.360834| 275.0           | 25.0            | NaN            | NaN            | Tráfego     | 1        |
| SITE                     | 5794  | 6424        | 7.535070   | 7.445545 | 8.91     | 4.0             | 275.0           | NaN            | NaN            | Tráfego     | 52       |

```python
# Identify columns with more than 30 non-null values
columns_to_keep = df_copy.count()[df_campaigns.count() > 30].index

# Keep only those columns in the DataFrame
df_copy = df_copy[columns_to_keep]

# Verify the filtered DataFrame
print(df_copy.info())
```

| Column            | Non-Null Count | Dtype   |
|-------------------|----------------|---------|
| Campaign Name     | 37 non-null    | object  |
| Reach             | 37 non-null    | int64   |
| Impressions       | 37 non-null    | int64   |
| Investment        | 37 non-null    | float64 |
| CPR (1K)          | 37 non-null    | float64 |
| CPM (1K)          | 37 non-null    | float64 |
| Page Engagement   | 37 non-null    | float64 |
| Post Engagement   | 37 non-null    | float64 |
| Post Reactions    | 37 non-null    | float64 |
| Ad Recall Lift    | 37 non-null    | int64   |
| Objective         | 37 non-null    | object  |
| Duration          | 37 non-null    | int64   |
dtypes: float64(6), int64(4), object(2)

### Creating a Campaign Sub-objective

```python
# Relocate and rename columns 
columns_order = ['Objective', 'Duration', 'Investment', 'Reach', 'Impressions', 'Page Engagement', 
                 'Post Engagement', 'Post Reactions', 'Ad Recall Lift', 'CPR (1K)', 'CPM (1K)', 'Campaign Name']
df_copy = df_copy[columns_order]

# Map the strategy labels
def map_strategy(value):
    value = value.upper()
    if "MENSAGEM" in value or "ENGAJAMENTO" in value:
        return "Leads"
    elif "ALCANCE" in value or "CAPTAÇÃO" in value:
        return "Growth"
    elif "PERSEGUIÇÃO" in value:
        return "Remarketing"
    elif any(term in value for term in ["TRÁFEGO", "VENDAS", "VENDER", "SITE", "EBOOK", "MENUDINO"]):
        return "Visitors"
    else:
        return "Followers"

df_copy['Strategy'] = df_copy['Campaign Name'].apply(map_strategy)

# Drop the 'Campaign Name' column as it's no longer needed
df_copy.drop(columns=['Campaign Name'], inplace=True)

# Relabel the objectives to English
objective_mapping = {
    'Engajamento': 'Engagement',
    'Reconhecimento': 'Awareness',
    'Tráfego': 'Traffic',
    'Vendas': 'Sales'
}

df_copy['Objective'] = df_copy['Objective'].replace(objective_mapping)
```

### Ranking of Strategies

```python
# Calculate cost per page engagement
df_copy.loc[:, 'Cost per Page Engagement'] = df_copy['Investment'] / df_copy['Page Engagement']
df_copy.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace infinite values with NaN
df_copy.dropna(subset=['Cost per Page Engagement'], inplace=True)  # Drop rows with NaN values in the cost per page engagement

# Filter the DataFrame for "Traffic" and "Engagement" objectives
df_filtered = df_copy[df_copy['Objective'].isin(['Traffic', 'Engagement'])]

# Aggregate the cost per page engagement for each objective and strategy combination
df_grouped_cost = df_copy.groupby(['Objective', 'Strategy']).agg({
    'Cost per Page Engagement': 'mean'
}).reset_index()

# Rank the strategies by cost per page engagement
cost_effective_ranking = df_grouped_cost.sort_values(by='Cost per Page Engagement').reset_index(drop=True)

# Display the ranking
print(cost_effective_ranking)
```

### Ranking of Strategies by Duration

```python
# Aggregate total days running for each strategy (including all objectives)
df_grouped_days = df_copy.groupby(['Objective', 'Strategy']).agg({
    'Duration': 'sum',
}).reset_index()

# Rank the strategies by duration 
days_ranking = df_grouped_days.sort_values(by='Duration', ascending=False).reset_index(drop=True)

# Display the ranking
print(days_ranking)
```

| Objective   | Strategy    | Cost per Page Engagement |            | Objective   | Strategy   | Duration |
|-------------|-------------|--------------------------|------------|-------------|------------|----------|
| Engagement  | Followers   | 0.136000                 |            |             |            |          |
| Traffic     | Visitors    | 0.359822                 |            | Engagement  | Leads      | 228      |
| Sales       | Visitors    | 0.500712                 |            | Awareness   | Remarketing| 107      |
| Awareness   | Growth      | 0.670714                 |            | Traffic     | Followers  | 88       |
| Engagement  | Leads       | 0.743987                 |            | Sales       | Visitors   | 71       |
| Traffic     | Followers   | 0.786665                 |            | Awareness   | Growth     | 26       |
| Engagement  | Growth      | 1.439375                 |            | Traffic     | Growth     | 17       |
| Traffic     | Growth      | 1.781022                 |            | Engagement  | Growth     | 10       |
| Awareness   | Remarketing | 1.857752                 |            | Engagement  | Followers  | 1        |

### Identify the Most Cost-Effective Strategy

```python
most_cost_effective_strategy = cost_effective_ranking.iloc[0]
most_cost_effective_cost_per_engagement = most_cost_effective_strategy['Cost per Page Engagement']

# Calculate the total amount spent
total_investment = df_copy['Investment'].sum()

# Calculate potential savings
current_total_engagements = df_copy['Page Engagement'].sum()
potential_total_engagements = total_investment / most_cost_effective_cost_per_engagement

# Calculate the additional engagements
additional_engagements = potential_total_engagements - current_total_engagements

# Calculate savings
total_spent_on_effective_strategy = current_total_engagements * most_cost_effective_cost_per_engagement
savings = total_investment - total_spent_on_effective_strategy

# Calculate the percentage savings
percentage_savings = (savings / total_investment) * 100

# Print the results
print(f"Most cost-effective strategy: {most_cost_effective_strategy['Strategy']} for {most_cost_effective_strategy['Objective']}")
print(f"Total investment: {total_investment:.2f} BRL")
print(f"Total saved: {savings:.2f} BRL")
print(f"Percentage saved: {percentage_savings:.2f}%")
print(f"Current total page engagements: {current_total_engagements}")
print(f"Potential total page engagements: {potential_total_engagements:.2f}")
print(f"Additional page engagements: {additional_engagements:.2f}")
```

## Analysis Summary

### Most Cost-Effective Strategy

- **Most cost-effective strategy:** Followers for Engagement
- **Total investment:** 11,985.45 BRL
- **Potential savings:** 4,588.26 BRL
- **Percentage savings:** 38.28%
- **Current total page engagements:** 54,391.09
- **Potential total page engagements:** 88,128.31
- **Additional page engagements:** 33,737.22
---  
For this restaurant, if the primary goal was to grow its followers, focusing solely on using the **"Boost Post"** button on Instagram would have been significantly more cost-effective. The analysis revealed that the most cost-effective strategy was the **"Followers"** strategy for the **"Engagement"** objective, achieved through Instagram's **"Boost Post"** function.

If the entire advertising budget of 11,985.45 BRL had been allocated to this strategy, the restaurant could have saved approximately **38.28%** of its total investment. This would have resulted in a total saving of **4,588.26 BRL**. Additionally, the number of page engagements would have increased substantially. Instead of the current total of **54,391** page engagements, the potential total could have reached **88,128**, yielding an additional **33,737** page engagements.

This analysis underscores the effectiveness and efficiency of using Instagram's **"Boost Post"** button for growing followers and engaging with a broader audience, offering significant savings and better engagement outcomes compared to other strategies.

By reallocating the advertising budget to the most cost-effective strategy, the restaurant could have maximized its return on investment and achieved better engagement results with a lower expenditure. This highlights the potential benefits of focusing on the most cost-effective advertising strategies to achieve desired business outcomes while optimizing marketing expenditures.
