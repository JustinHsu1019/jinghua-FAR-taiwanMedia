import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------
# 1) Read CSV
# ---------------------------------------------------------------
df = pd.read_csv('result.csv')

# Optional: convert the 'date' column to datetime
# df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d')

# ---------------------------------------------------------------
# 2) Plotting: Political Bias
# ---------------------------------------------------------------
# Create a pivot table
pivot_bias = df.pivot_table(
    index=['Media', 'date'],
    columns='Political Bias',   # e.g., "Biased" vs. "Not biased" vs. "neutral"
    values='ID',
    aggfunc='count',
    fill_value=0
).reset_index()

# Melt into long format
df_bias_melted = pivot_bias.melt(
    id_vars=['Media', 'date'],
    var_name='Political_Bias',
    value_name='Count'
)

# Facet by date so each date is a separate subplot
g_bias = sns.catplot(
    data=df_bias_melted,
    x='Media',
    y='Count',
    hue='Political_Bias',
    col='date',
    kind='bar',
    height=5,
    aspect=1
)
g_bias.set_xticklabels(rotation=45)
g_bias.fig.suptitle("Political Bias: Number of Articles by Media, Date", y=1.02)
g_bias.tight_layout()
plt.show()

# ---------------------------------------------------------------
# 3) Plotting: Evidence Objectivity
# ---------------------------------------------------------------
pivot_obj = df.pivot_table(
    index=['Media', 'date'],
    columns='Evidence Objectivity',  # e.g., "Subjective" vs. "Objective"
    values='ID',
    aggfunc='count',
    fill_value=0
).reset_index()

df_obj_melted = pivot_obj.melt(
    id_vars=['Media', 'date'],
    var_name='Objectivity',
    value_name='Count'
)

g_obj = sns.catplot(
    data=df_obj_melted,
    x='Media',
    y='Count',
    hue='Objectivity',
    col='date',
    kind='bar',
    height=5,
    aspect=1
)
g_obj.set_xticklabels(rotation=45)
g_obj.fig.suptitle("Evidence Objectivity: Number of Articles by Media, Date", y=1.02)
g_obj.tight_layout()
plt.show()

# ---------------------------------------------------------------
# 4) Plotting: Emotional Intensity
# ---------------------------------------------------------------
pivot_emo = df.pivot_table(
    index=['Media', 'date'],
    columns='Emotional Intensity',   # e.g., "High" vs. "Medium"
    values='ID',
    aggfunc='count',
    fill_value=0
).reset_index()

df_emo_melted = pivot_emo.melt(
    id_vars=['Media', 'date'],
    var_name='Emotion',
    value_name='Count'
)

g_emo = sns.catplot(
    data=df_emo_melted,
    x='Media',
    y='Count',
    hue='Emotion',
    col='date',
    kind='bar',
    height=5,
    aspect=1
)
g_emo.set_xticklabels(rotation=45)
g_emo.fig.suptitle("Emotional Intensity: Number of Articles by Media, Date", y=1.02)
g_emo.tight_layout()
plt.show()

# ---------------------------------------------------------------
# 5) Creating Summary Tables in Markdown
# ---------------------------------------------------------------
# (A) Detailed summary table
group_cols = [
    'Media',
    'date',
    'Political Bias',
    'Evidence Objectivity',
    'Emotional Intensity'
]
df_summary = df.groupby(group_cols).size().reset_index(name='Count')
df_summary_markdown = df_summary.to_markdown(
    index=False,
    tablefmt="github"
)

# (B) Wide pivot table
df_wide = df_summary.pivot_table(
    index=['Media', 'date'],
    columns=['Political Bias', 'Evidence Objectivity', 'Emotional Intensity'],
    values='Count',
    fill_value=0
).reset_index()
df_wide_markdown = df_wide.to_markdown(
    index=False,
    tablefmt="github"
)

# ---------------------------------------------------------------
# 6) Print the two tables, separated by "============="
# ---------------------------------------------------------------
print(df_summary_markdown)
print("=============")
print(df_wide_markdown)
