atributos_extremo = ['Participação', 'Pressão na linha alta', 'Impacto do passe', 
                'Movimentação ofensiva', 'Drible', 'Efetividade',  
                    'Criação de oportunidades', 'Ameaça ofensiva',
                    'Finalização']


# Dynamically create the HTML string with the 'jogadores' variable
title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"
# Use the dynamically created HTML string in st.markdown
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Participação</h3>", unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[72, 73, 31, 74]].reset_index(drop=True)
metrics_participação_1 = metrics.iloc[:, 0].tolist()
metrics_participação_2 = metrics.iloc[:, 1].tolist()
metrics_participação_3 = metrics.iloc[:, 2].tolist()
metrics_participação_4 = metrics.iloc[:, 3].tolist()
metrics_y = [0] * len(metrics_participação_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[72, 73, 31, 74]].reset_index(drop=True)
highlight_participação_1 = highlight.iloc[:, 0].tolist()
highlight_participação_2 = highlight.iloc[:, 1].tolist()
highlight_participação_3 = highlight.iloc[:, 2].tolist()
highlight_participação_4 = highlight.iloc[:, 3].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_participação_1_value = pd.DataFrame(highlight_participação_1).reset_index(drop=True)
highlight_participação_2_value = pd.DataFrame(highlight_participação_2).reset_index(drop=True)
highlight_participação_3_value = pd.DataFrame(highlight_participação_3).reset_index(drop=True)
highlight_participação_4_value = pd.DataFrame(highlight_participação_4).reset_index(drop=True)

highlight_participação_1_value = highlight_participação_1_value.iat[0,0]
highlight_participação_2_value = highlight_participação_2_value.iat[0,0]
highlight_participação_3_value = highlight_participação_3_value.iat[0,0]
highlight_participação_4_value = highlight_participação_4_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                    metrics_participação_3, metrics_participação_4])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                    metrics_participação_3, metrics_participação_4])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função'] == "Extremo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe, clube):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[(filtered_df['Atleta'] == player_name) & (filtered_df['Clube'] == clube)]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
participação_1_ranking_value = (get_player_rank(jogadores, liga, "xG gerado na construção (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({participação_1_ranking_value}/{rows_count})"
full_title_participação_1 = f"xG gerado na construção (p90) {output_str} {highlight_participação_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
participação_2_ranking_value = (get_player_rank(jogadores, liga, "Toques (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({participação_2_ranking_value}/{rows_count})"
full_title_participação_2 = f"Toques (p90) {output_str} {highlight_participação_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
participação_3_ranking_value = (get_player_rank(jogadores, liga, "Ações defensivas (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({participação_3_ranking_value}/{rows_count})"
full_title_participação_3 = f"Ações defensivas (p90) {output_str} {highlight_participação_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
participação_4_ranking_value = (get_player_rank(jogadores, liga, "Disputas aéreas (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({participação_4_ranking_value}/{rows_count})"
full_title_participação_4 = f"Disputas aéreas (p90) {output_str} {highlight_participação_4_value}"

##############################################################################################################
##############################################################################################################
#From Claude version2

def calculate_ranks(values):
    """Calculate ranks for a given metric, with highest values getting rank 1"""
    return pd.Series(values).rank(ascending=False).astype(int).tolist()

def prepare_data(tabela_a, metrics_cols):
    """Prepare the metrics data dictionary with all required data"""
    metrics_data = {}
    
    for col in metrics_cols:
        # Store the metric values
        metrics_data[f'metrics_{col}'] = tabela_a[col].tolist()
        # Calculate and store ranks
        metrics_data[f'ranks_{col}'] = calculate_ranks(tabela_a[col])
        # Store player names
        metrics_data[f'player_names_{col}'] = tabela_a['Atleta'].tolist()
    
    return metrics_data

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value, equipe):
    """
    Create an interactive plot showing player attributes with hover information
    
    Parameters:
    tabela_a (pd.DataFrame): DataFrame containing all player data
    jogadores (str): Name of the player to highlight
    min_value (float): Minimum value for x-axis
    max_value (float): Maximum value for x-axis
    """
    # List of metrics to plot
    metrics_list = [
        'xG gerado na construção (p90)', 'Toques (p90)', 
        'Ações defensivas (p90)','Disputas aéreas (p90)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data with additional filtering for Clube
    highlight_data = {
        f'highlight_{metric}': tabela_a[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)][metric].iloc[0]
        for metric in metrics_list
    }

    highlight_ranks = {
        metric: int(
            pd.Series(tabela_a[metric]).rank(ascending=False)[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)].iloc[0]
        )
        for metric in metrics_list
    }
    
    # Total number of players
    total_players = len(tabela_a)
    
    # Create subplots
    fig = make_subplots(
        rows=9, 
        cols=1,
        subplot_titles=[
            f"{metric.capitalize()} ({highlight_ranks[metric]}/{total_players}) {highlight_data[f'highlight_{metric}']:.2f}"
            for metric in metrics_list
        ],
        vertical_spacing=0.04
    )

    # Update subplot titles font size and color
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=17, color='black')

    # Add traces for each metric
    for idx, metric in enumerate(metrics_list, 1):
        # Add scatter plot for all players
        fig.add_trace(
            go.Scatter(
                x=metrics_data[f'metrics_{metric}'],
                y=[0] * len(metrics_data[f'metrics_{metric}']),
                mode='markers',
                name='Demais Jogadores',
                marker=dict(color='deepskyblue', size=8),
                text=[f"{rank}/{total_players}" for rank in metrics_data[f'ranks_{metric}']],
                customdata=metrics_data[f'player_names_{metric}'],
                hovertemplate='%{customdata}<br>Rank: %{text}<br>Value: %{x:.2f}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )
        
        # Add highlighted player point
        fig.add_trace(
            go.Scatter(
                x=[highlight_data[f'highlight_{metric}']],
                y=[0],
                mode='markers',
                name=jogadores,
                marker=dict(color='blue', size=12),
                hovertemplate=f'{jogadores}<br>Rank: {highlight_ranks[metric]}/{total_players}<br>Value: %{{x:.2f}}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )

    # Get the total number of metrics (subplots)
    n_metrics = len(metrics_list)

    # Update layout for each subplot
    for i in range(1, n_metrics + 1):
        if i == n_metrics:  # Only for the last subplot
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=False,
                ticktext=["PIOR", "MÉDIA (0)", "MELHOR"],
                tickvals=[min_value/2, 0, max_value/2],
                tickmode='array',
                ticks="outside",
                ticklen=2,
                tickfont=dict(size=16),
                tickangle=0,
                side='bottom',
                automargin=False,
                row=i, 
                col=1
            )
            # Adjust layout for the last subplot
            fig.update_layout(
                xaxis_tickfont_family="Arial",
                margin=dict(b=0)  # Reduce bottom margin
            )
        else:  # For all other subplots
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                showline=False,
                showticklabels=False,  # Hide tick labels
                row=i, 
                col=1
            )  # Reduces space between axis and labels

        # Update layout for the entire figure
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            showline=False,
            row=i, 
            col=1
        )

    # Update layout for the entire figure
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.23,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        margin=dict(t=100)
    )

    # Add x-axis label at the bottom
    fig.add_annotation(
        text="Desvio-padrão",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.32,
        showarrow=False,
        font=dict(size=16, color='black', weight='bold')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_participação_1), min(metrics_participação_2), 
min(metrics_participação_3), min(metrics_participação_4),
])  # Add padding of 0.5

max_value_test = max([
max(metrics_participação_1), max(metrics_participação_2), 
max(metrics_participação_3), max(metrics_participação_4),
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value,    # Maximum value for x-axis
    equipe = equipe
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################
    
#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&
                                            (attribute_chart_per['Liga']==liga)&(attribute_chart_per['Temporada']==temporada) & 
                                            (attribute_chart_per['função']=="Extremo") & (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[52, 53, 11, 54]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[72, 73, 31, 74]].reset_index(drop=True)
metrics_percent = pd.concat([metrics, percent]).reset_index(drop=True)
#metrics_percent.rename(columns={'Atleta': 'Métricas'}, inplace=True)
metrics_percent = metrics_percent.transpose()
# Rename specific columns while keeping 'Métricas' column unchanged
metrics_percent = metrics_percent.rename(columns={
    metrics_percent.columns[0]: f'Métricas',
    metrics_percent.columns[1]: f'Percentil na Liga'
})
#st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)

# Define function to color and label cells in the "Percentil na Liga" column
def color_percentil(val):
    """
    Apply color styling based on percentile value
    """
    # Color maps from Matplotlib
    cmap = plt.get_cmap('Blues')
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")
    
    try:
        # Convert to float in case it's a string or other type
        val_num = float(val)
        
        if pd.isna(val_num):
            return ''  # No styling for NaN values
        elif val_num >= 90:
            color = cmap2(0.70)  # "Elite"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 75 <= val_num < 90:
            color = cmap2(0.50)  # "Destaque"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 60 <= val_num < 75:
            color = cmap(0.50)  # "Razoável"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 40 <= val_num < 60:
            color = cmap(0.25)  # "Mediano"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 20 <= val_num < 40:
            color = cmap1(0.30)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        else:
            color = cmap1(0.50)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
    except (ValueError, TypeError):
        return ''

# Define the styling for the entire table
styles = [
    dict(selector="th", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("color", "#333333"),
        ("font-weight", "bold"),
        ("padding", "12px 15px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black"),  # Heavier horizontal line under headers
        ("background-color", "white")
    ]),
    dict(selector="td", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("padding", "2px 5px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black")  # Horizontal lines between rows
    ]),
    # Center align specific columns
    dict(selector="th:nth-child(2), th:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="td:nth-child(2), td:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="", props=[
        ("border", "none"),  # Remove table border
        ("border-collapse", "collapse"),
        ("box-shadow", "0px 1px 3px rgba(0,0,0,0.1)")
    ]),
    # Remove vertical grid lines by not defining them
    dict(selector="tbody tr:nth-child(even)", props=[
        ("background-color", "white")
    ]),
    # Remove table outline
    dict(selector="table", props=[
        ("border", "none")
    ])
]

# Apply the styling to your dataframe
styled_df = metrics_percent.style\
    .set_table_styles(styles)\
    .applymap(color_percentil, subset=['Percentil na Liga'])\
    .format({'Métricas': '{:.2f}', 'Percentil na Liga': '{:.0f}'})

# Display in Streamlit
st.table(styled_df)
# Function to plot the legend for the 5 colors from the Blues colormap
st.markdown("<br><h5 style='text-align: center;'>Legenda Baseada no Percentil do Jogador na Liga</h5>", unsafe_allow_html=True)

def plot_color_legend():
    # Custom colors for the categories (using the same logic as in apply_colormap_based_on_value)
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    # Assign colors using the same logic
    colors = [
        cmap2(0.70),   # "Elite"
        cmap2(0.50),  # "Destaque"
        cmap(0.50),   # "Razoável"
        cmap(0.25),  # "Mediano"
        cmap1(0.30), # "Frágil"
        cmap1(0.50)  # "Péssimo"
    ]
    
    # Labels for the legend (highest to lowest)
    labels = ['Elite (>=90)', 'Destaque (75-90)', 'Razoável (60-75)', 'Mediano (40-60)', 'Frágil (20-40)', 'Péssimo (<20)']

    # Plot the legend horizontally with a smaller size
    fig, ax = plt.subplots(figsize=(6, 0.3))  # Smaller layout
    for i, (label, color) in enumerate(zip(labels[::-1], colors[::-1])):  # Reverse labels for display
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))  # Draw rectangle
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=6.0)  # Add text inside the rectangles

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Remove axes

    # Add an arrow pointing from "Highest" to "Lowest"
    ax.annotate('', xy=(6, 1), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.04, width=1.2, headwidth=5))

    return fig

# Call the function to plot the legend and display it in Streamlit
legend_fig = plot_color_legend()
st.pyplot(legend_fig)


##################################################################################################################### 
#####################################################################################################################

#Plotar Terceiro Gráfico - Radar de Métricas x Média da liga:
st.markdown(f"<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em {temporada}</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)& 
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo") & 
                                    (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 52, 53, 11, 54]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[52, 53, 11, 54]]
metrics_mean['xG gerado na construção (p90)'] = metrics_mean['xG gerado na construção (p90)'].mean()
metrics_mean['Toques (p90)'] = metrics_mean['Toques (p90)'].mean()
metrics_mean['Ações defensivas (p90)'] = metrics_mean['Ações defensivas (p90)'].mean()
metrics_mean['Disputas aéreas (p90)'] = metrics_mean['Disputas aéreas (p90)'].mean()

# Keep only the first row
metrics_mean = metrics_mean.iloc[:1]

metrics_mean['Atleta'] = 'Média da Liga' 
metrics_mean.insert(0, 'Atleta', metrics_mean.pop('Atleta'))

#Concatenate both dataframes
metrics = pd.concat([metrics, metrics_mean]).reset_index(drop=True)
metrics_list = metrics.iloc[0].tolist()
#Collecting clube
clube = attribute_chart.iat[0, 5]
posição = attribute_chart.iat[0, 8]

## parameter names
params = list(metrics.columns)
params = params[1:]

#Preparing Data
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(attribute_chart_2[params][x])
    a = a
    b = max(attribute_chart_2[params][x])
    b = b
    ranges.append((a, b))

for x in range(len(metrics['Atleta'])):
    if metrics['Atleta'][x] == jogadores:
        a_values = metrics.iloc[x].values.tolist()
    if metrics['Atleta'][x] == 'Média da Liga':
        b_values = metrics.iloc[x].values.tolist()
            
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values, b_values]

#Plotting Data
title = dict(
    title_name = jogadores,
    title_color = '#B6282F',
    title_name_2 = 'Média da Liga',
    title_color_2 = '#344D94',
    title_fontsize = 18,
) 

endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are posadj, per90'
radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
plt.savefig('Player&League_Comparison.png')
st.pyplot(fig)

##################################################################################################################### 
#####################################################################################################################

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Pressão na Linha Alta </h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
#Renaming columns
attribute_chart_z.rename(columns={'counterpressing': 'Contra-pressão (p90)'}, inplace=True)

# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[70, 69, 82, 83]].reset_index(drop=True)
metrics_pressão_1 = metrics.iloc[:, 0].tolist()
metrics_pressão_2 = metrics.iloc[:, 1].tolist()
metrics_pressão_3 = metrics.iloc[:, 2].tolist()
metrics_pressão_4 = metrics.iloc[:, 3].tolist()
metrics_y = [0] * len(metrics_pressão_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[70, 69, 82, 83]].reset_index(drop=True)
highlight_pressão_1 = highlight.iloc[:, 0].tolist()
highlight_pressão_2 = highlight.iloc[:, 1].tolist()
highlight_pressão_3 = highlight.iloc[:, 2].tolist()
highlight_pressão_4 = highlight.iloc[:, 3].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_pressão_1_value = pd.DataFrame(highlight_pressão_1).reset_index(drop=True)
highlight_pressão_2_value = pd.DataFrame(highlight_pressão_2).reset_index(drop=True)
highlight_pressão_3_value = pd.DataFrame(highlight_pressão_3).reset_index(drop=True)
highlight_pressão_4_value = pd.DataFrame(highlight_pressão_4).reset_index(drop=True)

highlight_pressão_1_value = highlight_pressão_1_value.iat[0,0]
highlight_pressão_2_value = highlight_pressão_2_value.iat[0,0]
highlight_pressão_3_value = highlight_pressão_3_value.iat[0,0]
highlight_pressão_4_value = highlight_pressão_4_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_pressão_1, metrics_pressão_2, 
                                    metrics_pressão_3, metrics_pressão_4])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_pressão_1, metrics_pressão_2, 
                                    metrics_pressão_3, metrics_pressão_4])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função'] == "Extremo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe, clube):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[(filtered_df['Atleta'] == player_name) & (filtered_df['Clube'] == clube)]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
pressão_1_ranking_value = (get_player_rank(jogadores, liga, "Contra-pressão (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({pressão_1_ranking_value}/{rows_count})"
full_title_pressão_1 = f"Contra-pressão (p90) {output_str} {highlight_pressão_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
pressão_2_ranking_value = (get_player_rank(jogadores, liga, "Interceptações (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({pressão_2_ranking_value}/{rows_count})"
full_title_pressão_2 = f"Interceptações (p90) {output_str} {highlight_pressão_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
pressão_3_ranking_value = (get_player_rank(jogadores, liga, "Recuperações linha alta (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({pressão_3_ranking_value}/{rows_count})"
full_title_pressão_3 = f"Recuperações linha alta (p90) {output_str} {highlight_pressão_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
pressão_4_ranking_value = (get_player_rank(jogadores, liga, "Intensidade defensiva (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({pressão_4_ranking_value}/{rows_count})"
full_title_pressão_4 = f"Intensidade defensiva (p90) {output_str} {highlight_pressão_4_value}"

##############################################################################################################
##############################################################################################################
#From Claude version2

def calculate_ranks(values):
    """Calculate ranks for a given metric, with highest values getting rank 1"""
    return pd.Series(values).rank(ascending=False).astype(int).tolist()

def prepare_data(tabela_a, metrics_cols):
    """Prepare the metrics data dictionary with all required data"""
    metrics_data = {}
    
    for col in metrics_cols:
        # Store the metric values
        metrics_data[f'metrics_{col}'] = tabela_a[col].tolist()
        # Calculate and store ranks
        metrics_data[f'ranks_{col}'] = calculate_ranks(tabela_a[col])
        # Store player names
        metrics_data[f'player_names_{col}'] = tabela_a['Atleta'].tolist()
    
    return metrics_data

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value, equipe):
    """
    Create an interactive plot showing player attributes with hover information
    
    Parameters:
    tabela_a (pd.DataFrame): DataFrame containing all player data
    jogadores (str): Name of the player to highlight
    min_value (float): Minimum value for x-axis
    max_value (float): Maximum value for x-axis
    """
    # List of metrics to plot
    metrics_list = [
        'Contra-pressão (p90)', 'Interceptações (p90)', 
        'Recuperações linha alta (p90)','Intensidade defensiva (p90)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data with additional filtering for Clube
    highlight_data = {
        f'highlight_{metric}': tabela_a[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)][metric].iloc[0]
        for metric in metrics_list
    }

    highlight_ranks = {
        metric: int(
            pd.Series(tabela_a[metric]).rank(ascending=False)[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)].iloc[0]
        )
        for metric in metrics_list
    }
    
    # Total number of players
    total_players = len(tabela_a)
    
    # Create subplots
    fig = make_subplots(
        rows=9, 
        cols=1,
        subplot_titles=[
            f"{metric.capitalize()} ({highlight_ranks[metric]}/{total_players}) {highlight_data[f'highlight_{metric}']:.2f}"
            for metric in metrics_list
        ],
        vertical_spacing=0.04
    )

    # Update subplot titles font size and color
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=17, color='black')

    # Add traces for each metric
    for idx, metric in enumerate(metrics_list, 1):
        # Add scatter plot for all players
        fig.add_trace(
            go.Scatter(
                x=metrics_data[f'metrics_{metric}'],
                y=[0] * len(metrics_data[f'metrics_{metric}']),
                mode='markers',
                name='Demais Jogadores',
                marker=dict(color='deepskyblue', size=8),
                text=[f"{rank}/{total_players}" for rank in metrics_data[f'ranks_{metric}']],
                customdata=metrics_data[f'player_names_{metric}'],
                hovertemplate='%{customdata}<br>Rank: %{text}<br>Value: %{x:.2f}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )
        
        # Add highlighted player point
        fig.add_trace(
            go.Scatter(
                x=[highlight_data[f'highlight_{metric}']],
                y=[0],
                mode='markers',
                name=jogadores,
                marker=dict(color='blue', size=12),
                hovertemplate=f'{jogadores}<br>Rank: {highlight_ranks[metric]}/{total_players}<br>Value: %{{x:.2f}}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )

    # Get the total number of metrics (subplots)
    n_metrics = len(metrics_list)

    # Update layout for each subplot
    for i in range(1, n_metrics + 1):
        if i == n_metrics:  # Only for the last subplot
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=False,
                ticktext=["PIOR", "MÉDIA (0)", "MELHOR"],
                tickvals=[min_value/2, 0, max_value/2],
                tickmode='array',
                ticks="outside",
                ticklen=2,
                tickfont=dict(size=16),
                tickangle=0,
                side='bottom',
                automargin=False,
                row=i, 
                col=1
            )
            # Adjust layout for the last subplot
            fig.update_layout(
                xaxis_tickfont_family="Arial",
                margin=dict(b=0)  # Reduce bottom margin
            )
        else:  # For all other subplots
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                showline=False,
                showticklabels=False,  # Hide tick labels
                row=i, 
                col=1
            )  # Reduces space between axis and labels

        # Update layout for the entire figure
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            showline=False,
            row=i, 
            col=1
        )

    # Update layout for the entire figure
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.38,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        margin=dict(t=100)
    )

    # Add x-axis label at the bottom
    fig.add_annotation(
        text="Desvio-padrão",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.47,
        showarrow=False,
        font=dict(size=16, color='blue', weight='bold')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_pressão_1), min(metrics_pressão_2), 
min(metrics_pressão_3), min(metrics_pressão_4),
])  # Add padding of 0.5

max_value_test = max([
max(metrics_pressão_1), max(metrics_pressão_2), 
max(metrics_pressão_3), max(metrics_pressão_4),
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value,    # Maximum value for x-axis
    equipe = equipe
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################
    
#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
# renaming columns
attribute_chart.rename(columns={'counterpressing': 'Contra-pressão (p90)'}, inplace=True)
attribute_chart_per.rename(columns={'counterpressing': 'Contra-pressão (p90)'}, inplace=True)

Lateral_Charts_1 = Lateral_Charts[(Lateral_Charts['Atleta']==jogadores)&
                                  (Lateral_Charts['Liga']==liga)&
                                    (Lateral_Charts['Temporada']==temporada)&
                                    (Lateral_Charts['Clube']==equipe) &
                                    (Lateral_Charts['função']=='Extremo')]

Lateral_Charts_2 = Lateral_Percent[(Lateral_Percent['Atleta']==jogadores)&
                                   (Lateral_Percent['Liga']==liga)&
                                    (Lateral_Percent['Temporada']==temporada)&
                                    (Lateral_Percent['Clube']==equipe)&
                                    (Lateral_Percent['função']=='Extremo')]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[50, 49, 62, 63]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[70, 69, 82, 83]].reset_index(drop=True)
metrics_percent = pd.concat([metrics, percent]).reset_index(drop=True)
#metrics_percent.rename(columns={'Atleta': 'Métricas'}, inplace=True)
metrics_percent = metrics_percent.transpose()
# Rename specific columns while keeping 'Métricas' column unchanged
metrics_percent = metrics_percent.rename(columns={
    metrics_percent.columns[0]: f'Métricas',
    metrics_percent.columns[1]: f'Percentil na Liga'
})
#st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)

# Define function to color and label cells in the "Percentil na Liga" column
def color_percentil(val):
    """
    Apply color styling based on percentile value
    """
    # Color maps from Matplotlib
    cmap = plt.get_cmap('Blues')
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")
    
    try:
        # Convert to float in case it's a string or other type
        val_num = float(val)
        
        if pd.isna(val_num):
            return ''  # No styling for NaN values
        elif val_num >= 90:
            color = cmap2(0.70)  # "Elite"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 75 <= val_num < 90:
            color = cmap2(0.50)  # "Destaque"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 60 <= val_num < 75:
            color = cmap(0.50)  # "Razoável"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 40 <= val_num < 60:
            color = cmap(0.25)  # "Mediano"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 20 <= val_num < 40:
            color = cmap1(0.30)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        else:
            color = cmap1(0.50)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
    except (ValueError, TypeError):
        return ''

# Define the styling for the entire table
styles = [
    dict(selector="th", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("color", "#333333"),
        ("font-weight", "bold"),
        ("padding", "12px 15px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black"),  # Heavier horizontal line under headers
        ("background-color", "white")
    ]),
    dict(selector="td", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("padding", "2px 5px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black")  # Horizontal lines between rows
    ]),
    # Center align specific columns
    dict(selector="th:nth-child(2), th:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="td:nth-child(2), td:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="", props=[
        ("border", "none"),  # Remove table border
        ("border-collapse", "collapse"),
        ("box-shadow", "0px 1px 3px rgba(0,0,0,0.1)")
    ]),
    # Remove vertical grid lines by not defining them
    dict(selector="tbody tr:nth-child(even)", props=[
        ("background-color", "white")
    ]),
    # Remove table outline
    dict(selector="table", props=[
        ("border", "none")
    ])
]

# Apply the styling to your dataframe
styled_df = metrics_percent.style\
    .set_table_styles(styles)\
    .applymap(color_percentil, subset=['Percentil na Liga'])\
    .format({'Métricas': '{:.2f}', 'Percentil na Liga': '{:.0f}'})

# Display in Streamlit
st.table(styled_df)
# Function to plot the legend for the 5 colors from the Blues colormap
st.markdown("<br><h5 style='text-align: center;'>Legenda Baseada no Percentil do Jogador na Liga</h5>", unsafe_allow_html=True)

def plot_color_legend():
    # Custom colors for the categories (using the same logic as in apply_colormap_based_on_value)
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    # Assign colors using the same logic
    colors = [
        cmap2(0.70),   # "Elite"
        cmap2(0.50),  # "Destaque"
        cmap(0.50),   # "Razoável"
        cmap(0.25),  # "Mediano"
        cmap1(0.30), # "Frágil"
        cmap1(0.50)  # "Péssimo"
    ]
    
    # Labels for the legend (highest to lowest)
    labels = ['Elite (>=90)', 'Destaque (75-90)', 'Razoável (60-75)', 'Mediano (40-60)', 'Frágil (20-40)', 'Péssimo (<20)']

    # Plot the legend horizontally with a smaller size
    fig, ax = plt.subplots(figsize=(6, 0.3))  # Smaller layout
    for i, (label, color) in enumerate(zip(labels[::-1], colors[::-1])):  # Reverse labels for display
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))  # Draw rectangle
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=6.0)  # Add text inside the rectangles

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Remove axes

    # Add an arrow pointing from "Highest" to "Lowest"
    ax.annotate('', xy=(6, 1), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.04, width=1.2, headwidth=5))

    return fig

# Call the function to plot the legend and display it in Streamlit
legend_fig = plot_color_legend()
st.pyplot(legend_fig)


##################################################################################################################### 
#####################################################################################################################

#Plotar Terceiro Gráfico - Radar de Métricas x Média da liga:
st.markdown(f"<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em {temporada}</h3>", unsafe_allow_html=True)

attribute_chart.rename(columns={'counterpressing': 'Contra-pressão (p90)'}, inplace=True)
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")  & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 50, 49, 62, 63]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[50, 49, 62, 63]]
metrics_mean['Contra-pressão (p90)'] = metrics_mean['Contra-pressão (p90)'].mean()
metrics_mean['Interceptações (p90)'] = metrics_mean['Interceptações (p90)'].mean()
metrics_mean['Recuperações linha alta (p90)'] = metrics_mean['Recuperações linha alta (p90)'].mean()
metrics_mean['Intensidade defensiva (p90)'] = metrics_mean['Intensidade defensiva (p90)'].mean()

# Keep only the first row
metrics_mean = metrics_mean.iloc[:1]

metrics_mean['Atleta'] = 'Média da Liga' 
metrics_mean.insert(0, 'Atleta', metrics_mean.pop('Atleta'))

#Concatenate both dataframes
metrics = pd.concat([metrics, metrics_mean]).reset_index(drop=True)
metrics_list = metrics.iloc[0].tolist()
#Collecting clube
clube = attribute_chart.iat[0, 5]
posição = attribute_chart.iat[0, 8]

## parameter names
params = list(metrics.columns)
params = params[1:]

#Preparing Data
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(attribute_chart_2[params][x])
    a = a
    b = max(attribute_chart_2[params][x])
    b = b
    ranges.append((a, b))

for x in range(len(metrics['Atleta'])):
    if metrics['Atleta'][x] == jogadores:
        a_values = metrics.iloc[x].values.tolist()
    if metrics['Atleta'][x] == 'Média da Liga':
        b_values = metrics.iloc[x].values.tolist()
            
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values, b_values]

#Plotting Data
title = dict(
    title_name = jogadores,
    title_color = '#B6282F',
    title_name_2 = 'Média da Liga',
    title_color_2 = '#344D94',
    title_fontsize = 18,
) 

endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are posadj, per90'
radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
plt.savefig('Player&League_Comparison.png')
st.pyplot(fig)

##################################################################################################################### 
#####################################################################################################################
#################################################################################################################################
#################################################################################################################################

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Impacto dos Passes</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[75:80]].reset_index(drop=True)
metrics_impacto_passe_1 = metrics.iloc[:, 0].tolist()
metrics_impacto_passe_2 = metrics.iloc[:, 1].tolist()
metrics_impacto_passe_3 = metrics.iloc[:, 2].tolist()
metrics_impacto_passe_4 = metrics.iloc[:, 3].tolist()
metrics_impacto_passe_5 = metrics.iloc[:, 4].tolist()
metrics_y = [0] * len(metrics_impacto_passe_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[75:80]].reset_index(drop=True)
highlight_impacto_passe_1 = highlight.iloc[:, 0].tolist()
highlight_impacto_passe_2 = highlight.iloc[:, 1].tolist()
highlight_impacto_passe_3 = highlight.iloc[:, 2].tolist()
highlight_impacto_passe_4 = highlight.iloc[:, 3].tolist()
highlight_impacto_passe_5 = highlight.iloc[:, 4].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_impacto_passe_1_value = pd.DataFrame(highlight_impacto_passe_1).reset_index(drop=True)
highlight_impacto_passe_2_value = pd.DataFrame(highlight_impacto_passe_2).reset_index(drop=True)
highlight_impacto_passe_3_value = pd.DataFrame(highlight_impacto_passe_3).reset_index(drop=True)
highlight_impacto_passe_4_value = pd.DataFrame(highlight_impacto_passe_4).reset_index(drop=True)
highlight_impacto_passe_5_value = pd.DataFrame(highlight_impacto_passe_5).reset_index(drop=True)

highlight_impacto_passe_1_value = highlight_impacto_passe_1_value.iat[0,0]
highlight_impacto_passe_2_value = highlight_impacto_passe_2_value.iat[0,0]
highlight_impacto_passe_3_value = highlight_impacto_passe_3_value.iat[0,0]
highlight_impacto_passe_4_value = highlight_impacto_passe_4_value.iat[0,0]
highlight_impacto_passe_5_value = highlight_impacto_passe_5_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_impacto_passe_1, metrics_impacto_passe_2, 
                                    metrics_impacto_passe_3, metrics_impacto_passe_4,
                                    metrics_impacto_passe_5])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_impacto_passe_1, metrics_impacto_passe_2, 
                                    metrics_impacto_passe_3, metrics_impacto_passe_4,
                                    metrics_impacto_passe_5])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['Posição'] == "Extremo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe, clube):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[(filtered_df['Atleta'] == player_name) & (filtered_df['Clube'] == clube)]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_1_ranking_value = (get_player_rank(jogadores, liga, "Passes criativos (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({impacto_passe_1_ranking_value}/{rows_count})"
full_title_impacto_passe_1 = f"Passes criativos (p90) {output_str} {highlight_impacto_passe_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_2_ranking_value = (get_player_rank(jogadores, liga, "xT Passes no último terço (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({impacto_passe_2_ranking_value}/{rows_count})"
full_title_impacto_passe_2 = f"xT Passes no último terço (p90) {output_str} {highlight_impacto_passe_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_3_ranking_value = (get_player_rank(jogadores, liga, "xT Passes para último terço (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({impacto_passe_3_ranking_value}/{rows_count})"
full_title_impacto_passe_3 = f"xT Passes para último terço (p90) {output_str} {highlight_impacto_passe_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_4_ranking_value = (get_player_rank(jogadores, liga, "xT Passes (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({impacto_passe_4_ranking_value}/{rows_count})"
full_title_impacto_passe_4 = f"xT Passes (p90) {output_str} {highlight_impacto_passe_4_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_5_ranking_value = (get_player_rank(jogadores, liga, "xT Cruzamentos (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({impacto_passe_5_ranking_value}/{rows_count})"
full_title_impacto_passe_5 = f"xT Cruzamentos (p90) {output_str} {highlight_impacto_passe_5_value}"

##############################################################################################################
##############################################################################################################
#From Claude version2

def calculate_ranks(values):
    """Calculate ranks for a given metric, with highest values getting rank 1"""
    return pd.Series(values).rank(ascending=False).astype(int).tolist()

def prepare_data(tabela_a, metrics_cols):
    """Prepare the metrics data dictionary with all required data"""
    metrics_data = {}
    
    for col in metrics_cols:
        # Store the metric values
        metrics_data[f'metrics_{col}'] = tabela_a[col].tolist()
        # Calculate and store ranks
        metrics_data[f'ranks_{col}'] = calculate_ranks(tabela_a[col])
        # Store player names
        metrics_data[f'player_names_{col}'] = tabela_a['Atleta'].tolist()
    
    return metrics_data

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value, equipe):
    """
    Create an interactive plot showing player attributes with hover information
    
    Parameters:
    tabela_a (pd.DataFrame): DataFrame containing all player data
    jogadores (str): Name of the player to highlight
    min_value (float): Minimum value for x-axis
    max_value (float): Maximum value for x-axis
    """
    # List of metrics to plot
    metrics_list = [
        'Passes criativos (p90)', 'xT Passes no último terço (p90)', 
        'xT Passes para último terço (p90)','xT Passes (p90)',
        'xT Cruzamentos (p90)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data with additional filtering for Clube
    highlight_data = {
        f'highlight_{metric}': tabela_a[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)][metric].iloc[0]
        for metric in metrics_list
    }

    highlight_ranks = {
        metric: int(
            pd.Series(tabela_a[metric]).rank(ascending=False)[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)].iloc[0]
        )
        for metric in metrics_list
    }
    
    # Total number of players
    total_players = len(tabela_a)
    
    # Create subplots
    fig = make_subplots(
        rows=9, 
        cols=1,
        subplot_titles=[
            f"{metric.capitalize()} ({highlight_ranks[metric]}/{total_players}) {highlight_data[f'highlight_{metric}']:.2f}"
            for metric in metrics_list
        ],
        vertical_spacing=0.04
    )

    # Update subplot titles font size and color
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=17, color='black')

    # Add traces for each metric
    for idx, metric in enumerate(metrics_list, 1):
        # Add scatter plot for all players
        fig.add_trace(
            go.Scatter(
                x=metrics_data[f'metrics_{metric}'],
                y=[0] * len(metrics_data[f'metrics_{metric}']),
                mode='markers',
                name='Demais Jogadores',
                marker=dict(color='deepskyblue', size=8),
                text=[f"{rank}/{total_players}" for rank in metrics_data[f'ranks_{metric}']],
                customdata=metrics_data[f'player_names_{metric}'],
                hovertemplate='%{customdata}<br>Rank: %{text}<br>Value: %{x:.2f}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )
        
        # Add highlighted player point
        fig.add_trace(
            go.Scatter(
                x=[highlight_data[f'highlight_{metric}']],
                y=[0],
                mode='markers',
                name=jogadores,
                marker=dict(color='blue', size=12),
                hovertemplate=f'{jogadores}<br>Rank: {highlight_ranks[metric]}/{total_players}<br>Value: %{{x:.2f}}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )

    # Get the total number of metrics (subplots)
    n_metrics = len(metrics_list)

    # Update layout for each subplot
    for i in range(1, n_metrics + 1):
        if i == n_metrics:  # Only for the last subplot
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=False,
                ticktext=["PIOR", "MÉDIA (0)", "MELHOR"],
                tickvals=[min_value/2, 0, max_value/2],
                tickmode='array',
                ticks="outside",
                ticklen=2,
                tickfont=dict(size=16),
                tickangle=0,
                side='bottom',
                automargin=False,
                row=i, 
                col=1
            )
            # Adjust layout for the last subplot
            fig.update_layout(
                xaxis_tickfont_family="Arial",
                margin=dict(b=0)  # Reduce bottom margin
            )
        else:  # For all other subplots
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                showline=False,
                showticklabels=False,  # Hide tick labels
                row=i, 
                col=1
            )  # Reduces space between axis and labels

        # Update layout for the entire figure
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            showline=False,
            row=i, 
            col=1
        )

    # Update layout for the entire figure
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.23,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        margin=dict(t=100)
    )

    # Add x-axis label at the bottom
    fig.add_annotation(
        text="Desvio-padrão",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.32,
        showarrow=False,
        font=dict(size=16, color='black', weight='bold')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_impacto_passe_1), min(metrics_impacto_passe_2), 
min(metrics_impacto_passe_3), min(metrics_impacto_passe_4),
min(metrics_impacto_passe_5)
])  # Add padding of 0.5

max_value_test = max([
max(metrics_impacto_passe_1), max(metrics_impacto_passe_2), 
max(metrics_impacto_passe_3), max(metrics_impacto_passe_4),
max(metrics_impacto_passe_5)
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value,    # Maximum value for x-axis
    equipe = equipe
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & 
                                    (attribute_chart['função']=="Extremo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&
                                            (attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Extremo") & 
                                            (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[55:60]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[75:80]].reset_index(drop=True)
metrics_percent = pd.concat([metrics, percent]).reset_index(drop=True)
#metrics_percent.rename(columns={'Atleta': 'Métricas'}, inplace=True)
metrics_percent = metrics_percent.transpose()
# Rename specific columns while keeping 'Métricas' column unchanged
metrics_percent = metrics_percent.rename(columns={
    metrics_percent.columns[0]: f'Métricas',
    metrics_percent.columns[1]: f'Percentil na Liga'
})
#st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)

# Define function to color and label cells in the "Percentil na Liga" column
def color_percentil(val):
    """
    Apply color styling based on percentile value
    """
    # Color maps from Matplotlib
    cmap = plt.get_cmap('Blues')
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")
    
    try:
        # Convert to float in case it's a string or other type
        val_num = float(val)
        
        if pd.isna(val_num):
            return ''  # No styling for NaN values
        elif val_num >= 90:
            color = cmap2(0.70)  # "Elite"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 75 <= val_num < 90:
            color = cmap2(0.50)  # "Destaque"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 60 <= val_num < 75:
            color = cmap(0.50)  # "Razoável"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 40 <= val_num < 60:
            color = cmap(0.25)  # "Mediano"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 20 <= val_num < 40:
            color = cmap1(0.30)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        else:
            color = cmap1(0.50)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
    except (ValueError, TypeError):
        return ''

# Define the styling for the entire table
styles = [
    dict(selector="th", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("color", "#333333"),
        ("font-weight", "bold"),
        ("padding", "12px 15px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black"),  # Heavier horizontal line under headers
        ("background-color", "white")
    ]),
    dict(selector="td", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("padding", "2px 5px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black")  # Horizontal lines between rows
    ]),
    # Center align specific columns
    dict(selector="th:nth-child(2), th:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="td:nth-child(2), td:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="", props=[
        ("border", "none"),  # Remove table border
        ("border-collapse", "collapse"),
        ("box-shadow", "0px 1px 3px rgba(0,0,0,0.1)")
    ]),
    # Remove vertical grid lines by not defining them
    dict(selector="tbody tr:nth-child(even)", props=[
        ("background-color", "white")
    ]),
    # Remove table outline
    dict(selector="table", props=[
        ("border", "none")
    ])
]

# Apply the styling to your dataframe
styled_df = metrics_percent.style\
    .set_table_styles(styles)\
    .applymap(color_percentil, subset=['Percentil na Liga'])\
    .format({'Métricas': '{:.2f}', 'Percentil na Liga': '{:.0f}'})

# Display in Streamlit
st.table(styled_df)
# Function to plot the legend for the 5 colors from the Blues colormap
st.markdown("<br><h5 style='text-align: center;'>Legenda Baseada no Percentil do Jogador na Liga</h5>", unsafe_allow_html=True)

def plot_color_legend():
    # Custom colors for the categories (using the same logic as in apply_colormap_based_on_value)
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    # Assign colors using the same logic
    colors = [
        cmap2(0.70),   # "Elite"
        cmap2(0.50),  # "Destaque"
        cmap(0.50),   # "Razoável"
        cmap(0.25),  # "Mediano"
        cmap1(0.30), # "Frágil"
        cmap1(0.50)  # "Péssimo"
    ]
    
    # Labels for the legend (highest to lowest)
    labels = ['Elite (>=90)', 'Destaque (75-90)', 'Razoável (60-75)', 'Mediano (40-60)', 'Frágil (20-40)', 'Péssimo (<20)']

    # Plot the legend horizontally with a smaller size
    fig, ax = plt.subplots(figsize=(6, 0.3))  # Smaller layout
    for i, (label, color) in enumerate(zip(labels[::-1], colors[::-1])):  # Reverse labels for display
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))  # Draw rectangle
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=6.0)  # Add text inside the rectangles

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Remove axes

    # Add an arrow pointing from "Highest" to "Lowest"
    ax.annotate('', xy=(6, 1), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.04, width=1.2, headwidth=5))

    return fig

# Call the function to plot the legend and display it in Streamlit
legend_fig = plot_color_legend()
st.pyplot(legend_fig)


##################################################################################################################### 
#####################################################################################################################

#Plotar Terceiro Gráfico - Radar de Métricas x Média da liga:
st.markdown(f"<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em {temporada}</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")  & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 55:60]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[55:60]]
metrics_mean['Passes criativos (p90)'] = metrics_mean['Passes criativos (p90)'].mean()
metrics_mean['xT Passes no último terço (p90)'] = metrics_mean['xT Passes no último terço (p90)'].mean()
metrics_mean['xT Passes para último terço (p90)'] = metrics_mean['xT Passes para último terço (p90)'].mean()
metrics_mean['xT Passes (p90)'] = metrics_mean['xT Passes (p90)'].mean()
metrics_mean['xT Cruzamentos (p90)'] = metrics_mean['xT Cruzamentos (p90)'].mean()

# Keep only the first row
metrics_mean = metrics_mean.iloc[:1]

metrics_mean['Atleta'] = 'Média da Liga' 
metrics_mean.insert(0, 'Atleta', metrics_mean.pop('Atleta'))

#Concatenate both dataframes
metrics = pd.concat([metrics, metrics_mean]).reset_index(drop=True)
metrics_list = metrics.iloc[0].tolist()
#Collecting clube
clube = attribute_chart.iat[0, 5]
posição = attribute_chart.iat[0, 8]

## parameter names
params = list(metrics.columns)
params = params[1:]

#Preparing Data
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(attribute_chart_2[params][x])
    a = a
    b = max(attribute_chart_2[params][x])
    b = b
    ranges.append((a, b))

for x in range(len(metrics['Atleta'])):
    if metrics['Atleta'][x] == jogadores:
        a_values = metrics.iloc[x].values.tolist()
    if metrics['Atleta'][x] == 'Média da Liga':
        b_values = metrics.iloc[x].values.tolist()
            
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values, b_values]

#Plotting Data
title = dict(
    title_name = jogadores,
    title_color = '#B6282F',
    title_name_2 = 'Média da Liga',
    title_color_2 = '#344D94',
    title_fontsize = 18,
) 

endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are posadj, per90'
radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
plt.savefig('Player&League_Comparison.png')
st.pyplot(fig)

###############################################################################################################################
###############################################################################################################################
###############################################################################################################################

métricas_movimentação_ofensiva = ['Recepções na área (p90)', 
                                    'xT Conduções (p90)', 
                                    'xT Corridas em profundidade (p90)',
                                    'Entradas na área (p90)'
]

#Plotar Primeiro Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Movimentação Ofensiva</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[38, 92, 93, 41]].reset_index(drop=True)
metrics_movimentação_ofensiva_1 = metrics.iloc[:, 0].tolist()
metrics_movimentação_ofensiva_2 = metrics.iloc[:, 1].tolist()
metrics_movimentação_ofensiva_3 = metrics.iloc[:, 2].tolist()
metrics_movimentação_ofensiva_4 = metrics.iloc[:, 3].tolist()
metrics_y = [0] * len(metrics_movimentação_ofensiva_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[38, 92, 93, 41]].reset_index(drop=True)
highlight_movimentação_ofensiva_1 = highlight.iloc[:, 0].tolist()
highlight_movimentação_ofensiva_2 = highlight.iloc[:, 1].tolist()
highlight_movimentação_ofensiva_3 = highlight.iloc[:, 2].tolist()
highlight_movimentação_ofensiva_4 = highlight.iloc[:, 3].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_movimentação_ofensiva_1_value = pd.DataFrame(highlight_movimentação_ofensiva_1).reset_index(drop=True)
highlight_movimentação_ofensiva_2_value = pd.DataFrame(highlight_movimentação_ofensiva_2).reset_index(drop=True)
highlight_movimentação_ofensiva_3_value = pd.DataFrame(highlight_movimentação_ofensiva_3).reset_index(drop=True)
highlight_movimentação_ofensiva_4_value = pd.DataFrame(highlight_movimentação_ofensiva_4).reset_index(drop=True)

highlight_movimentação_ofensiva_1_value = highlight_movimentação_ofensiva_1_value.iat[0,0]
highlight_movimentação_ofensiva_2_value = highlight_movimentação_ofensiva_2_value.iat[0,0]
highlight_movimentação_ofensiva_3_value = highlight_movimentação_ofensiva_3_value.iat[0,0]
highlight_movimentação_ofensiva_4_value = highlight_movimentação_ofensiva_4_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_movimentação_ofensiva_1, metrics_movimentação_ofensiva_2, 
                                    metrics_movimentação_ofensiva_3, metrics_movimentação_ofensiva_4])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_movimentação_ofensiva_1, metrics_movimentação_ofensiva_2, 
                                    metrics_movimentação_ofensiva_3, metrics_movimentação_ofensiva_4])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função'] == "Extremo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe, clube):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[(filtered_df['Atleta'] == player_name) & (filtered_df['Clube'] == clube)]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
movimentação_ofensiva_1_ranking_value = (get_player_rank(jogadores, liga, "Recepções na área (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({movimentação_ofensiva_1_ranking_value}/{rows_count})"
full_title_movimentação_ofensiva_1 = f"Recepções na área (p90) {output_str} {highlight_movimentação_ofensiva_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
movimentação_ofensiva_2_ranking_value = (get_player_rank(jogadores, liga, "xT Conduções (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({movimentação_ofensiva_2_ranking_value}/{rows_count})"
full_title_movimentação_ofensiva_2 = f"xT Conduções (p90) {output_str} {highlight_movimentação_ofensiva_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
movimentação_ofensiva_3_ranking_value = (get_player_rank(jogadores, liga, "xT Corridas em profundidade (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({movimentação_ofensiva_3_ranking_value}/{rows_count})"
full_title_movimentação_ofensiva_3 = f"xT Corridas em profundidade (p90) {output_str} {highlight_movimentação_ofensiva_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
movimentação_ofensiva_4_ranking_value = (get_player_rank(jogadores, liga, "Entradas na área (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({movimentação_ofensiva_4_ranking_value}/{rows_count})"
full_title_movimentação_ofensiva_4 = f"Entradas na área (p90) {output_str} {highlight_movimentação_ofensiva_4_value}"

##############################################################################################################
##############################################################################################################
#From Claude version2

def calculate_ranks(values):
    """Calculate ranks for a given metric, with highest values getting rank 1"""
    return pd.Series(values).rank(ascending=False).astype(int).tolist()

def prepare_data(tabela_a, metrics_cols):
    """Prepare the metrics data dictionary with all required data"""
    metrics_data = {}
    
    for col in metrics_cols:
        # Store the metric values
        metrics_data[f'metrics_{col}'] = tabela_a[col].tolist()
        # Calculate and store ranks
        metrics_data[f'ranks_{col}'] = calculate_ranks(tabela_a[col])
        # Store player names
        metrics_data[f'player_names_{col}'] = tabela_a['Atleta'].tolist()
    
    return metrics_data

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value, equipe):
    """
    Create an interactive plot showing player attributes with hover information
    
    Parameters:
    tabela_a (pd.DataFrame): DataFrame containing all player data
    jogadores (str): Name of the player to highlight
    min_value (float): Minimum value for x-axis
    max_value (float): Maximum value for x-axis
    """
    # List of metrics to plot
    metrics_list = [
        'Recepções na área (p90)', 'xT Conduções (p90)', 
        'xT Corridas em profundidade (p90)','Entradas na área (p90)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data with additional filtering for Clube
    highlight_data = {
        f'highlight_{metric}': tabela_a[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)][metric].iloc[0]
        for metric in metrics_list
    }

    highlight_ranks = {
        metric: int(
            pd.Series(tabela_a[metric]).rank(ascending=False)[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)].iloc[0]
        )
        for metric in metrics_list
    }
    
    # Total number of players
    total_players = len(tabela_a)
    
    # Create subplots
    fig = make_subplots(
        rows=9, 
        cols=1,
        subplot_titles=[
            f"{metric.capitalize()} ({highlight_ranks[metric]}/{total_players}) {highlight_data[f'highlight_{metric}']:.2f}"
            for metric in metrics_list
        ],
        vertical_spacing=0.04
    )

    # Update subplot titles font size and color
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=17, color='black')

    # Add traces for each metric
    for idx, metric in enumerate(metrics_list, 1):
        # Add scatter plot for all players
        fig.add_trace(
            go.Scatter(
                x=metrics_data[f'metrics_{metric}'],
                y=[0] * len(metrics_data[f'metrics_{metric}']),
                mode='markers',
                name='Demais Jogadores',
                marker=dict(color='deepskyblue', size=8),
                text=[f"{rank}/{total_players}" for rank in metrics_data[f'ranks_{metric}']],
                customdata=metrics_data[f'player_names_{metric}'],
                hovertemplate='%{customdata}<br>Rank: %{text}<br>Value: %{x:.2f}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )
        
        # Add highlighted player point
        fig.add_trace(
            go.Scatter(
                x=[highlight_data[f'highlight_{metric}']],
                y=[0],
                mode='markers',
                name=jogadores,
                marker=dict(color='blue', size=12),
                hovertemplate=f'{jogadores}<br>Rank: {highlight_ranks[metric]}/{total_players}<br>Value: %{{x:.2f}}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )

    # Get the total number of metrics (subplots)
    n_metrics = len(metrics_list)

    # Update layout for each subplot
    for i in range(1, n_metrics + 1):
        if i == n_metrics:  # Only for the last subplot
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=False,
                ticktext=["PIOR", "MÉDIA (0)", "MELHOR"],
                tickvals=[min_value/2, 0, max_value/2],
                tickmode='array',
                ticks="outside",
                ticklen=2,
                tickfont=dict(size=16),
                tickangle=0,
                side='bottom',
                automargin=False,
                row=i, 
                col=1
            )
            # Adjust layout for the last subplot
            fig.update_layout(
                xaxis_tickfont_family="Arial",
                margin=dict(b=0)  # Reduce bottom margin
            )
        else:  # For all other subplots
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                showline=False,
                showticklabels=False,  # Hide tick labels
                row=i, 
                col=1
            )  # Reduces space between axis and labels

        # Update layout for the entire figure
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            showline=False,
            row=i, 
            col=1
        )

    # Update layout for the entire figure
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.38,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        margin=dict(t=100)
    )

    # Add x-axis label at the bottom
    fig.add_annotation(
        text="Desvio-padrão",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.47,
        showarrow=False,
        font=dict(size=16, color='blue', weight='bold')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_movimentação_ofensiva_1), min(metrics_movimentação_ofensiva_2), 
min(metrics_movimentação_ofensiva_3), min(metrics_movimentação_ofensiva_4),
])  # Add padding of 0.5

max_value_test = max([
max(metrics_movimentação_ofensiva_1), max(metrics_movimentação_ofensiva_2), 
max(metrics_movimentação_ofensiva_3), max(metrics_movimentação_ofensiva_4),
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value,    # Maximum value for x-axis
    equipe = equipe
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&
                                            (attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Extremo") & 
                                            (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[18, 72, 73, 21]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[38, 92, 93, 41]].reset_index(drop=True)
metrics_percent = pd.concat([metrics, percent]).reset_index(drop=True)
#metrics_percent.rename(columns={'Atleta': 'Métricas'}, inplace=True)
metrics_percent = metrics_percent.transpose()
# Rename specific columns while keeping 'Métricas' column unchanged
metrics_percent = metrics_percent.rename(columns={
    metrics_percent.columns[0]: f'Métricas',
    metrics_percent.columns[1]: f'Percentil na Liga'
})
#st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)

# Define function to color and label cells in the "Percentil na Liga" column
def color_percentil(val):
    """
    Apply color styling based on percentile value
    """
    # Color maps from Matplotlib
    cmap = plt.get_cmap('Blues')
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")
    
    try:
        # Convert to float in case it's a string or other type
        val_num = float(val)
        
        if pd.isna(val_num):
            return ''  # No styling for NaN values
        elif val_num >= 90:
            color = cmap2(0.70)  # "Elite"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 75 <= val_num < 90:
            color = cmap2(0.50)  # "Destaque"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 60 <= val_num < 75:
            color = cmap(0.50)  # "Razoável"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 40 <= val_num < 60:
            color = cmap(0.25)  # "Mediano"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 20 <= val_num < 40:
            color = cmap1(0.30)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        else:
            color = cmap1(0.50)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
    except (ValueError, TypeError):
        return ''

# Define the styling for the entire table
styles = [
    dict(selector="th", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("color", "#333333"),
        ("font-weight", "bold"),
        ("padding", "12px 15px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black"),  # Heavier horizontal line under headers
        ("background-color", "white")
    ]),
    dict(selector="td", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("padding", "2px 5px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black")  # Horizontal lines between rows
    ]),
    # Center align specific columns
    dict(selector="th:nth-child(2), th:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="td:nth-child(2), td:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="", props=[
        ("border", "none"),  # Remove table border
        ("border-collapse", "collapse"),
        ("box-shadow", "0px 1px 3px rgba(0,0,0,0.1)")
    ]),
    # Remove vertical grid lines by not defining them
    dict(selector="tbody tr:nth-child(even)", props=[
        ("background-color", "white")
    ]),
    # Remove table outline
    dict(selector="table", props=[
        ("border", "none")
    ])
]

# Apply the styling to your dataframe
styled_df = metrics_percent.style\
    .set_table_styles(styles)\
    .applymap(color_percentil, subset=['Percentil na Liga'])\
    .format({'Métricas': '{:.2f}', 'Percentil na Liga': '{:.0f}'})

# Display in Streamlit
st.table(styled_df)
# Function to plot the legend for the 5 colors from the Blues colormap
st.markdown("<br><h5 style='text-align: center;'>Legenda Baseada no Percentil do Jogador na Liga</h5>", unsafe_allow_html=True)

def plot_color_legend():
    # Custom colors for the categories (using the same logic as in apply_colormap_based_on_value)
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    # Assign colors using the same logic
    colors = [
        cmap2(0.70),   # "Elite"
        cmap2(0.50),  # "Destaque"
        cmap(0.50),   # "Razoável"
        cmap(0.25),  # "Mediano"
        cmap1(0.30), # "Frágil"
        cmap1(0.50)  # "Péssimo"
    ]
    
    # Labels for the legend (highest to lowest)
    labels = ['Elite (>=90)', 'Destaque (75-90)', 'Razoável (60-75)', 'Mediano (40-60)', 'Frágil (20-40)', 'Péssimo (<20)']

    # Plot the legend horizontally with a smaller size
    fig, ax = plt.subplots(figsize=(6, 0.3))  # Smaller layout
    for i, (label, color) in enumerate(zip(labels[::-1], colors[::-1])):  # Reverse labels for display
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))  # Draw rectangle
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=6.0)  # Add text inside the rectangles

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Remove axes

    # Add an arrow pointing from "Highest" to "Lowest"
    ax.annotate('', xy=(6, 1), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.04, width=1.2, headwidth=5))

    return fig

# Call the function to plot the legend and display it in Streamlit
legend_fig = plot_color_legend()
st.pyplot(legend_fig)


##################################################################################################################### 
#####################################################################################################################

#Plotar Terceiro Gráfico - Radar de Métricas x Média da liga:
st.markdown(f"<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em {temporada}</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")  & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]

#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 18, 72, 73, 21]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[18, 72, 73, 21]]
metrics_mean['Recepções na área (p90)'] = metrics_mean['Recepções na área (p90)'].mean()
metrics_mean['xT Conduções (p90)'] = metrics_mean['xT Conduções (p90)'].mean()
metrics_mean['xT Corridas em profundidade (p90)'] = metrics_mean['xT Corridas em profundidade (p90)'].mean()
metrics_mean['Entradas na área (p90)'] = metrics_mean['Entradas na área (p90)'].mean()

# Keep only the first row
metrics_mean = metrics_mean.iloc[:1]

metrics_mean['Atleta'] = 'Média da Liga' 
metrics_mean.insert(0, 'Atleta', metrics_mean.pop('Atleta'))

#Concatenate both dataframes
metrics = pd.concat([metrics, metrics_mean]).reset_index(drop=True)
metrics_list = metrics.iloc[0].tolist()
#Collecting clube
clube = attribute_chart.iat[0, 5]
posição = attribute_chart.iat[0, 8]

## parameter names
params = list(metrics.columns)
params = params[1:]

#Preparing Data
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(attribute_chart_2[params][x])
    a = a
    b = max(attribute_chart_2[params][x])
    b = b
    ranges.append((a, b))

for x in range(len(metrics['Atleta'])):
    if metrics['Atleta'][x] == jogadores:
        a_values = metrics.iloc[x].values.tolist()
    if metrics['Atleta'][x] == 'Média da Liga':
        b_values = metrics.iloc[x].values.tolist()
            
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values, b_values]

#Plotting Data
title = dict(
    title_name = jogadores,
    title_color = '#B6282F',
    title_name_2 = 'Média da Liga',
    title_color_2 = '#344D94',
    title_fontsize = 18,
) 

endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are posadj, per90'
radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
plt.savefig('Player&League_Comparison.png')
st.pyplot(fig)

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Drible</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[48, 54:57]].reset_index(drop=True)
metrics_dribles_1 = metrics.iloc[:, 0].tolist()
metrics_dribles_2 = metrics.iloc[:, 1].tolist()
metrics_dribles_3 = metrics.iloc[:, 2].tolist()
metrics_dribles_4 = metrics.iloc[:, 3].tolist()
metrics_y = [0] * len(metrics_dribles_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[48, 54:57]].reset_index(drop=True)
highlight_dribles_1 = highlight.iloc[:, 0].tolist()
highlight_dribles_2 = highlight.iloc[:, 1].tolist()
highlight_dribles_3 = highlight.iloc[:, 2].tolist()
highlight_dribles_4 = highlight.iloc[:, 3].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_dribles_1_value = pd.DataFrame(highlight_dribles_1).reset_index(drop=True)
highlight_dribles_2_value = pd.DataFrame(highlight_dribles_2).reset_index(drop=True)
highlight_dribles_3_value = pd.DataFrame(highlight_dribles_3).reset_index(drop=True)
highlight_dribles_4_value = pd.DataFrame(highlight_dribles_4).reset_index(drop=True)

highlight_dribles_1_value = highlight_dribles_1_value.iat[0,0]
highlight_dribles_2_value = highlight_dribles_2_value.iat[0,0]
highlight_dribles_3_value = highlight_dribles_3_value.iat[0,0]
highlight_dribles_4_value = highlight_dribles_4_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_dribles_1, metrics_dribles_2, 
                                    metrics_dribles_3, metrics_dribles_4])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_dribles_1, metrics_dribles_2, 
                                    metrics_dribles_3, metrics_dribles_4])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função'] == "Extremo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe, clube):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[(filtered_df['Atleta'] == player_name) & (filtered_df['Clube'] == clube)]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
dribles_1_ranking_value = (get_player_rank(jogadores, liga, "Resistência à pressão (%)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({dribles_1_ranking_value}/{rows_count})"
full_title_dribles_1 = f"Resistência à pressão (%) {output_str} {highlight_dribles_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
dribles_2_ranking_value = (get_player_rank(jogadores, liga, "xG Dribles (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({dribles_2_ranking_value}/{rows_count})"
full_title_dribles_2 = f"xG Dribles (p90) {output_str} {highlight_dribles_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
dribles_3_ranking_value = (get_player_rank(jogadores, liga, "xT Dribles (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({dribles_3_ranking_value}/{rows_count})"
full_title_dribles_3 = f"xT Dribles (p90) {output_str} {highlight_dribles_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
dribles_4_ranking_value = (get_player_rank(jogadores, liga, "Dribles bem sucedidos (%)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({dribles_4_ranking_value}/{rows_count})"
full_title_dribles_4 = f"Dribles bem sucedidos (%) {output_str} {highlight_dribles_4_value}"

##############################################################################################################
##############################################################################################################
#From Claude version2

def calculate_ranks(values):
    """Calculate ranks for a given metric, with highest values getting rank 1"""
    return pd.Series(values).rank(ascending=False).astype(int).tolist()

def prepare_data(tabela_a, metrics_cols):
    """Prepare the metrics data dictionary with all required data"""
    metrics_data = {}
    
    for col in metrics_cols:
        # Store the metric values
        metrics_data[f'metrics_{col}'] = tabela_a[col].tolist()
        # Calculate and store ranks
        metrics_data[f'ranks_{col}'] = calculate_ranks(tabela_a[col])
        # Store player names
        metrics_data[f'player_names_{col}'] = tabela_a['Atleta'].tolist()
    
    return metrics_data

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value, equipe):
    """
    Create an interactive plot showing player attributes with hover information
    
    Parameters:
    tabela_a (pd.DataFrame): DataFrame containing all player data
    jogadores (str): Name of the player to highlight
    min_value (float): Minimum value for x-axis
    max_value (float): Maximum value for x-axis
    """
    # List of metrics to plot
    metrics_list = [
        'Resistência à pressão (%)', 'xG Dribles (p90)', 
        'xT Dribles (p90)','Dribles bem sucedidos (%)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data with additional filtering for Clube
    highlight_data = {
        f'highlight_{metric}': tabela_a[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)][metric].iloc[0]
        for metric in metrics_list
    }

    highlight_ranks = {
        metric: int(
            pd.Series(tabela_a[metric]).rank(ascending=False)[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)].iloc[0]
        )
        for metric in metrics_list
    }
    
    # Total number of players
    total_players = len(tabela_a)
    
    # Create subplots
    fig = make_subplots(
        rows=9, 
        cols=1,
        subplot_titles=[
            f"{metric.capitalize()} ({highlight_ranks[metric]}/{total_players}) {highlight_data[f'highlight_{metric}']:.2f}"
            for metric in metrics_list
        ],
        vertical_spacing=0.04
    )

    # Update subplot titles font size and color
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=17, color='black')

    # Add traces for each metric
    for idx, metric in enumerate(metrics_list, 1):
        # Add scatter plot for all players
        fig.add_trace(
            go.Scatter(
                x=metrics_data[f'metrics_{metric}'],
                y=[0] * len(metrics_data[f'metrics_{metric}']),
                mode='markers',
                name='Demais Jogadores',
                marker=dict(color='deepskyblue', size=8),
                text=[f"{rank}/{total_players}" for rank in metrics_data[f'ranks_{metric}']],
                customdata=metrics_data[f'player_names_{metric}'],
                hovertemplate='%{customdata}<br>Rank: %{text}<br>Value: %{x:.2f}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )
        
        # Add highlighted player point
        fig.add_trace(
            go.Scatter(
                x=[highlight_data[f'highlight_{metric}']],
                y=[0],
                mode='markers',
                name=jogadores,
                marker=dict(color='blue', size=12),
                hovertemplate=f'{jogadores}<br>Rank: {highlight_ranks[metric]}/{total_players}<br>Value: %{{x:.2f}}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )

    # Get the total number of metrics (subplots)
    n_metrics = len(metrics_list)

    # Update layout for each subplot
    for i in range(1, n_metrics + 1):
        if i == n_metrics:  # Only for the last subplot
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=False,
                ticktext=["PIOR", "MÉDIA (0)", "MELHOR"],
                tickvals=[min_value/2, 0, max_value/2],
                tickmode='array',
                ticks="outside",
                ticklen=2,
                tickfont=dict(size=16),
                tickangle=0,
                side='bottom',
                automargin=False,
                row=i, 
                col=1
            )
            # Adjust layout for the last subplot
            fig.update_layout(
                xaxis_tickfont_family="Arial",
                margin=dict(b=0)  # Reduce bottom margin
            )
        else:  # For all other subplots
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                showline=False,
                showticklabels=False,  # Hide tick labels
                row=i, 
                col=1
            )  # Reduces space between axis and labels

        # Update layout for the entire figure
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            showline=False,
            row=i, 
            col=1
        )

    # Update layout for the entire figure
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.38,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        margin=dict(t=100)
    )

    # Add x-axis label at the bottom
    fig.add_annotation(
        text="Desvio-padrão",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.47,
        showarrow=False,
        font=dict(size=16, color='blue', weight='bold')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_dribles_1), min(metrics_dribles_2), 
min(metrics_dribles_3), min(metrics_dribles_4),
])  # Add padding of 0.5

max_value_test = max([
min(metrics_dribles_1), min(metrics_dribles_2), 
min(metrics_dribles_3), min(metrics_dribles_4),
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value,    # Maximum value for x-axis
    equipe = equipe
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################
    
#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & 
                                    (attribute_chart['função']=="Extremo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&
                                            (attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Extremo") & 
                                            (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[28, 34:37]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[48, 54:57]].reset_index(drop=True)
metrics_percent = pd.concat([metrics, percent]).reset_index(drop=True)
metrics_percent = metrics_percent.transpose()
metrics_percent = metrics_percent.rename(columns={
    metrics_percent.columns[0]: f'Métricas',
    metrics_percent.columns[1]: f'Percentil na Liga'
})
#st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)

# Define function to color and label cells in the "Percentil na Liga" column
def color_percentil(val):
    """
    Apply color styling based on percentile value
    """
    # Color maps from Matplotlib
    cmap = plt.get_cmap('Blues')
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")
    
    try:
        # Convert to float in case it's a string or other type
        val_num = float(val)
        
        if pd.isna(val_num):
            return ''  # No styling for NaN values
        elif val_num >= 90:
            color = cmap2(0.70)  # "Elite"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 75 <= val_num < 90:
            color = cmap2(0.50)  # "Destaque"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 60 <= val_num < 75:
            color = cmap(0.50)  # "Razoável"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 40 <= val_num < 60:
            color = cmap(0.25)  # "Mediano"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 20 <= val_num < 40:
            color = cmap1(0.30)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        else:
            color = cmap1(0.50)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
    except (ValueError, TypeError):
        return ''

# Define the styling for the entire table
styles = [
    dict(selector="th", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("color", "#333333"),
        ("font-weight", "bold"),
        ("padding", "12px 15px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black"),  # Heavier horizontal line under headers
        ("background-color", "white")
    ]),
    dict(selector="td", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("padding", "2px 5px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black")  # Horizontal lines between rows
    ]),
    # Center align specific columns
    dict(selector="th:nth-child(2), th:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="td:nth-child(2), td:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="", props=[
        ("border", "none"),  # Remove table border
        ("border-collapse", "collapse"),
        ("box-shadow", "0px 1px 3px rgba(0,0,0,0.1)")
    ]),
    # Remove vertical grid lines by not defining them
    dict(selector="tbody tr:nth-child(even)", props=[
        ("background-color", "white")
    ]),
    # Remove table outline
    dict(selector="table", props=[
        ("border", "none")
    ])
]

# Apply the styling to your dataframe
styled_df = metrics_percent.style\
    .set_table_styles(styles)\
    .applymap(color_percentil, subset=['Percentil na Liga'])\
    .format({'Métricas': '{:.2f}', 'Percentil na Liga': '{:.0f}'})

# Display in Streamlit
st.table(styled_df)
# Function to plot the legend for the 5 colors from the Blues colormap
st.markdown("<br><h5 style='text-align: center;'>Legenda Baseada no Percentil do Jogador na Liga</h5>", unsafe_allow_html=True)

def plot_color_legend():
    # Custom colors for the categories (using the same logic as in apply_colormap_based_on_value)
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    # Assign colors using the same logic
    colors = [
        cmap2(0.70),   # "Elite"
        cmap2(0.50),  # "Destaque"
        cmap(0.50),   # "Razoável"
        cmap(0.25),  # "Mediano"
        cmap1(0.30), # "Frágil"
        cmap1(0.50)  # "Péssimo"
    ]
    
    # Labels for the legend (highest to lowest)
    labels = ['Elite (>=90)', 'Destaque (75-90)', 'Razoável (60-75)', 'Mediano (40-60)', 'Frágil (20-40)', 'Péssimo (<20)']

    # Plot the legend horizontally with a smaller size
    fig, ax = plt.subplots(figsize=(6, 0.3))  # Smaller layout
    for i, (label, color) in enumerate(zip(labels[::-1], colors[::-1])):  # Reverse labels for display
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))  # Draw rectangle
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=6.0)  # Add text inside the rectangles

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Remove axes

    # Add an arrow pointing from "Highest" to "Lowest"
    ax.annotate('', xy=(6, 1), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.04, width=1.2, headwidth=5))

    return fig

# Call the function to plot the legend and display it in Streamlit
legend_fig = plot_color_legend()
st.pyplot(legend_fig)


##################################################################################################################### 
#####################################################################################################################

#Plotar Terceiro Gráfico - Radar de Métricas x Média da liga:
st.markdown(f"<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em {temporada}</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")  & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 28, 34:37]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[28, 34:37]]
metrics_mean['Resistência à pressão (%)'] = metrics_mean['Resistência à pressão (%)'].mean()
metrics_mean['xG Dribles (p90)'] = metrics_mean['xG Dribles (p90)'].mean()
metrics_mean['xT Dribles (p90)'] = metrics_mean['xT Dribles (p90)'].mean()
metrics_mean['Dribles bem sucedidos (%)'] = metrics_mean['Dribles bem sucedidos (%)'].mean()

# Keep only the first row
metrics_mean = metrics_mean.iloc[:1]

metrics_mean['Atleta'] = 'Média da Liga' 
metrics_mean.insert(0, 'Atleta', metrics_mean.pop('Atleta'))

#Concatenate both dataframes
metrics = pd.concat([metrics, metrics_mean]).reset_index(drop=True)
metrics_list = metrics.iloc[0].tolist()
#Collecting clube
clube = attribute_chart.iat[0, 5]
posição = attribute_chart.iat[0, 8]

## parameter names
params = list(metrics.columns)
params = params[1:]

#Preparing Data
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(attribute_chart_2[params][x])
    a = a
    b = max(attribute_chart_2[params][x])
    b = b
    ranges.append((a, b))

for x in range(len(metrics['Atleta'])):
    if metrics['Atleta'][x] == jogadores:
        a_values = metrics.iloc[x].values.tolist()
    if metrics['Atleta'][x] == 'Média da Liga':
        b_values = metrics.iloc[x].values.tolist()
            
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values, b_values]

#Plotting Data
title = dict(
    title_name = jogadores,
    title_color = '#B6282F',
    title_name_2 = 'Média da Liga',
    title_color_2 = '#344D94',
    title_fontsize = 18,
) 

endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are posadj, per90'
radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
plt.savefig('Player&League_Comparison.png')
st.pyplot(fig)

##################################################################################################################### 
#####################################################################################################################

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Efetividade</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")

#Renaming columns                        
attribute_chart_z.rename(columns={'xG_xA_touches': '(xG + xA) (p100 toques)'}, inplace=True)
attribute_chart_z.rename(columns={'possession_won_opponent_possession': 'Posses recuperadas (pPosse adversária)'}, inplace=True)
attribute_chart_z.rename(columns={'high_turnovers_low_reception': 'Perdas de posse (pRecepção na linha baixa)'}, inplace=True)
attribute_chart_z.rename(columns={'carries_xt_reception': 'xT Conduções (p100 Recepções)'}, inplace=True)
attribute_chart_z.rename(columns={'passes_xT_reception': 'xT Passes (p100 Recepções)'}, inplace=True)

# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[57:64]].reset_index(drop=True)
metrics_efetividade_1 = metrics.iloc[:, 0].tolist()
metrics_efetividade_2 = metrics.iloc[:, 1].tolist()
metrics_efetividade_3 = metrics.iloc[:, 2].tolist()
metrics_efetividade_4 = metrics.iloc[:, 3].tolist()
metrics_efetividade_5 = metrics.iloc[:, 4].tolist()
metrics_efetividade_6 = metrics.iloc[:, 5].tolist()
metrics_efetividade_7 = metrics.iloc[:, 6].tolist()
metrics_y = [0] * len(metrics_efetividade_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[57:64]].reset_index(drop=True)
highlight_efetividade_1 = highlight.iloc[:, 0].tolist()
highlight_efetividade_2 = highlight.iloc[:, 1].tolist()
highlight_efetividade_3 = highlight.iloc[:, 2].tolist()
highlight_efetividade_4 = highlight.iloc[:, 3].tolist()
highlight_efetividade_5 = highlight.iloc[:, 4].tolist()
highlight_efetividade_6 = highlight.iloc[:, 5].tolist()
highlight_efetividade_7 = highlight.iloc[:, 6].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_efetividade_1_value = pd.DataFrame(highlight_efetividade_1).reset_index(drop=True)
highlight_efetividade_2_value = pd.DataFrame(highlight_efetividade_2).reset_index(drop=True)
highlight_efetividade_3_value = pd.DataFrame(highlight_efetividade_3).reset_index(drop=True)
highlight_efetividade_4_value = pd.DataFrame(highlight_efetividade_4).reset_index(drop=True)
highlight_efetividade_5_value = pd.DataFrame(highlight_efetividade_5).reset_index(drop=True)
highlight_efetividade_6_value = pd.DataFrame(highlight_efetividade_6).reset_index(drop=True)
highlight_efetividade_7_value = pd.DataFrame(highlight_efetividade_7).reset_index(drop=True)

highlight_efetividade_1_value = highlight_efetividade_1_value.iat[0,0]
highlight_efetividade_2_value = highlight_efetividade_2_value.iat[0,0]
highlight_efetividade_3_value = highlight_efetividade_3_value.iat[0,0]
highlight_efetividade_4_value = highlight_efetividade_4_value.iat[0,0]
highlight_efetividade_5_value = highlight_efetividade_5_value.iat[0,0]
highlight_efetividade_6_value = highlight_efetividade_6_value.iat[0,0]
highlight_efetividade_7_value = highlight_efetividade_7_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_efetividade_1, metrics_efetividade_2, 
                                    metrics_efetividade_3, metrics_efetividade_4,
                                    metrics_efetividade_5, metrics_efetividade_6,
                                    metrics_efetividade_7])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_efetividade_1, metrics_efetividade_2, 
                                    metrics_efetividade_3, metrics_efetividade_4,
                                    metrics_efetividade_5, metrics_efetividade_6,
                                    metrics_efetividade_7])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função'] == "Extremo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe, clube):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[(filtered_df['Atleta'] == player_name) & (filtered_df['Clube'] == clube)]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
efetividade_1_ranking_value = (get_player_rank(jogadores, liga, "xG (pFinalização)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({efetividade_1_ranking_value}/{rows_count})"
full_title_efetividade_1 = f"xG (pFinalização) {output_str} {highlight_efetividade_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
efetividade_2_ranking_value = (get_player_rank(jogadores, liga, "(xG + xA) (p100 toques)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({efetividade_2_ranking_value}/{rows_count})"
full_title_efetividade_2 = f"(xG + xA) (p100 toques) {output_str} {highlight_efetividade_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
efetividade_3_ranking_value = (get_player_rank(jogadores, liga, "Posses recuperadas (pPosse adversária)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({efetividade_3_ranking_value}/{rows_count})"
full_title_efetividade_3 = f"Posses recuperadas (pPosse adversária) {output_str} {highlight_efetividade_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
efetividade_4_ranking_value = (get_player_rank(jogadores, liga, "Perdas de posse (pRecepção na linha baixa)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({efetividade_4_ranking_value}/{rows_count})"
full_title_efetividade_4 = f"Perdas de posse (pRecepção na linha baixa) {output_str} {highlight_efetividade_4_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
efetividade_5_ranking_value = (get_player_rank(jogadores, liga, "xG Chain (pPosse)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({efetividade_5_ranking_value}/{rows_count})"
full_title_efetividade_5 = f"xG Chain (pPosse) {output_str} {highlight_efetividade_5_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
efetividade_6_ranking_value = (get_player_rank(jogadores, liga, "xT Conduções (p100 Recepções)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({efetividade_6_ranking_value}/{rows_count})"
full_title_efetividade_6 = f"xT Conduções (p100 Recepções) {output_str} {highlight_efetividade_6_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
efetividade_7_ranking_value = (get_player_rank(jogadores, liga, "xT Passes (p100 Recepções)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({efetividade_7_ranking_value}/{rows_count})"
full_title_efetividade_7 = f"xT Passes (p100 Recepções) {output_str} {highlight_efetividade_7_value}"

##############################################################################################################
##############################################################################################################
#From Claude version2

def calculate_ranks(values):
    """Calculate ranks for a given metric, with highest values getting rank 1"""
    return pd.Series(values).rank(ascending=False).astype(int).tolist()

def prepare_data(tabela_a, metrics_cols):
    """Prepare the metrics data dictionary with all required data"""
    metrics_data = {}
    
    for col in metrics_cols:
        # Store the metric values
        metrics_data[f'metrics_{col}'] = tabela_a[col].tolist()
        # Calculate and store ranks
        metrics_data[f'ranks_{col}'] = calculate_ranks(tabela_a[col])
        # Store player names
        metrics_data[f'player_names_{col}'] = tabela_a['Atleta'].tolist()
    
    return metrics_data

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value, equipe):
    """
    Create an interactive plot showing player attributes with hover information
    
    Parameters:
    tabela_a (pd.DataFrame): DataFrame containing all player data
    jogadores (str): Name of the player to highlight
    min_value (float): Minimum value for x-axis
    max_value (float): Maximum value for x-axis
    """
    # List of metrics to plot
    metrics_list = [
        'xG (pFinalização)', '(xG + xA) (p100 toques)', 
        'Posses recuperadas (pPosse adversária)', 'Perdas de posse (pRecepção na linha baixa)',
        'xG Chain (pPosse)', 'xT Conduções (p100 Recepções)', 'xT Passes (p100 Recepções)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data with additional filtering for Clube
    highlight_data = {
        f'highlight_{metric}': tabela_a[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)][metric].iloc[0]
        for metric in metrics_list
    }

    highlight_ranks = {
        metric: int(
            pd.Series(tabela_a[metric]).rank(ascending=False)[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)].iloc[0]
        )
        for metric in metrics_list
    }
    
    # Total number of players
    total_players = len(tabela_a)
    
    # Create subplots
    fig = make_subplots(
        rows=9, 
        cols=1,
        subplot_titles=[
            f"{metric.capitalize()} ({highlight_ranks[metric]}/{total_players}) {highlight_data[f'highlight_{metric}']:.2f}"
            for metric in metrics_list
        ],
        vertical_spacing=0.04
    )

    # Update subplot titles font size and color
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=17, color='black')

    # Add traces for each metric
    for idx, metric in enumerate(metrics_list, 1):
        # Add scatter plot for all players
        fig.add_trace(
            go.Scatter(
                x=metrics_data[f'metrics_{metric}'],
                y=[0] * len(metrics_data[f'metrics_{metric}']),
                mode='markers',
                name='Demais Jogadores',
                marker=dict(color='deepskyblue', size=8),
                text=[f"{rank}/{total_players}" for rank in metrics_data[f'ranks_{metric}']],
                customdata=metrics_data[f'player_names_{metric}'],
                hovertemplate='%{customdata}<br>Rank: %{text}<br>Value: %{x:.2f}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )
        
        # Add highlighted player point
        fig.add_trace(
            go.Scatter(
                x=[highlight_data[f'highlight_{metric}']],
                y=[0],
                mode='markers',
                name=jogadores,
                marker=dict(color='blue', size=12),
                hovertemplate=f'{jogadores}<br>Rank: {highlight_ranks[metric]}/{total_players}<br>Value: %{{x:.2f}}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )

    # Get the total number of metrics (subplots)
    n_metrics = len(metrics_list)

    # Update layout for each subplot
    for i in range(1, n_metrics + 1):
        if i == n_metrics:  # Only for the last subplot
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=False,
                ticktext=["PIOR", "MÉDIA (0)", "MELHOR"],
                tickvals=[min_value/2, 0, max_value/2],
                tickmode='array',
                ticks="outside",
                ticklen=2,
                tickfont=dict(size=16),
                tickangle=0,
                side='bottom',
                automargin=False,
                row=i, 
                col=1
            )
            # Adjust layout for the last subplot
            fig.update_layout(
                xaxis_tickfont_family="Arial",
                margin=dict(b=0)  # Reduce bottom margin
            )
        else:  # For all other subplots
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                showline=False,
                showticklabels=False,  # Hide tick labels
                row=i, 
                col=1
            )  # Reduces space between axis and labels

        # Update layout for the entire figure
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            showline=False,
            row=i, 
            col=1
        )

    # Update layout for the entire figure
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.00,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        margin=dict(t=100)
    )

    # Add x-axis label at the bottom
    fig.add_annotation(
        text="Desvio-padrão",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.09,
        showarrow=False,
        font=dict(size=16, color='blue', weight='bold')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_efetividade_1), min(metrics_efetividade_2), 
min(metrics_efetividade_3), min(metrics_efetividade_4),
min(metrics_efetividade_5), min(metrics_efetividade_6),
min(metrics_efetividade_7)
])  # Add padding of 0.5

max_value_test = max([
max(metrics_efetividade_1), max(metrics_efetividade_2), 
max(metrics_efetividade_3), max(metrics_efetividade_4),
max(metrics_efetividade_5), max(metrics_efetividade_6),
max(metrics_efetividade_7)
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value,    # Maximum value for x-axis
    equipe = equipe
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')

#Renaming columns                        
attribute_chart.rename(columns={'xG_xA_touches': '(xG + xA) (p100 toques)'}, inplace=True)
attribute_chart.rename(columns={'possession_won_opponent_possession': 'Posses recuperadas (pPosse adversária)'}, inplace=True)
attribute_chart.rename(columns={'high_turnovers_low_reception': 'Perdas de posse (pRecepção na linha baixa)'}, inplace=True)
attribute_chart.rename(columns={'carries_xt_reception': 'xT Conduções (p100 Recepções)'}, inplace=True)
attribute_chart.rename(columns={'passes_xT_reception': 'xT Passes (p100 Recepções)'}, inplace=True)
attribute_chart_per.rename(columns={'xG_xA_touches': '(xG + xA) (p100 toques)'}, inplace=True)
attribute_chart_per.rename(columns={'possession_won_opponent_possession': 'Posses recuperadas (pPosse adversária)'}, inplace=True)
attribute_chart_per.rename(columns={'high_turnovers_low_reception': 'Perdas de posse (pRecepção na linha baixa)'}, inplace=True)
attribute_chart_per.rename(columns={'carries_xt_reception': 'xT Conduções (p100 Recepções)'}, inplace=True)
attribute_chart_per.rename(columns={'passes_xT_reception': 'xT Passes (p100 Recepções)'}, inplace=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo") & 
                                    (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&
                                            (attribute_chart_per['Liga']==liga)&(attribute_chart_per['Temporada']==temporada) & 
                                            (attribute_chart_per['função']=="Extremo") & (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[37:44]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[57:64]].reset_index(drop=True)
metrics_percent = pd.concat([metrics, percent]).reset_index(drop=True)
metrics_percent = metrics_percent.transpose()
# Rename specific columns while keeping 'Métricas' column unchanged
metrics_percent = metrics_percent.rename(columns={
    metrics_percent.columns[0]: f'Métricas',
    metrics_percent.columns[1]: f'Percentil na Liga'
})
#st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)

# Define function to color and label cells in the "Percentil na Liga" column
def color_percentil(val):
    """
    Apply color styling based on percentile value
    """
    # Color maps from Matplotlib
    cmap = plt.get_cmap('Blues')
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")
    
    try:
        # Convert to float in case it's a string or other type
        val_num = float(val)
        
        if pd.isna(val_num):
            return ''  # No styling for NaN values
        elif val_num >= 90:
            color = cmap2(0.70)  # "Elite"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 75 <= val_num < 90:
            color = cmap2(0.50)  # "Destaque"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 60 <= val_num < 75:
            color = cmap(0.50)  # "Razoável"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 40 <= val_num < 60:
            color = cmap(0.25)  # "Mediano"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 20 <= val_num < 40:
            color = cmap1(0.30)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        else:
            color = cmap1(0.50)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
    except (ValueError, TypeError):
        return ''

# Define the styling for the entire table
styles = [
    dict(selector="th", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("color", "#333333"),
        ("font-weight", "bold"),
        ("padding", "12px 15px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black"),  # Heavier horizontal line under headers
        ("background-color", "white")
    ]),
    dict(selector="td", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("padding", "2px 5px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black")  # Horizontal lines between rows
    ]),
    # Center align specific columns
    dict(selector="th:nth-child(2), th:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="td:nth-child(2), td:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="", props=[
        ("border", "none"),  # Remove table border
        ("border-collapse", "collapse"),
        ("box-shadow", "0px 1px 3px rgba(0,0,0,0.1)")
    ]),
    # Remove vertical grid lines by not defining them
    dict(selector="tbody tr:nth-child(even)", props=[
        ("background-color", "white")
    ]),
    # Remove table outline
    dict(selector="table", props=[
        ("border", "none")
    ])
]

# Apply the styling to your dataframe
styled_df = metrics_percent.style\
    .set_table_styles(styles)\
    .applymap(color_percentil, subset=['Percentil na Liga'])\
    .format({'Métricas': '{:.2f}', 'Percentil na Liga': '{:.0f}'})

# Display in Streamlit
st.table(styled_df)
# Function to plot the legend for the 5 colors from the Blues colormap
st.markdown("<br><h5 style='text-align: center;'>Legenda Baseada no Percentil do Jogador na Liga</h5>", unsafe_allow_html=True)

def plot_color_legend():
    # Custom colors for the categories (using the same logic as in apply_colormap_based_on_value)
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    # Assign colors using the same logic
    colors = [
        cmap2(0.70),   # "Elite"
        cmap2(0.50),  # "Destaque"
        cmap(0.50),   # "Razoável"
        cmap(0.25),  # "Mediano"
        cmap1(0.30), # "Frágil"
        cmap1(0.50)  # "Péssimo"
    ]
    
    # Labels for the legend (highest to lowest)
    labels = ['Elite (>=90)', 'Destaque (75-90)', 'Razoável (60-75)', 'Mediano (40-60)', 'Frágil (20-40)', 'Péssimo (<20)']

    # Plot the legend horizontally with a smaller size
    fig, ax = plt.subplots(figsize=(6, 0.3))  # Smaller layout
    for i, (label, color) in enumerate(zip(labels[::-1], colors[::-1])):  # Reverse labels for display
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))  # Draw rectangle
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=6.0)  # Add text inside the rectangles

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Remove axes

    # Add an arrow pointing from "Highest" to "Lowest"
    ax.annotate('', xy=(6, 1), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.04, width=1.2, headwidth=5))

    return fig

# Call the function to plot the legend and display it in Streamlit
legend_fig = plot_color_legend()
st.pyplot(legend_fig)


##################################################################################################################### 
#####################################################################################################################

#Plotar Terceiro Gráfico - Radar de Métricas x Média da liga:
st.markdown(f"<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em {temporada}</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")  & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 37:44]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[37:44]]
metrics_mean['xG (pFinalização)'] = metrics_mean['xG (pFinalização)'].mean()
metrics_mean['(xG + xA) (p100 toques)'] = metrics_mean['(xG + xA) (p100 toques)'].mean()
metrics_mean['Posses recuperadas (pPosse adversária)'] = metrics_mean['Posses recuperadas (pPosse adversária)'].mean()
metrics_mean['Perdas de posse (pRecepção na linha baixa)'] = metrics_mean['Perdas de posse (pRecepção na linha baixa)'].mean()
metrics_mean['xG Chain (pPosse)'] = metrics_mean['xG Chain (pPosse)'].mean()
metrics_mean['xT Conduções (p100 Recepções)'] = metrics_mean['xT Conduções (p100 Recepções)'].mean()
metrics_mean['xT Passes (p100 Recepções)'] = metrics_mean['xT Passes (p100 Recepções)'].mean()

# Keep only the first row
metrics_mean = metrics_mean.iloc[:1]

metrics_mean['Atleta'] = 'Média da Liga' 
metrics_mean.insert(0, 'Atleta', metrics_mean.pop('Atleta'))

#Concatenate both dataframes
metrics = pd.concat([metrics, metrics_mean]).reset_index(drop=True)
metrics_list = metrics.iloc[0].tolist()
#Collecting clube
clube = attribute_chart.iat[0, 5]
posição = attribute_chart.iat[0, 8]

## parameter names
params = list(metrics.columns)
params = params[1:]

#Preparing Data
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(attribute_chart_2[params][x])
    a = a
    b = max(attribute_chart_2[params][x])
    b = b
    ranges.append((a, b))

for x in range(len(metrics['Atleta'])):
    if metrics['Atleta'][x] == jogadores:
        a_values = metrics.iloc[x].values.tolist()
    if metrics['Atleta'][x] == 'Média da Liga':
        b_values = metrics.iloc[x].values.tolist()
            
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values, b_values]

#Plotting Data
title = dict(
    title_name = jogadores,
    title_color = '#B6282F',
    title_name_2 = 'Média da Liga',
    title_color_2 = '#344D94',
    title_fontsize = 18,
) 

endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are posadj, per90'
radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
plt.savefig('Player&League_Comparison.png')
st.pyplot(fig)

##################################################################################################################### 
#####################################################################################################################
##################################################################################################################### 
#####################################################################################################################

##################################################################################################################### 
#####################################################################################################################

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Criação de Oportunidades</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[86, 88:92]].reset_index(drop=True)
metrics_criação_oportunidades_1 = metrics.iloc[:, 0].tolist()
metrics_criação_oportunidades_2 = metrics.iloc[:, 1].tolist()
metrics_criação_oportunidades_3 = metrics.iloc[:, 2].tolist()
metrics_criação_oportunidades_4 = metrics.iloc[:, 3].tolist()
metrics_criação_oportunidades_5 = metrics.iloc[:, 4].tolist()
metrics_y = [0] * len(metrics_criação_oportunidades_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[86, 88:92]].reset_index(drop=True)
highlight_criação_oportunidades_1 = highlight.iloc[:, 0].tolist()
highlight_criação_oportunidades_2 = highlight.iloc[:, 1].tolist()
highlight_criação_oportunidades_3 = highlight.iloc[:, 2].tolist()
highlight_criação_oportunidades_4 = highlight.iloc[:, 3].tolist()
highlight_criação_oportunidades_5 = highlight.iloc[:, 4].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_criação_oportunidades_1_value = pd.DataFrame(highlight_criação_oportunidades_1).reset_index(drop=True)
highlight_criação_oportunidades_2_value = pd.DataFrame(highlight_criação_oportunidades_2).reset_index(drop=True)
highlight_criação_oportunidades_3_value = pd.DataFrame(highlight_criação_oportunidades_3).reset_index(drop=True)
highlight_criação_oportunidades_4_value = pd.DataFrame(highlight_criação_oportunidades_4).reset_index(drop=True)
highlight_criação_oportunidades_5_value = pd.DataFrame(highlight_criação_oportunidades_5).reset_index(drop=True)

highlight_criação_oportunidades_1_value = highlight_criação_oportunidades_1_value.iat[0,0]
highlight_criação_oportunidades_2_value = highlight_criação_oportunidades_2_value.iat[0,0]
highlight_criação_oportunidades_3_value = highlight_criação_oportunidades_3_value.iat[0,0]
highlight_criação_oportunidades_4_value = highlight_criação_oportunidades_4_value.iat[0,0]
highlight_criação_oportunidades_5_value = highlight_criação_oportunidades_5_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_criação_oportunidades_1, metrics_criação_oportunidades_2, 
                                    metrics_criação_oportunidades_3, metrics_criação_oportunidades_4,
                                    metrics_criação_oportunidades_5])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_criação_oportunidades_1, metrics_criação_oportunidades_2, 
                                    metrics_criação_oportunidades_3, metrics_criação_oportunidades_4,
                                    metrics_criação_oportunidades_5])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função'] == "Extremo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe, clube):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[(filtered_df['Atleta'] == player_name) & (filtered_df['Clube'] == clube)]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_1_ranking_value = (get_player_rank(jogadores, liga, "xG Criado (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({criação_oportunidades_1_ranking_value}/{rows_count})"
full_title_criação_oportunidades_1 = f"xG Criado (p90) {output_str} {highlight_criação_oportunidades_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_2_ranking_value = (get_player_rank(jogadores, liga, "Passes chave (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({criação_oportunidades_2_ranking_value}/{rows_count})"
full_title_criação_oportunidades_2 = f"Passes chave (p90) {output_str} {highlight_criação_oportunidades_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_3_ranking_value = (get_player_rank(jogadores, liga, "Deep completions (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({criação_oportunidades_3_ranking_value}/{rows_count})"
full_title_criação_oportunidades_3 = f"Deep completions (p90) {output_str} {highlight_criação_oportunidades_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_4_ranking_value = (get_player_rank(jogadores, liga, "xA (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({criação_oportunidades_4_ranking_value}/{rows_count})"
full_title_criação_oportunidades_4 = f"xA (p90) {output_str} {highlight_criação_oportunidades_4_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_5_ranking_value = (get_player_rank(jogadores, liga, "Assistências (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({criação_oportunidades_5_ranking_value}/{rows_count})"
full_title_criação_oportunidades_5 = f"xT Cruzamentos (p90) {output_str} {highlight_criação_oportunidades_5_value}"

##############################################################################################################
##############################################################################################################
#From Claude version2

def calculate_ranks(values):
    """Calculate ranks for a given metric, with highest values getting rank 1"""
    return pd.Series(values).rank(ascending=False).astype(int).tolist()

def prepare_data(tabela_a, metrics_cols):
    """Prepare the metrics data dictionary with all required data"""
    metrics_data = {}
    
    for col in metrics_cols:
        # Store the metric values
        metrics_data[f'metrics_{col}'] = tabela_a[col].tolist()
        # Calculate and store ranks
        metrics_data[f'ranks_{col}'] = calculate_ranks(tabela_a[col])
        # Store player names
        metrics_data[f'player_names_{col}'] = tabela_a['Atleta'].tolist()
    
    return metrics_data

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value, equipe):
    """
    Create an interactive plot showing player attributes with hover information
    
    Parameters:
    tabela_a (pd.DataFrame): DataFrame containing all player data
    jogadores (str): Name of the player to highlight
    min_value (float): Minimum value for x-axis
    max_value (float): Maximum value for x-axis
    """
    # List of metrics to plot
    metrics_list = [
        'xG Criado (p90)', 'Passes chave (p90)', 
        'Deep completions (p90)','xA (p90)',
        'Assistências (p90)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data with additional filtering for Clube
    highlight_data = {
        f'highlight_{metric}': tabela_a[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)][metric].iloc[0]
        for metric in metrics_list
    }

    highlight_ranks = {
        metric: int(
            pd.Series(tabela_a[metric]).rank(ascending=False)[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)].iloc[0]
        )
        for metric in metrics_list
    }
    
    # Total number of players
    total_players = len(tabela_a)
    
    # Create subplots
    fig = make_subplots(
        rows=9, 
        cols=1,
        subplot_titles=[
            f"{metric.capitalize()} ({highlight_ranks[metric]}/{total_players}) {highlight_data[f'highlight_{metric}']:.2f}"
            for metric in metrics_list
        ],
        vertical_spacing=0.04
    )

    # Update subplot titles font size and color
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=17, color='black')

    # Add traces for each metric
    for idx, metric in enumerate(metrics_list, 1):
        # Add scatter plot for all players
        fig.add_trace(
            go.Scatter(
                x=metrics_data[f'metrics_{metric}'],
                y=[0] * len(metrics_data[f'metrics_{metric}']),
                mode='markers',
                name='Demais Jogadores',
                marker=dict(color='deepskyblue', size=8),
                text=[f"{rank}/{total_players}" for rank in metrics_data[f'ranks_{metric}']],
                customdata=metrics_data[f'player_names_{metric}'],
                hovertemplate='%{customdata}<br>Rank: %{text}<br>Value: %{x:.2f}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )
        
        # Add highlighted player point
        fig.add_trace(
            go.Scatter(
                x=[highlight_data[f'highlight_{metric}']],
                y=[0],
                mode='markers',
                name=jogadores,
                marker=dict(color='blue', size=12),
                hovertemplate=f'{jogadores}<br>Rank: {highlight_ranks[metric]}/{total_players}<br>Value: %{{x:.2f}}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )

    # Get the total number of metrics (subplots)
    n_metrics = len(metrics_list)

    # Update layout for each subplot
    for i in range(1, n_metrics + 1):
        if i == n_metrics:  # Only for the last subplot
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=False,
                ticktext=["PIOR", "MÉDIA (0)", "MELHOR"],
                tickvals=[min_value/2, 0, max_value/2],
                tickmode='array',
                ticks="outside",
                ticklen=2,
                tickfont=dict(size=16),
                tickangle=0,
                side='bottom',
                automargin=False,
                row=i, 
                col=1
            )
            # Adjust layout for the last subplot
            fig.update_layout(
                xaxis_tickfont_family="Arial",
                margin=dict(b=0)  # Reduce bottom margin
            )
        else:  # For all other subplots
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                showline=False,
                showticklabels=False,  # Hide tick labels
                row=i, 
                col=1
            )  # Reduces space between axis and labels

        # Update layout for the entire figure
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            showline=False,
            row=i, 
            col=1
        )

    # Update layout for the entire figure
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.20,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        margin=dict(t=100)
    )

    # Add x-axis label at the bottom
    fig.add_annotation(
        text="Desvio-padrão",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.29,
        showarrow=False,
        font=dict(size=16, color='black', weight='bold')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_criação_oportunidades_1), min(metrics_criação_oportunidades_2), 
min(metrics_criação_oportunidades_3), min(metrics_criação_oportunidades_4),
min(metrics_criação_oportunidades_5)
])  # Add padding of 0.5

max_value_test = max([
max(metrics_criação_oportunidades_1), max(metrics_criação_oportunidades_2), 
max(metrics_criação_oportunidades_3), max(metrics_criação_oportunidades_4),
max(metrics_criação_oportunidades_5)
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value,    # Maximum value for x-axis
    equipe = equipe
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo") & 
                                    (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&
                                            (attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Extremo") & 
                                            (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[66, 68:72]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[86, 88:92]].reset_index(drop=True)
metrics_percent = pd.concat([metrics, percent]).reset_index(drop=True)
#metrics_percent.rename(columns={'Atleta': 'Métricas'}, inplace=True)
metrics_percent = metrics_percent.transpose()
# Rename specific columns while keeping 'Métricas' column unchanged
metrics_percent = metrics_percent.rename(columns={
    metrics_percent.columns[0]: f'Métricas',
    metrics_percent.columns[1]: f'Percentil na Liga'
})
#st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)

# Define function to color and label cells in the "Percentil na Liga" column
def color_percentil(val):
    """
    Apply color styling based on percentile value
    """
    # Color maps from Matplotlib
    cmap = plt.get_cmap('Blues')
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")
    
    try:
        # Convert to float in case it's a string or other type
        val_num = float(val)
        
        if pd.isna(val_num):
            return ''  # No styling for NaN values
        elif val_num >= 90:
            color = cmap2(0.70)  # "Elite"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 75 <= val_num < 90:
            color = cmap2(0.50)  # "Destaque"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 60 <= val_num < 75:
            color = cmap(0.50)  # "Razoável"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 40 <= val_num < 60:
            color = cmap(0.25)  # "Mediano"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 20 <= val_num < 40:
            color = cmap1(0.30)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        else:
            color = cmap1(0.50)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
    except (ValueError, TypeError):
        return ''

# Define the styling for the entire table
styles = [
    dict(selector="th", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("color", "#333333"),
        ("font-weight", "bold"),
        ("padding", "12px 15px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black"),  # Heavier horizontal line under headers
        ("background-color", "white")
    ]),
    dict(selector="td", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("padding", "2px 5px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black")  # Horizontal lines between rows
    ]),
    # Center align specific columns
    dict(selector="th:nth-child(2), th:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="td:nth-child(2), td:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="", props=[
        ("border", "none"),  # Remove table border
        ("border-collapse", "collapse"),
        ("box-shadow", "0px 1px 3px rgba(0,0,0,0.1)")
    ]),
    # Remove vertical grid lines by not defining them
    dict(selector="tbody tr:nth-child(even)", props=[
        ("background-color", "white")
    ]),
    # Remove table outline
    dict(selector="table", props=[
        ("border", "none")
    ])
]

# Apply the styling to your dataframe
styled_df = metrics_percent.style\
    .set_table_styles(styles)\
    .applymap(color_percentil, subset=['Percentil na Liga'])\
    .format({'Métricas': '{:.2f}', 'Percentil na Liga': '{:.0f}'})

# Display in Streamlit
st.table(styled_df)
# Function to plot the legend for the 5 colors from the Blues colormap
st.markdown("<br><h5 style='text-align: center;'>Legenda Baseada no Percentil do Jogador na Liga</h5>", unsafe_allow_html=True)

def plot_color_legend():
    # Custom colors for the categories (using the same logic as in apply_colormap_based_on_value)
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    # Assign colors using the same logic
    colors = [
        cmap2(0.70),   # "Elite"
        cmap2(0.50),  # "Destaque"
        cmap(0.50),   # "Razoável"
        cmap(0.25),  # "Mediano"
        cmap1(0.30), # "Frágil"
        cmap1(0.50)  # "Péssimo"
    ]
    
    # Labels for the legend (highest to lowest)
    labels = ['Elite (>=90)', 'Destaque (75-90)', 'Razoável (60-75)', 'Mediano (40-60)', 'Frágil (20-40)', 'Péssimo (<20)']

    # Plot the legend horizontally with a smaller size
    fig, ax = plt.subplots(figsize=(6, 0.3))  # Smaller layout
    for i, (label, color) in enumerate(zip(labels[::-1], colors[::-1])):  # Reverse labels for display
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))  # Draw rectangle
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=6.0)  # Add text inside the rectangles

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Remove axes

    # Add an arrow pointing from "Highest" to "Lowest"
    ax.annotate('', xy=(6, 1), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.04, width=1.2, headwidth=5))

    return fig

# Call the function to plot the legend and display it in Streamlit
legend_fig = plot_color_legend()
st.pyplot(legend_fig)


##################################################################################################################### 
#####################################################################################################################

#Plotar Terceiro Gráfico - Radar de Métricas x Média da liga:
st.markdown(f"<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em {temporada}</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")  & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 66, 68:72]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[66, 68:72]]
metrics_mean['xG Criado (p90)'] = metrics_mean['xG Criado (p90)'].mean()
metrics_mean['Passes chave (p90)'] = metrics_mean['Passes chave (p90)'].mean()
metrics_mean['Deep completions (p90)'] = metrics_mean['Deep completions (p90)'].mean()
metrics_mean['xA (p90)'] = metrics_mean['xA (p90)'].mean()
metrics_mean['Assistências (p90)'] = metrics_mean['Assistências (p90)'].mean()

# Keep only the first row
metrics_mean = metrics_mean.iloc[:1]

metrics_mean['Atleta'] = 'Média da Liga' 
metrics_mean.insert(0, 'Atleta', metrics_mean.pop('Atleta'))

#Concatenate both dataframes
metrics = pd.concat([metrics, metrics_mean]).reset_index(drop=True)
metrics_list = metrics.iloc[0].tolist()
#Collecting clube
clube = attribute_chart.iat[0, 5]
posição = attribute_chart.iat[0, 8]

## parameter names
params = list(metrics.columns)
params = params[1:]

#Preparing Data
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(attribute_chart_2[params][x])
    a = a
    b = max(attribute_chart_2[params][x])
    b = b
    ranges.append((a, b))

for x in range(len(metrics['Atleta'])):
    if metrics['Atleta'][x] == jogadores:
        a_values = metrics.iloc[x].values.tolist()
    if metrics['Atleta'][x] == 'Média da Liga':
        b_values = metrics.iloc[x].values.tolist()
            
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values, b_values]

#Plotting Data
title = dict(
    title_name = jogadores,
    title_color = '#B6282F',
    title_name_2 = 'Média da Liga',
    title_color_2 = '#344D94',
    title_fontsize = 18,
) 

endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are posadj, per90'
radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
plt.savefig('Player&League_Comparison.png')
st.pyplot(fig)

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Ameaça Ofensiva</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")

# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[38:43]].reset_index(drop=True)
metrics_ameaça_ofensiva_1 = metrics.iloc[:, 0].tolist()
metrics_ameaça_ofensiva_2 = metrics.iloc[:, 1].tolist()
metrics_ameaça_ofensiva_3 = metrics.iloc[:, 2].tolist()
metrics_ameaça_ofensiva_4 = metrics.iloc[:, 3].tolist()
metrics_ameaça_ofensiva_5 = metrics.iloc[:, 4].tolist()
metrics_y = [0] * len(metrics_ameaça_ofensiva_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[38:43]].reset_index(drop=True)
highlight_ameaça_ofensiva_1 = highlight.iloc[:, 0].tolist()
highlight_ameaça_ofensiva_2 = highlight.iloc[:, 1].tolist()
highlight_ameaça_ofensiva_3 = highlight.iloc[:, 2].tolist()
highlight_ameaça_ofensiva_4 = highlight.iloc[:, 3].tolist()
highlight_ameaça_ofensiva_5 = highlight.iloc[:, 4].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_ameaça_ofensiva_1_value = pd.DataFrame(highlight_ameaça_ofensiva_1).reset_index(drop=True)
highlight_ameaça_ofensiva_2_value = pd.DataFrame(highlight_ameaça_ofensiva_2).reset_index(drop=True)
highlight_ameaça_ofensiva_3_value = pd.DataFrame(highlight_ameaça_ofensiva_3).reset_index(drop=True)
highlight_ameaça_ofensiva_4_value = pd.DataFrame(highlight_ameaça_ofensiva_4).reset_index(drop=True)
highlight_ameaça_ofensiva_5_value = pd.DataFrame(highlight_ameaça_ofensiva_5).reset_index(drop=True)

highlight_ameaça_ofensiva_1_value = highlight_ameaça_ofensiva_1_value.iat[0,0]
highlight_ameaça_ofensiva_2_value = highlight_ameaça_ofensiva_2_value.iat[0,0]
highlight_ameaça_ofensiva_3_value = highlight_ameaça_ofensiva_3_value.iat[0,0]
highlight_ameaça_ofensiva_4_value = highlight_ameaça_ofensiva_4_value.iat[0,0]
highlight_ameaça_ofensiva_5_value = highlight_ameaça_ofensiva_5_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_ameaça_ofensiva_1, metrics_ameaça_ofensiva_2, 
                                    metrics_ameaça_ofensiva_3, metrics_ameaça_ofensiva_4,
                                    metrics_ameaça_ofensiva_5])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_ameaça_ofensiva_1, metrics_ameaça_ofensiva_2, 
                                    metrics_ameaça_ofensiva_3, metrics_ameaça_ofensiva_4,
                                    metrics_ameaça_ofensiva_5])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função'] == "Extremo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe, clube):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[(filtered_df['Atleta'] == player_name) & (filtered_df['Clube'] == clube)]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
ameaça_ofensiva_1_ranking_value = (get_player_rank(jogadores, liga, "Recepções na área (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({ameaça_ofensiva_1_ranking_value}/{rows_count})"
full_title_ameaça_ofensiva_1 = f"Recepções na área (p90) {output_str} {highlight_ameaça_ofensiva_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
ameaça_ofensiva_2_ranking_value = (get_player_rank(jogadores, liga, "xG (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({ameaça_ofensiva_2_ranking_value}/{rows_count})"
full_title_ameaça_ofensiva_2 = f"xG (p90) {output_str} {highlight_ameaça_ofensiva_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
ameaça_ofensiva_3_ranking_value = (get_player_rank(jogadores, liga, "Gols (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({ameaça_ofensiva_3_ranking_value}/{rows_count})"
full_title_ameaça_ofensiva_3 = f"Gols (p90) {output_str} {highlight_ameaça_ofensiva_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
ameaça_ofensiva_4_ranking_value = (get_player_rank(jogadores, liga, "Entradas na área (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({ameaça_ofensiva_4_ranking_value}/{rows_count})"
full_title_ameaça_ofensiva_4 = f"Entradas na área (p90) {output_str} {highlight_ameaça_ofensiva_4_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
ameaça_ofensiva_5_ranking_value = (get_player_rank(jogadores, liga, "Toques na área (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({ameaça_ofensiva_5_ranking_value}/{rows_count})"
full_title_ameaça_ofensiva_5 = f"Toques na área (p90) {output_str} {highlight_ameaça_ofensiva_5_value}"

##############################################################################################################
##############################################################################################################
#From Claude version2

def calculate_ranks(values):
    """Calculate ranks for a given metric, with highest values getting rank 1"""
    return pd.Series(values).rank(ascending=False).astype(int).tolist()

def prepare_data(tabela_a, metrics_cols):
    """Prepare the metrics data dictionary with all required data"""
    metrics_data = {}
    
    for col in metrics_cols:
        # Store the metric values
        metrics_data[f'metrics_{col}'] = tabela_a[col].tolist()
        # Calculate and store ranks
        metrics_data[f'ranks_{col}'] = calculate_ranks(tabela_a[col])
        # Store player names
        metrics_data[f'player_names_{col}'] = tabela_a['Atleta'].tolist()
    
    return metrics_data

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value, equipe):
    """
    Create an interactive plot showing player attributes with hover information
    
    Parameters:
    tabela_a (pd.DataFrame): DataFrame containing all player data
    jogadores (str): Name of the player to highlight
    min_value (float): Minimum value for x-axis
    max_value (float): Maximum value for x-axis
    """
    # List of metrics to plot
    metrics_list = [
        'Recepções na área (p90)', 'xG (p90)', 
        'Gols (p90)', 'Entradas na área (p90)',
        'Toques na área (p90)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data with additional filtering for Clube
    highlight_data = {
        f'highlight_{metric}': tabela_a[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)][metric].iloc[0]
        for metric in metrics_list
    }

    highlight_ranks = {
        metric: int(
            pd.Series(tabela_a[metric]).rank(ascending=False)[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)].iloc[0]
        )
        for metric in metrics_list
    }
    
    # Total number of players
    total_players = len(tabela_a)
    
    # Create subplots
    fig = make_subplots(
        rows=9, 
        cols=1,
        subplot_titles=[
            f"{metric.capitalize()} ({highlight_ranks[metric]}/{total_players}) {highlight_data[f'highlight_{metric}']:.2f}"
            for metric in metrics_list
        ],
        vertical_spacing=0.04
    )

    # Update subplot titles font size and color
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=17, color='black')

    # Add traces for each metric
    for idx, metric in enumerate(metrics_list, 1):
        # Add scatter plot for all players
        fig.add_trace(
            go.Scatter(
                x=metrics_data[f'metrics_{metric}'],
                y=[0] * len(metrics_data[f'metrics_{metric}']),
                mode='markers',
                name='Demais Jogadores',
                marker=dict(color='deepskyblue', size=8),
                text=[f"{rank}/{total_players}" for rank in metrics_data[f'ranks_{metric}']],
                customdata=metrics_data[f'player_names_{metric}'],
                hovertemplate='%{customdata}<br>Rank: %{text}<br>Value: %{x:.2f}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )
        
        # Add highlighted player point
        fig.add_trace(
            go.Scatter(
                x=[highlight_data[f'highlight_{metric}']],
                y=[0],
                mode='markers',
                name=jogadores,
                marker=dict(color='blue', size=12),
                hovertemplate=f'{jogadores}<br>Rank: {highlight_ranks[metric]}/{total_players}<br>Value: %{{x:.2f}}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )

    # Get the total number of metrics (subplots)
    n_metrics = len(metrics_list)

    # Update layout for each subplot
    for i in range(1, n_metrics + 1):
        if i == n_metrics:  # Only for the last subplot
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=False,
                ticktext=["PIOR", "MÉDIA (0)", "MELHOR"],
                tickvals=[min_value/2, 0, max_value/2],
                tickmode='array',
                ticks="outside",
                ticklen=2,
                tickfont=dict(size=16),
                tickangle=0,
                side='bottom',
                automargin=False,
                row=i, 
                col=1
            )
            # Adjust layout for the last subplot
            fig.update_layout(
                xaxis_tickfont_family="Arial",
                margin=dict(b=0)  # Reduce bottom margin
            )
        else:  # For all other subplots
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                showline=False,
                showticklabels=False,  # Hide tick labels
                row=i, 
                col=1
            )  # Reduces space between axis and labels

        # Update layout for the entire figure
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            showline=False,
            row=i, 
            col=1
        )

    # Update layout for the entire figure
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.20,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        margin=dict(t=100)
    )

    # Add x-axis label at the bottom
    fig.add_annotation(
        text="Desvio-padrão",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.29,
        showarrow=False,
        font=dict(size=16, color='blue', weight='bold')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_ameaça_ofensiva_1), min(metrics_ameaça_ofensiva_2), 
min(metrics_ameaça_ofensiva_3), min(metrics_ameaça_ofensiva_4),
min(metrics_ameaça_ofensiva_5)
])  # Add padding of 0.5

max_value_test = max([
max(metrics_ameaça_ofensiva_1), max(metrics_ameaça_ofensiva_2), 
max(metrics_ameaça_ofensiva_3), max(metrics_ameaça_ofensiva_4),
max(metrics_ameaça_ofensiva_5)
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value,    # Maximum value for x-axis
    equipe = equipe
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & 
                                    (attribute_chart['função']=="Extremo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&
                                            (attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Extremo") & 
                                            (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[18:23]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[38:43]].reset_index(drop=True)
metrics_percent = pd.concat([metrics, percent]).reset_index(drop=True)
metrics_percent = metrics_percent.transpose()
# Rename specific columns while keeping 'Métricas' column unchanged
metrics_percent = metrics_percent.rename(columns={
    metrics_percent.columns[0]: f'Métricas',
    metrics_percent.columns[1]: f'Percentil na Liga'
})
st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)

# Define function to color and label cells in the "Percentil na Liga" column
def color_percentil(val):
    """
    Apply color styling based on percentile value
    """
    # Color maps from Matplotlib
    cmap = plt.get_cmap('Blues')
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")
    
    try:
        # Convert to float in case it's a string or other type
        val_num = float(val)
        
        if pd.isna(val_num):
            return ''  # No styling for NaN values
        elif val_num >= 90:
            color = cmap2(0.70)  # "Elite"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 75 <= val_num < 90:
            color = cmap2(0.50)  # "Destaque"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 60 <= val_num < 75:
            color = cmap(0.50)  # "Razoável"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 40 <= val_num < 60:
            color = cmap(0.25)  # "Mediano"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 20 <= val_num < 40:
            color = cmap1(0.30)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        else:
            color = cmap1(0.50)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
    except (ValueError, TypeError):
        return ''

# Define the styling for the entire table
styles = [
    dict(selector="th", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("color", "#333333"),
        ("font-weight", "bold"),
        ("padding", "12px 15px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black"),  # Heavier horizontal line under headers
        ("background-color", "white")
    ]),
    dict(selector="td", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("padding", "2px 5px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black")  # Horizontal lines between rows
    ]),
    # Center align specific columns
    dict(selector="th:nth-child(2), th:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="td:nth-child(2), td:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="", props=[
        ("border", "none"),  # Remove table border
        ("border-collapse", "collapse"),
        ("box-shadow", "0px 1px 3px rgba(0,0,0,0.1)")
    ]),
    # Remove vertical grid lines by not defining them
    dict(selector="tbody tr:nth-child(even)", props=[
        ("background-color", "white")
    ]),
    # Remove table outline
    dict(selector="table", props=[
        ("border", "none")
    ])
]

# Apply the styling to your dataframe
styled_df = metrics_percent.style\
    .set_table_styles(styles)\
    .applymap(color_percentil, subset=['Percentil na Liga'])\
    .format({'Métricas': '{:.2f}', 'Percentil na Liga': '{:.0f}'})

# Display in Streamlit
st.table(styled_df)
# Function to plot the legend for the 5 colors from the Blues colormap
st.markdown("<br><h5 style='text-align: center;'>Legenda Baseada no Percentil do Jogador na Liga</h5>", unsafe_allow_html=True)

def plot_color_legend():
    # Custom colors for the categories (using the same logic as in apply_colormap_based_on_value)
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    # Assign colors using the same logic
    colors = [
        cmap2(0.70),   # "Elite"
        cmap2(0.50),  # "Destaque"
        cmap(0.50),   # "Razoável"
        cmap(0.25),  # "Mediano"
        cmap1(0.30), # "Frágil"
        cmap1(0.50)  # "Péssimo"
    ]
    
    # Labels for the legend (highest to lowest)
    labels = ['Elite (>=90)', 'Destaque (75-90)', 'Razoável (60-75)', 'Mediano (40-60)', 'Frágil (20-40)', 'Péssimo (<20)']

    # Plot the legend horizontally with a smaller size
    fig, ax = plt.subplots(figsize=(6, 0.3))  # Smaller layout
    for i, (label, color) in enumerate(zip(labels[::-1], colors[::-1])):  # Reverse labels for display
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))  # Draw rectangle
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=6.0)  # Add text inside the rectangles

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Remove axes

    # Add an arrow pointing from "Highest" to "Lowest"
    ax.annotate('', xy=(6, 1), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.04, width=1.2, headwidth=5))

    return fig

# Call the function to plot the legend and display it in Streamlit
legend_fig = plot_color_legend()
st.pyplot(legend_fig)


##################################################################################################################### 
#####################################################################################################################

#Plotar Terceiro Gráfico - Radar de Métricas x Média da liga:
st.markdown(f"<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em {temporada}</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")  & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 18:23]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[18:23]]
metrics_mean['Recepções na área (p90)'] = metrics_mean['Recepções na área (p90)'].mean()
metrics_mean['xG (p90)'] = metrics_mean['xG (p90)'].mean()
metrics_mean['Gols (p90)'] = metrics_mean['Gols (p90)'].mean()
metrics_mean['Entradas na área (p90)'] = metrics_mean['Entradas na área (p90)'].mean()
metrics_mean['Toques na área (p90)'] = metrics_mean['Toques na área (p90)'].mean()

# Keep only the first row
metrics_mean = metrics_mean.iloc[:1]

metrics_mean['Atleta'] = 'Média da Liga' 
metrics_mean.insert(0, 'Atleta', metrics_mean.pop('Atleta'))

#Concatenate both dataframes
metrics = pd.concat([metrics, metrics_mean]).reset_index(drop=True)
metrics_list = metrics.iloc[0].tolist()
#Collecting clube
clube = attribute_chart.iat[0, 5]
posição = attribute_chart.iat[0, 8]

## parameter names
params = list(metrics.columns)
params = params[1:]

#Preparing Data
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(attribute_chart_2[params][x])
    a = a
    b = max(attribute_chart_2[params][x])
    b = b
    ranges.append((a, b))

for x in range(len(metrics['Atleta'])):
    if metrics['Atleta'][x] == jogadores:
        a_values = metrics.iloc[x].values.tolist()
    if metrics['Atleta'][x] == 'Média da Liga':
        b_values = metrics.iloc[x].values.tolist()
            
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values, b_values]

#Plotting Data
title = dict(
    title_name = jogadores,
    title_color = '#B6282F',
    title_name_2 = 'Média da Liga',
    title_color_2 = '#344D94',
    title_fontsize = 18,
) 

endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are posadj, per90'
radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
plt.savefig('Player&League_Comparison.png')
st.pyplot(fig)


##############################################################################################################################
##############################################################################################################################

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Finalização</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[64:67, 40]].reset_index(drop=True)
metrics_finalização_1 = metrics.iloc[:, 0].tolist()
metrics_finalização_2 = metrics.iloc[:, 1].tolist()
metrics_finalização_3 = metrics.iloc[:, 2].tolist()
metrics_finalização_4 = metrics.iloc[:, 3].tolist()
metrics_y = [0] * len(metrics_finalização_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores)]
highlight = highlight.iloc[:, np.r_[64:67, 40]].reset_index(drop=True)
highlight_finalização_1 = highlight.iloc[:, 0].tolist()
highlight_finalização_2 = highlight.iloc[:, 1].tolist()
highlight_finalização_3 = highlight.iloc[:, 2].tolist()
highlight_finalização_4 = highlight.iloc[:, 3].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_finalização_1_value = pd.DataFrame(highlight_finalização_1).reset_index(drop=True)
highlight_finalização_2_value = pd.DataFrame(highlight_finalização_2).reset_index(drop=True)
highlight_finalização_3_value = pd.DataFrame(highlight_finalização_3).reset_index(drop=True)
highlight_finalização_4_value = pd.DataFrame(highlight_finalização_4).reset_index(drop=True)

highlight_finalização_1_value = highlight_finalização_1_value.iat[0,0]
highlight_finalização_2_value = highlight_finalização_2_value.iat[0,0]
highlight_finalização_3_value = highlight_finalização_3_value.iat[0,0]
highlight_finalização_4_value = highlight_finalização_4_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_finalização_1, metrics_finalização_2, 
                                    metrics_finalização_3, metrics_finalização_4])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_finalização_1, metrics_finalização_2, 
                                    metrics_finalização_3, metrics_finalização_4])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função'] == "Extremo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe, clube):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[(filtered_df['Atleta'] == player_name) & (filtered_df['Clube'] == clube)]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None



# Building the Extended Title"
# Determining player's rank in attribute in league
finalização_1_ranking_value = (get_player_rank(jogadores, liga, "(Gols - xG)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({finalização_1_ranking_value}/{rows_count})"
full_title_finalização_1 = f"(Gols - xG) {output_str} {highlight_finalização_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
finalização_2_ranking_value = (get_player_rank(jogadores, liga, "xGOT (xG no alvo) (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({finalização_2_ranking_value}/{rows_count})"
full_title_finalização_2 = f"xGOT (xG no alvo) (p90) {output_str} {highlight_finalização_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
finalização_3_ranking_value = (get_player_rank(jogadores, liga, "Conversão de finalizações (%)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({finalização_3_ranking_value}/{rows_count})"
full_title_finalização_3 = f"Conversão de finalizações (%) {output_str} {highlight_finalização_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
finalização_4_ranking_value = (get_player_rank(jogadores, liga, "Gols (p90)", attribute_chart_z1, equipe))

# Data to plot
output_str = f"({finalização_4_ranking_value}/{rows_count})"
full_title_finalização_4 = f"Gols (p90) {output_str} {highlight_finalização_4_value}"

##############################################################################################################
##############################################################################################################
#From Claude version2

def calculate_ranks(values):
    """Calculate ranks for a given metric, with highest values getting rank 1"""
    return pd.Series(values).rank(ascending=False).astype(int).tolist()

def prepare_data(tabela_a, metrics_cols):
    """Prepare the metrics data dictionary with all required data"""
    metrics_data = {}
    
    for col in metrics_cols:
        # Store the metric values
        metrics_data[f'metrics_{col}'] = tabela_a[col].tolist()
        # Calculate and store ranks
        metrics_data[f'ranks_{col}'] = calculate_ranks(tabela_a[col])
        # Store player names
        metrics_data[f'player_names_{col}'] = tabela_a['Atleta'].tolist()
    
    return metrics_data

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value, equipe):
    """
    Create an interactive plot showing player attributes with hover information
    
    Parameters:
    tabela_a (pd.DataFrame): DataFrame containing all player data
    jogadores (str): Name of the player to highlight
    min_value (float): Minimum value for x-axis
    max_value (float): Maximum value for x-axis
    """
    # List of metrics to plot
    metrics_list = [
        '(Gols - xG)', 'xGOT (xG no alvo) (p90)', 
        'Conversão de finalizações (%)','Gols (p90)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data with additional filtering for Clube
    highlight_data = {
        f'highlight_{metric}': tabela_a[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)][metric].iloc[0]
        for metric in metrics_list
    }

    highlight_ranks = {
        metric: int(
            pd.Series(tabela_a[metric]).rank(ascending=False)[(tabela_a['Atleta'] == jogadores) & (tabela_a['Clube'] == equipe)].iloc[0]
        )
        for metric in metrics_list
    }
    
    # Total number of players
    total_players = len(tabela_a)
    
    # Create subplots
    fig = make_subplots(
        rows=9, 
        cols=1,
        subplot_titles=[
            f"{metric.capitalize()} ({highlight_ranks[metric]}/{total_players}) {highlight_data[f'highlight_{metric}']:.2f}"
            for metric in metrics_list
        ],
        vertical_spacing=0.04
    )

    # Update subplot titles font size and color
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=17, color='black')

    # Add traces for each metric
    for idx, metric in enumerate(metrics_list, 1):
        # Add scatter plot for all players
        fig.add_trace(
            go.Scatter(
                x=metrics_data[f'metrics_{metric}'],
                y=[0] * len(metrics_data[f'metrics_{metric}']),
                mode='markers',
                name='Demais Jogadores',
                marker=dict(color='deepskyblue', size=8),
                text=[f"{rank}/{total_players}" for rank in metrics_data[f'ranks_{metric}']],
                customdata=metrics_data[f'player_names_{metric}'],
                hovertemplate='%{customdata}<br>Rank: %{text}<br>Value: %{x:.2f}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )
        
        # Add highlighted player point
        fig.add_trace(
            go.Scatter(
                x=[highlight_data[f'highlight_{metric}']],
                y=[0],
                mode='markers',
                name=jogadores,
                marker=dict(color='blue', size=12),
                hovertemplate=f'{jogadores}<br>Rank: {highlight_ranks[metric]}/{total_players}<br>Value: %{{x:.2f}}<extra></extra>',
                showlegend=True if idx == 1 else False
            ),
            row=idx, 
            col=1
        )

    # Get the total number of metrics (subplots)
    n_metrics = len(metrics_list)

    # Update layout for each subplot
    for i in range(1, n_metrics + 1):
        if i == n_metrics:  # Only for the last subplot
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=False,
                ticktext=["PIOR", "MÉDIA (0)", "MELHOR"],
                tickvals=[min_value/2, 0, max_value/2],
                tickmode='array',
                ticks="outside",
                ticklen=2,
                tickfont=dict(size=16),
                tickangle=0,
                side='bottom',
                automargin=False,
                row=i, 
                col=1
            )
            # Adjust layout for the last subplot
            fig.update_layout(
                xaxis_tickfont_family="Arial",
                margin=dict(b=0)  # Reduce bottom margin
            )
        else:  # For all other subplots
            fig.update_xaxes(
                range=[min_value, max_value],
                showgrid=False,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                showline=False,
                showticklabels=False,  # Hide tick labels
                row=i, 
                col=1
            )  # Reduces space between axis and labels

        # Update layout for the entire figure
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            showline=False,
            row=i, 
            col=1
        )

    # Update layout for the entire figure
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.38,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        margin=dict(t=100)
    )

    # Add x-axis label at the bottom
    fig.add_annotation(
        text="Desvio-padrão",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.47,
        showarrow=False,
        font=dict(size=16, color='blue', weight='bold')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_finalização_1), min(metrics_finalização_2), 
min(metrics_finalização_3), min(metrics_finalização_4),
])  # Add padding of 0.5

max_value_test = max([
max(metrics_finalização_1), max(metrics_finalização_2), 
max(metrics_finalização_3), max(metrics_finalização_4),
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value,    # Maximum value for x-axis
    equipe = equipe
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################
    
#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & 
                                    (attribute_chart['função']=="Extremo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&
                                            (attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Extremo") & 
                                            (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[44:47, 20]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[64:67, 40]].reset_index(drop=True)
metrics_percent = pd.concat([metrics, percent]).reset_index(drop=True)
metrics_percent = metrics_percent.transpose()
metrics_percent = metrics_percent.rename(columns={
    metrics_percent.columns[0]: f'Métricas',
    metrics_percent.columns[1]: f'Percentil na Liga'
})
st.markdown("<h4 style='text-align: center;'>Desempenho do Jogador na Liga/Temporada</h4>", unsafe_allow_html=True)

# Define function to color and label cells in the "Percentil na Liga" column
def color_percentil(val):
    """
    Apply color styling based on percentile value
    """
    # Color maps from Matplotlib
    cmap = plt.get_cmap('Blues')
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")
    
    try:
        # Convert to float in case it's a string or other type
        val_num = float(val)
        
        if pd.isna(val_num):
            return ''  # No styling for NaN values
        elif val_num >= 90:
            color = cmap2(0.70)  # "Elite"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 75 <= val_num < 90:
            color = cmap2(0.50)  # "Destaque"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 60 <= val_num < 75:
            color = cmap(0.50)  # "Razoável"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 40 <= val_num < 60:
            color = cmap(0.25)  # "Mediano"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        elif 20 <= val_num < 40:
            color = cmap1(0.30)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
        else:
            color = cmap1(0.50)  # Orange color for "Frágil"
            return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black; text-align: center'
    except (ValueError, TypeError):
        return ''

# Define the styling for the entire table
styles = [
    dict(selector="th", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("color", "#333333"),
        ("font-weight", "bold"),
        ("padding", "12px 15px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black"),  # Heavier horizontal line under headers
        ("background-color", "white")
    ]),
    dict(selector="td", props=[
        ("font-family", "Helvetica"),
        ("font-size", "16px"),
        ("padding", "2px 5px"),
        ("border", "none"),  # Remove all borders
        ("border-bottom", "1px solid black")  # Horizontal lines between rows
    ]),
    # Center align specific columns
    dict(selector="th:nth-child(2), th:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="td:nth-child(2), td:nth-child(3)", props=[
        ("text-align", "center !important")
    ]),
    dict(selector="", props=[
        ("border", "none"),  # Remove table border
        ("border-collapse", "collapse"),
        ("box-shadow", "0px 1px 3px rgba(0,0,0,0.1)")
    ]),
    # Remove vertical grid lines by not defining them
    dict(selector="tbody tr:nth-child(even)", props=[
        ("background-color", "white")
    ]),
    # Remove table outline
    dict(selector="table", props=[
        ("border", "none")
    ])
]

# Apply the styling to your dataframe
styled_df = metrics_percent.style\
    .set_table_styles(styles)\
    .applymap(color_percentil, subset=['Percentil na Liga'])\
    .format({'Métricas': '{:.2f}', 'Percentil na Liga': '{:.0f}'})

# Display in Streamlit
st.table(styled_df)
# Function to plot the legend for the 5 colors from the Blues colormap
st.markdown("<br><h5 style='text-align: center;'>Legenda Baseada no Percentil do Jogador na Liga</h5>", unsafe_allow_html=True)

def plot_color_legend():
    # Custom colors for the categories (using the same logic as in apply_colormap_based_on_value)
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    # Assign colors using the same logic
    colors = [
        cmap2(0.70),   # "Elite"
        cmap2(0.50),  # "Destaque"
        cmap(0.50),   # "Razoável"
        cmap(0.25),  # "Mediano"
        cmap1(0.30), # "Frágil"
        cmap1(0.50)  # "Péssimo"
    ]
    
    # Labels for the legend (highest to lowest)
    labels = ['Elite (>=90)', 'Destaque (75-90)', 'Razoável (60-75)', 'Mediano (40-60)', 'Frágil (20-40)', 'Péssimo (<20)']

    # Plot the legend horizontally with a smaller size
    fig, ax = plt.subplots(figsize=(6, 0.3))  # Smaller layout
    for i, (label, color) in enumerate(zip(labels[::-1], colors[::-1])):  # Reverse labels for display
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))  # Draw rectangle
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=6.0)  # Add text inside the rectangles

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Remove axes

    # Add an arrow pointing from "Highest" to "Lowest"
    ax.annotate('', xy=(6, 1), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.04, width=1.2, headwidth=5))

    return fig

# Call the function to plot the legend and display it in Streamlit
legend_fig = plot_color_legend()
st.pyplot(legend_fig)


##################################################################################################################### 
#####################################################################################################################

#Plotar Terceiro Gráfico - Radar de Métricas x Média da liga:
st.markdown(f"<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em {temporada}</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")  & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Extremo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 44:47, 20]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[44:47, 20]]
metrics_mean['(Gols - xG)'] = metrics_mean['(Gols - xG)'].mean()
metrics_mean['xGOT (xG no alvo) (p90)'] = metrics_mean['xGOT (xG no alvo) (p90)'].mean()
metrics_mean['Conversão de finalizações (%)'] = metrics_mean['Conversão de finalizações (%)'].mean()
metrics_mean['Gols (p90)'] = metrics_mean['Gols (p90)'].mean()

# Keep only the first row
metrics_mean = metrics_mean.iloc[:1]

metrics_mean['Atleta'] = 'Média da Liga' 
metrics_mean.insert(0, 'Atleta', metrics_mean.pop('Atleta'))

#Concatenate both dataframes
metrics = pd.concat([metrics, metrics_mean]).reset_index(drop=True)
metrics_list = metrics.iloc[0].tolist()
#Collecting clube
clube = attribute_chart.iat[0, 5]
posição = attribute_chart.iat[0, 8]

## parameter names
params = list(metrics.columns)
params = params[1:]

#Preparing Data
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(attribute_chart_2[params][x])
    a = a
    b = max(attribute_chart_2[params][x])
    b = b
    ranges.append((a, b))

for x in range(len(metrics['Atleta'])):
    if metrics['Atleta'][x] == jogadores:
        a_values = metrics.iloc[x].values.tolist()
    if metrics['Atleta'][x] == 'Média da Liga':
        b_values = metrics.iloc[x].values.tolist()
            
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values, b_values]

#Plotting Data
title = dict(
    title_name = jogadores,
    title_color = '#B6282F',
    title_name_2 = 'Média da Liga',
    title_color_2 = '#344D94',
    title_fontsize = 18,
) 

endnote = 'Viz by@JAmerico1898\ Data from Wyscout\nAll features are posadj, per90'
radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,radar_color=['#B6282F', '#344D94'], dpi=600, alphas=[.8,.6], title=title, endnote=endnote, compare=True)
plt.savefig('Player&League_Comparison.png')
st.pyplot(fig)
