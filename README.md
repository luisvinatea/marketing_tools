<h1>Finding the Most Cost Effective Marketing Strategy For Inca Sushi</h1>

<h2>Understanding Meta's Definition of Page Engagement</h2>
<p class="italic">Meta (formerly Facebook) defines "Page Engagement" as a broad metric that encompasses various types of interactions users can have with a Facebook or Instagram page. This metric is designed to capture the full range of activities users perform that indicate their interest and interaction with the page's content.</p>

<h3>Types of Page Engagements</h3>
<div class="highlight">
  <ul>
    <li><strong>Likes:</strong> Users liking the page itself / Users liking individual posts or photos.</li>
    <li><strong>Comments:</strong> Users commenting on posts, photos, or videos.</li>
    <li><strong>Shares:</strong> Users sharing posts, photos, or videos to their own or others' timelines.</li>
    <li><strong>Reactions:</strong> Users reacting to posts, photos, or videos with different reaction types (e.g., Love, Haha, Wow, Sad, Angry).</li>
    <li><strong>Clicks:</strong> Link clicks on the content, including "See More" clicks to expand posts / Clicks on the page name or profile picture / Clicks to play a video.</li>
    <li><strong>Video Views:</strong> Users viewing a video for a specific duration (typically 3 seconds or more).</li>
    <li><strong>Photo Views:</strong> Users viewing photos or albums.</li>
    <li><strong>Post Saves:</strong> Users saving posts for later viewing.</li>
    <li><strong>Message Sends:</strong> Users sending messages to the page through Messenger or Instagram Direct.</li>
    <li><strong>Follows:</strong> Users following the page to receive updates in their feed.</li>
  </ul>
</div>

<h3>Implications for the Restaurant's Advertising Strategy</h3>
<p>Given the broad definition of page engagement, focusing on maximizing this metric can provide a comprehensive view of how users are interacting with the page. For the restaurant, this means that activities like liking posts, commenting, sharing, clicking on links, watching videos, and sending messages all contribute to the engagement metric.</p>

<h2>Some Data Cleaning</h2>


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
| Campaign Name            | Reach | Impressions | Investment | CPR (1K) | CPM (1K) | Page Engagement | Comentários na publicação | Post Engagement | informações de pagamento offline | informações de pagamento no app para celular | Valor de conversão de adições de informações de pagamento |  adições das informações de pagamento offline | Pedidos  | COMPRAS | Valor de conversão de Pedidos| Valor de conversão de COMPRAS | Objective   | Duration      |
|--------------------------|-------|-------------|------------|----------|----------|-----------------|---------------------------|---------------- |----------------------------------|----------------------------------------------|-----------------------------------------------------------|-----------------------------------------------|----------|---------|------------------------------|-------------------------------|-------------|---------------|
| Publicação do Instagram: | 1908  | 1947        | 7.52       | 15.26    | 7.997904 | 81              | NaN                       | 9.0             | NaN                              | NaN                                          | NaN                                                       | NaN                                           | NaN      | NaN     | NaN                          | NaN                           | Tráfego     | 0             |
| Publicação do Instagram: | 998   | 1010        | 3.40       | 11.764706| 11.564626| 25.0            | NaN                       | 4.0             | NaN                              | NaN                                          | NaN                                                       | NaN                                           | NaN      | NaN     | NaN                          | NaN                           | Tráfego     | 0             |
| Inca Sushi Culinária     | 289   | 294         | 27.41      | 8.541602 | 8.218891 | 25.0            | NaN                       | 25.0            | NaN                              | NaN                                          | NaN                                                       | NaN                                           | NaN      | NaN     | NaN                          | NaN                           | Engajamento | 1             |
| Publicação do Instagram: | 3209  | 3335        | 85.83      | 14.813600| 13.360834| 275.0           | NaN                       | 25.0            | NaN                              | NaN                                          | NaN                                                       | NaN                                           | NaN      | NaN     | NaN                          | NaN                           | Tráfego     | 1             |
| SITE                     | 5794  | 6424        | 7.535070   | 7.445545 | 8.91     | 4.0             | NaN                       | 275.0           | NaN                              | NaN                                          | NaN                                                       | NaN                                           | NaN      | NaN     | NaN                          | NaN                           | Tráfego     | 52            |
| Campanha de vendas       | 79    | 81          | 27.67      | 8.541602 | 7.99790  | 294             | NaN                       | NaN             | NaN                              | NaN                                          | NaN                                                       | NaN                                           | NaN      | NaN     | NaN                          | NaN                           | Vendas      | 10            |


```python
# Identify columns with more than 30 non-null values
columns_to_keep = df_copy.count()[df_campaigns.count() > 30].index

# Keep only those columns in the DataFrame
df_copy = df_copy[columns_to_keep]

# Verify the filtered DataFrame
print(df_copy.info())
```

| Column            | Non-Null Count | Dtype   |
|------------------ |----------------|---------|
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
<table>
<tr>
  <th>Objective</th>
  <th>Strategy</th>
  <th>Cost per Page Engagement</th>
  <th></th>
  <th>Objective</th>
  <th>Strategy</th>
  <th>Duration</th>
</tr>
<tr>
  <td>Engagement</td>
  <td>Followers</td>
  <td>0.136000</td>
  <td></td>
  <td>Traffic</td>
  <td>Visitors</td>
  <td>284</td>
</tr>
<tr>
  <td>Traffic</td>
  <td>Visitors</td>
  <td>0.359822</td>
  <td></td>
  <td>Engagement</td>
  <td>Leads</td>
  <td>228</td>
</tr>
<tr>
  <td>Sales</td>
  <td>Visitors</td>
  <td>0.500712</td>
  <td></td>
  <td>Awareness</td>
  <td>Remarketing</td>
  <td>107</td>
</tr>
<tr>
  <td>Awareness</td>
  <td>Growth</td>
  <td>0.670714</td>
  <td></td>
  <td>Traffic</td>
  <td>Followers</td>
  <td>88</td>
</tr>
<tr>
  <td>Engagement</td>
  <td>Leads</td>
  <td>0.743987</td>
  <td></td>
  <td>Sales</td>
  <td>Visitors</td>
  <td>71</td>
</tr>
<tr>
  <td>Traffic</td>
  <td>Followers</td>
  <td>0.786665</td>
  <td></td>
  <td>Awareness</td>
  <td>Growth</td>
  <td>26</td>
</tr>
<tr>
  <td>Engagement</td>
  <td>Growth</td>
  <td>1.439375</td>
  <td></td>
  <td>Traffic</td>
  <td>Growth</td>
  <td>17</td>
</tr>
<tr>
  <td>Traffic</td>
  <td>Growth</td>
  <td>1.781022</td>
  <td></td>
  <td>Engagement</td>
  <td>Growth</td>
  <td>10</td>
</tr>
<tr>
  <td>Awareness</td>
  <td>Remarketing</td>
  <td>1.857752</td>
  <td></td>
  <td>Engagement</td>
  <td>Followers</td>
  <td>1</td>
</tr>
</table>

### Identify the most cost-effective strategy

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
<h3>Analysis Summary</h3>

<h4>Most Cost-Effective Strategy</h4>

<p><strong>Most cost-effective strategy:</strong> Followers for Engagement<br>
<strong>Total investment:</strong> 11,985.45 BRL<br>
<strong>Potential savings:</strong> 4,588.26 BRL<br>
<strong>Percentage savings:</strong> 38.28%<br>
<strong>Current total page engagements:</strong> 54,391.09<br>
<strong>Potential total page engagements:</strong> 88,128.31<br>
<strong>Additional page engagements:</strong> 33,737.22<br></p>

<p>For this restaurant, if the primary goal was to grow its followers, focusing solely on using the <strong>"Boost Post"</strong> button on Instagram would have been significantly more cost-effective. The analysis revealed that the most cost-effective strategy was the <strong>"Followers"</strong> strategy for the <strong>"Engagement"</strong> objective, achieved through Instagram's <strong>"Boost Post"</strong> function.</p>

<p>If the entire advertising budget of 11,985.45 BRL had been allocated to this strategy, the restaurant could have saved approximately <strong>38.28%</strong> of its total investment. This would have resulted in a total saving of <strong>4,588.26 BRL</strong>. Additionally, the number of page engagements would have increased substantially. Instead of the current total of <strong>54,391</strong> page engagements, the potential total could have reached <strong>88,128</strong>, yielding an additional <strong>33,737</strong> page engagements.</p>

<p>This analysis underscores the effectiveness and efficiency of using Instagram's <strong>"Boost Post"</strong> button for growing followers and engaging with a broader audience, offering significant savings and better engagement outcomes compared to other strategies.</p>

<p>By reallocating the advertising budget to the most cost-effective strategy, the restaurant could have maximized its return on investment and achieved better engagement results with a lower expenditure.</p>

<p>This highlights the potential benefits of focusing on the most cost-effective advertising strategies to achieve desired business outcomes while optimizing marketing expenditures.</p>
