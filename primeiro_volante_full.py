atributos_primeiro_volante = ['Participação', 'Intensidade defensiva', 'Inteligência defensiva', 
                        'Transição ofensiva', 'Impacto do passe', 'Criação de oportunidades']


# Dynamically create the HTML string with the 'jogadores' variable
title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"
# Use the dynamically created HTML string in st.markdown
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Participação</h3>", unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Meio Campo")]
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
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['Posição'] == "Primeiro Volante")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[filtered_df['Atleta'] == player_name]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
participação_1_ranking_value = (get_player_rank(jogadores, liga, "xG gerado na construção (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({participação_1_ranking_value}/{rows_count})"
full_title_participação_1 = f"xG gerado na construção (p90) {output_str} {highlight_participação_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
participação_2_ranking_value = (get_player_rank(jogadores, liga, "Toques (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({participação_2_ranking_value}/{rows_count})"
full_title_participação_2 = f"Toques (p90) {output_str} {highlight_participação_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
participação_3_ranking_value = (get_player_rank(jogadores, liga, "Ações defensivas (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({participação_3_ranking_value}/{rows_count})"
full_title_participação_3 = f"Ações defensivas (p90) {output_str} {highlight_participação_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
participação_4_ranking_value = (get_player_rank(jogadores, liga, "Disputas aéreas (p90)", attribute_chart_z1))

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

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value):
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
    
    # Calculate highlight data
    highlight_data = {
        f'highlight_{metric}': tabela_a[tabela_a['Atleta'] == jogadores][metric].iloc[0]
        for metric in metrics_list
    }
    
    # Calculate highlight ranks
    highlight_ranks = {
        metric: int(pd.Series(tabela_a[metric]).rank(ascending=False)[tabela_a['Atleta'] == jogadores].iloc[0])
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
        font=dict(size=16, color='blue')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_participação_1), min(metrics_participação_2), 
min(metrics_participação_3), min(metrics_participação_4),
])  # Add padding of 0.5

max_value_test = max([
min(metrics_participação_1), min(metrics_participação_2), 
min(metrics_participação_3), min(metrics_participação_4),
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value    # Maximum value for x-axis
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################
    
#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&(attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Meio Campo") & (attribute_chart_per['Clube']==equipe)]
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
st.markdown("<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em 2024</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
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
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Intensidade Defensiva</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Meio Campo")]
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[29, 30, 31, 32]].reset_index(drop=True)
metrics_intensidade_defensiva_1 = metrics.iloc[:, 0].tolist()
metrics_intensidade_defensiva_2 = metrics.iloc[:, 1].tolist()
metrics_intensidade_defensiva_3 = metrics.iloc[:, 2].tolist()
metrics_intensidade_defensiva_4 = metrics.iloc[:, 3].tolist()
metrics_y = [0] * len(metrics_intensidade_defensiva_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[29, 30, 31, 32]].reset_index(drop=True)
highlight_intensidade_defensiva_1 = highlight.iloc[:, 0].tolist()
highlight_intensidade_defensiva_2 = highlight.iloc[:, 1].tolist()
highlight_intensidade_defensiva_3 = highlight.iloc[:, 2].tolist()
highlight_intensidade_defensiva_4 = highlight.iloc[:, 3].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_intensidade_defensiva_1_value = pd.DataFrame(highlight_intensidade_defensiva_1).reset_index(drop=True)
highlight_intensidade_defensiva_2_value = pd.DataFrame(highlight_intensidade_defensiva_2).reset_index(drop=True)
highlight_intensidade_defensiva_3_value = pd.DataFrame(highlight_intensidade_defensiva_3).reset_index(drop=True)
highlight_intensidade_defensiva_4_value = pd.DataFrame(highlight_intensidade_defensiva_4).reset_index(drop=True)

highlight_intensidade_defensiva_1_value = highlight_intensidade_defensiva_1_value.iat[0,0]
highlight_intensidade_defensiva_2_value = highlight_intensidade_defensiva_2_value.iat[0,0]
highlight_intensidade_defensiva_3_value = highlight_intensidade_defensiva_3_value.iat[0,0]
highlight_intensidade_defensiva_4_value = highlight_intensidade_defensiva_4_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_intensidade_defensiva_1, metrics_intensidade_defensiva_2, 
                                    metrics_intensidade_defensiva_3, metrics_intensidade_defensiva_4])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_intensidade_defensiva_1, metrics_intensidade_defensiva_2, 
                                    metrics_intensidade_defensiva_3, metrics_intensidade_defensiva_4])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['Posição'] == "Primeiro Volante")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[filtered_df['Atleta'] == player_name]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
intensidade_defensiva_1_ranking_value = (get_player_rank(jogadores, liga, "Sucesso em desarmes (%)", attribute_chart_z1))

# Data to plot
output_str = f"({intensidade_defensiva_1_ranking_value}/{rows_count})"
full_title_intensidade_defensiva_1 = f"Sucesso em desarmes (%) {output_str} {highlight_intensidade_defensiva_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
intensidade_defensiva_2_ranking_value = (get_player_rank(jogadores, liga, "Posses recuperadas (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({intensidade_defensiva_2_ranking_value}/{rows_count})"
full_title_intensidade_defensiva_2 = f"Posses recuperadas (p90) {output_str} {highlight_intensidade_defensiva_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
intensidade_defensiva_3_ranking_value = (get_player_rank(jogadores, liga, "Ações defensivas (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({intensidade_defensiva_3_ranking_value}/{rows_count})"
full_title_intensidade_defensiva_3 = f"Ações defensivas (p90) {output_str} {highlight_intensidade_defensiva_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
intensidade_defensiva_4_ranking_value = (get_player_rank(jogadores, liga, "Sucesso em 1v1 defensivo (%)", attribute_chart_z1))

# Data to plot
output_str = f"({intensidade_defensiva_4_ranking_value}/{rows_count})"
full_title_intensidade_defensiva_4 = f"Sucesso em 1v1 defensivo (%) {output_str} {highlight_intensidade_defensiva_4_value}"

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

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value):
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
        'Sucesso em desarmes (%)', 'Posses recuperadas (p90)', 
        'Ações defensivas (p90)','Sucesso em 1v1 defensivo (%)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data
    highlight_data = {
        f'highlight_{metric}': tabela_a[tabela_a['Atleta'] == jogadores][metric].iloc[0]
        for metric in metrics_list
    }
    
    # Calculate highlight ranks
    highlight_ranks = {
        metric: int(pd.Series(tabela_a[metric]).rank(ascending=False)[tabela_a['Atleta'] == jogadores].iloc[0])
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
        font=dict(size=16, color='blue')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_intensidade_defensiva_1), min(metrics_intensidade_defensiva_2), 
min(metrics_intensidade_defensiva_3), min(metrics_intensidade_defensiva_4),
])  # Add padding of 0.5

max_value_test = max([
max(metrics_intensidade_defensiva_1), max(metrics_intensidade_defensiva_2), 
max(metrics_intensidade_defensiva_3), max(metrics_intensidade_defensiva_4),
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value    # Maximum value for x-axis
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&(attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Meio Campo") & (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[9:13]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[29:33]].reset_index(drop=True)
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
st.markdown("<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em 2024</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 9:13]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[9:13]]
metrics_mean['Sucesso em desarmes (%)'] = metrics_mean['Sucesso em desarmes (%)'].mean()
metrics_mean['Posses recuperadas (p90)'] = metrics_mean['Posses recuperadas (p90)'].mean()
metrics_mean['Ações defensivas (p90)'] = metrics_mean['Ações defensivas (p90)'].mean()
metrics_mean['Sucesso em 1v1 defensivo (%)'] = metrics_mean['Sucesso em 1v1 defensivo (%)'].mean()

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

#################################################################################################################################
#################################################################################################################################
# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Inteligência Defensiva</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Meio Campo")]
attribute_chart_z1.rename(columns={"counterpressing": "Contra-pressão (p90)"}, inplace=True)
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[69:72]].reset_index(drop=True)
metrics_inteligência_defensiva_1 = metrics.iloc[:, 0].tolist()
metrics_inteligência_defensiva_2 = metrics.iloc[:, 1].tolist()
metrics_inteligência_defensiva_3 = metrics.iloc[:, 2].tolist()
metrics_y = [0] * len(metrics_inteligência_defensiva_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[69:72]].reset_index(drop=True)
highlight_inteligência_defensiva_1 = highlight.iloc[:, 0].tolist()
highlight_inteligência_defensiva_2 = highlight.iloc[:, 1].tolist()
highlight_inteligência_defensiva_3 = highlight.iloc[:, 2].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_inteligência_defensiva_1_value = pd.DataFrame(highlight_inteligência_defensiva_1).reset_index(drop=True)
highlight_inteligência_defensiva_2_value = pd.DataFrame(highlight_inteligência_defensiva_2).reset_index(drop=True)
highlight_inteligência_defensiva_3_value = pd.DataFrame(highlight_inteligência_defensiva_3).reset_index(drop=True)

highlight_inteligência_defensiva_1_value = highlight_inteligência_defensiva_1_value.iat[0,0]
highlight_inteligência_defensiva_2_value = highlight_inteligência_defensiva_2_value.iat[0,0]
highlight_inteligência_defensiva_3_value = highlight_inteligência_defensiva_3_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_inteligência_defensiva_1, metrics_inteligência_defensiva_2, 
                                    metrics_inteligência_defensiva_3])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_inteligência_defensiva_1, metrics_inteligência_defensiva_2, 
                                    metrics_inteligência_defensiva_3])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['Posição'] == "Primeiro Volante")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[filtered_df['Atleta'] == player_name]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
inteligência_defensiva_1_ranking_value = (get_player_rank(jogadores, liga, "Interceptações (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({inteligência_defensiva_1_ranking_value}/{rows_count})"
full_title_inteligência_defensiva_1 = f"Interceptações (p90) {output_str} {highlight_inteligência_defensiva_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
inteligência_defensiva_2_ranking_value = (get_player_rank(jogadores, liga, "Contra-pressão (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({inteligência_defensiva_2_ranking_value}/{rows_count})"
full_title_inteligência_defensiva_2 = f"Contra-pressão (p90) {output_str} {highlight_inteligência_defensiva_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
inteligência_defensiva_3_ranking_value = (get_player_rank(jogadores, liga, "Recuperações de bola (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({inteligência_defensiva_3_ranking_value}/{rows_count})"
full_title_inteligência_defensiva_3 = f"Recuperações de bola (p90) {output_str} {highlight_inteligência_defensiva_3_value}"

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

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value):
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
        'Interceptações (p90)', 'Contra-pressão (p90)', 
        'Recuperações de bola (p90)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data
    highlight_data = {
        f'highlight_{metric}': tabela_a[tabela_a['Atleta'] == jogadores][metric].iloc[0]
        for metric in metrics_list
    }
    
    # Calculate highlight ranks
    highlight_ranks = {
        metric: int(pd.Series(tabela_a[metric]).rank(ascending=False)[tabela_a['Atleta'] == jogadores].iloc[0])
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
        font=dict(size=16, color='blue')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_inteligência_defensiva_1), min(metrics_inteligência_defensiva_2), 
min(metrics_inteligência_defensiva_3)
])  # Add padding of 0.5

max_value_test = max([
min(metrics_inteligência_defensiva_1), min(metrics_inteligência_defensiva_2), 
min(metrics_inteligência_defensiva_3)
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value    # Maximum value for x-axis
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart.rename(columns={"counterpressing": "Contra-pressão (p90)"}, inplace=True)
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_per.rename(columns={"counterpressing": "Contra-pressão (p90)"}, inplace=True)
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&(attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Meio Campo") & (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[49:52]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[69:72]].reset_index(drop=True)
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
st.markdown("<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em 2024</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 49:52]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[49:52]]
metrics_mean['Interceptações (p90)'] = metrics_mean['Interceptações (p90)'].mean()
metrics_mean['Contra-pressão (p90)'] = metrics_mean['Contra-pressão (p90)'].mean()
metrics_mean['Recuperações de bola (p90)'] = metrics_mean['Recuperações de bola (p90)'].mean()

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

#################################################################################################################################
#################################################################################################################################

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Transição Ofensiva</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Meio Campo")]
attribute_chart_z1.rename(columns={"counterpressing": "Contra-pressão (p90)"}, inplace=True)
#Collecting data to plot
metrics = attribute_chart_z1.iloc[:, np.r_[84, 77, 85]].reset_index(drop=True)
metrics_transição_ofensiva_1 = metrics.iloc[:, 0].tolist()
metrics_transição_ofensiva_2 = metrics.iloc[:, 1].tolist()
metrics_transição_ofensiva_3 = metrics.iloc[:, 2].tolist()
metrics_y = [0] * len(metrics_transição_ofensiva_1)

# The specific data point you want to highlight
highlight = attribute_chart_z1[(attribute_chart_z1['Atleta']==jogadores) & (attribute_chart_z1['Clube']==equipe)]
highlight = highlight.iloc[:, np.r_[84, 77, 85]].reset_index(drop=True)
highlight_transição_ofensiva_1 = highlight.iloc[:, 0].tolist()
highlight_transição_ofensiva_2 = highlight.iloc[:, 1].tolist()
highlight_transição_ofensiva_3 = highlight.iloc[:, 2].tolist()
highlight_y = 0

# Computing the selected player specific values
highlight_transição_ofensiva_1_value = pd.DataFrame(highlight_transição_ofensiva_1).reset_index(drop=True)
highlight_transição_ofensiva_2_value = pd.DataFrame(highlight_transição_ofensiva_2).reset_index(drop=True)
highlight_transição_ofensiva_3_value = pd.DataFrame(highlight_transição_ofensiva_3).reset_index(drop=True)

highlight_transição_ofensiva_1_value = highlight_transição_ofensiva_1_value.iat[0,0]
highlight_transição_ofensiva_2_value = highlight_transição_ofensiva_2_value.iat[0,0]
highlight_transição_ofensiva_3_value = highlight_transição_ofensiva_3_value.iat[0,0]

# Computing the min and max value across all lists using a generator expression
min_value = min(min(lst) for lst in [metrics_transição_ofensiva_1, metrics_transição_ofensiva_2, 
                                    metrics_transição_ofensiva_3])
min_value = min_value - 0.1
max_value = max(max(lst) for lst in [metrics_transição_ofensiva_1, metrics_transição_ofensiva_2, 
                                    metrics_transição_ofensiva_3])
max_value = max_value + 0.1

# Create two subplots vertically aligned with separate x-axes
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
#ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

# Building the Extended Title"
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['Posição'] == "Primeiro Volante")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[filtered_df['Atleta'] == player_name]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
transição_ofensiva_1_ranking_value = (get_player_rank(jogadores, liga, "Passes de criação de jogadas (90)", attribute_chart_z1))

# Data to plot
output_str = f"({transição_ofensiva_1_ranking_value}/{rows_count})"
full_title_transição_ofensiva_1 = f"Passes de criação de jogadas (90) {output_str} {highlight_transição_ofensiva_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
transição_ofensiva_2_ranking_value = (get_player_rank(jogadores, liga, "xT Passes para último terço (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({transição_ofensiva_2_ranking_value}/{rows_count})"
full_title_transição_ofensiva_2 = f"xT Passes para último terço (p90) {output_str} {highlight_transição_ofensiva_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
transição_ofensiva_3_ranking_value = (get_player_rank(jogadores, liga, "xT Progressão com bola (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({transição_ofensiva_3_ranking_value}/{rows_count})"
full_title_transição_ofensiva_3 = f"xT Progressão com bola (p90) {output_str} {highlight_transição_ofensiva_3_value}"

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

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value):
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
        'Passes de criação de jogadas (90)', 
        'xT Passes para último terço (p90)', 
        'xT Progressão com bola (p90)'
    ]

    # Prepare all the data
    metrics_data = prepare_data(tabela_a, metrics_list)
    
    # Calculate highlight data
    highlight_data = {
        f'highlight_{metric}': tabela_a[tabela_a['Atleta'] == jogadores][metric].iloc[0]
        for metric in metrics_list
    }
    
    # Calculate highlight ranks
    highlight_ranks = {
        metric: int(pd.Series(tabela_a[metric]).rank(ascending=False)[tabela_a['Atleta'] == jogadores].iloc[0])
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
        font=dict(size=16, color='blue')
    )

    return fig

# Calculate min and max values with some padding
min_value_test = min([
min(metrics_transição_ofensiva_1), min(metrics_transição_ofensiva_2), 
min(metrics_transição_ofensiva_3)
])  # Add padding of 0.5

max_value_test = max([
min(metrics_transição_ofensiva_1), min(metrics_transição_ofensiva_2), 
min(metrics_transição_ofensiva_3)
])  # Add padding of 0.5

min_value = -max(abs(min_value_test), max_value_test) -0.03
max_value = -min_value

# Create the plot
fig = create_player_attributes_plot(
    tabela_a=attribute_chart_z1,  # Your main dataframe
    jogadores=jogadores,  # Name of player to highlight
    min_value= min_value,  # Minimum value for x-axis
    max_value= max_value    # Maximum value for x-axis
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&(attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Meio Campo") & (attribute_chart_per['Clube']==equipe)]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[64, 57, 65]].reset_index(drop=True)
percent = attribute_chart_per_1.iloc[:, np.r_[84, 77, 85]].reset_index(drop=True)
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
st.markdown("<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em 2024</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
#Collecting data to plot
metrics = attribute_chart_1.iloc[:, np.r_[3, 64, 57, 65]].reset_index(drop=True)
metrics_mean = attribute_chart_mean.iloc[:, np.r_[64, 57, 65]]
metrics_mean['Passes de criação de jogadas (90)'] = metrics_mean['Passes de criação de jogadas (90)'].mean()
metrics_mean['xT Passes para último terço (p90)'] = metrics_mean['xT Passes para último terço (p90)'].mean()
metrics_mean['xT Progressão com bola (p90)'] = metrics_mean['xT Progressão com bola (p90)'].mean()

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

#################################################################################################################################
#################################################################################################################################
# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Impacto dos Passes</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Meio Campo")]
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
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função']=="Meio Campo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[filtered_df['Atleta'] == player_name]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_1_ranking_value = (get_player_rank(jogadores, liga, "Passes criativos (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({impacto_passe_1_ranking_value}/{rows_count})"
full_title_impacto_passe_1 = f"Passes criativos (p90) {output_str} {highlight_impacto_passe_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_2_ranking_value = (get_player_rank(jogadores, liga, "xT Passes no último terço (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({impacto_passe_2_ranking_value}/{rows_count})"
full_title_impacto_passe_2 = f"xT Passes no último terço (p90) {output_str} {highlight_impacto_passe_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_3_ranking_value = (get_player_rank(jogadores, liga, "xT Passes para último terço (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({impacto_passe_3_ranking_value}/{rows_count})"
full_title_impacto_passe_3 = f"xT Passes para último terço (p90) {output_str} {highlight_impacto_passe_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_4_ranking_value = (get_player_rank(jogadores, liga, "xT Passes (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({impacto_passe_4_ranking_value}/{rows_count})"
full_title_impacto_passe_4 = f"xT Passes (p90) {output_str} {highlight_impacto_passe_4_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
impacto_passe_5_ranking_value = (get_player_rank(jogadores, liga, "xT Cruzamentos (p90)", attribute_chart_z1))

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

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value):
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
    
    # Calculate highlight data
    highlight_data = {
        f'highlight_{metric}': tabela_a[tabela_a['Atleta'] == jogadores][metric].iloc[0]
        for metric in metrics_list
    }
    
    # Calculate highlight ranks
    highlight_ranks = {
        metric: int(pd.Series(tabela_a[metric]).rank(ascending=False)[tabela_a['Atleta'] == jogadores].iloc[0])
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
        font=dict(size=16, color='blue')
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
    max_value= max_value    # Maximum value for x-axis
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&(attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Meio Campo") & (attribute_chart_per['Clube']==equipe)]
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
st.markdown("<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em 2024</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
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

# Use the dynamically created HTML string in st.markdown
st.markdown("<h3 style='text-align: center; color: deepskyblue; '>Criação de Oportunidades</h3>", unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)

attribute_chart_z = pd.read_csv("patch_code_z.csv")
# Collecting data
attribute_chart_z1 = attribute_chart_z[(attribute_chart_z['Liga']==liga) & (attribute_chart_z['Temporada']==temporada) & (attribute_chart_z['função']=="Meio Campo")]
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
rows_count = attribute_chart_z1[(attribute_chart_z1['Liga'] == liga) & (attribute_chart_z1['função']=="Meio Campo")].shape[0]

# Function to determine player's rank in attribute in league
def get_player_rank(player_name, liga, column_name, dataframe):
    # Filter the dataframe for the specified Liga
    filtered_df = dataframe[dataframe['Liga'] == liga]
    
    # Rank players based on the specified column in descending order
    filtered_df['Rank'] = filtered_df[column_name].rank(ascending=False, method='min')
    
    # Find the rank of the specified player
    player_row = filtered_df[filtered_df['Atleta'] == player_name]
    if not player_row.empty:
        return int(player_row['Rank'].iloc[0])
    else:
        return None

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_1_ranking_value = (get_player_rank(jogadores, liga, "xG Criado (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({criação_oportunidades_1_ranking_value}/{rows_count})"
full_title_criação_oportunidades_1 = f"xG Criado (p90) {output_str} {highlight_criação_oportunidades_1_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_2_ranking_value = (get_player_rank(jogadores, liga, "Passes chave (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({criação_oportunidades_2_ranking_value}/{rows_count})"
full_title_criação_oportunidades_2 = f"Passes chave (p90) {output_str} {highlight_criação_oportunidades_2_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_3_ranking_value = (get_player_rank(jogadores, liga, "Deep completions (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({criação_oportunidades_3_ranking_value}/{rows_count})"
full_title_criação_oportunidades_3 = f"Deep completions (p90) {output_str} {highlight_criação_oportunidades_3_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_4_ranking_value = (get_player_rank(jogadores, liga, "xA (p90)", attribute_chart_z1))

# Data to plot
output_str = f"({criação_oportunidades_4_ranking_value}/{rows_count})"
full_title_criação_oportunidades_4 = f"xA (p90) {output_str} {highlight_criação_oportunidades_4_value}"

# Building the Extended Title"
# Determining player's rank in attribute in league
criação_oportunidades_5_ranking_value = (get_player_rank(jogadores, liga, "Assistências (p90)", attribute_chart_z1))

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

def create_player_attributes_plot(tabela_a, jogadores, min_value, max_value):
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
    
    # Calculate highlight data
    highlight_data = {
        f'highlight_{metric}': tabela_a[tabela_a['Atleta'] == jogadores][metric].iloc[0]
        for metric in metrics_list
    }
    
    # Calculate highlight ranks
    highlight_ranks = {
        metric: int(pd.Series(tabela_a[metric]).rank(ascending=False)[tabela_a['Atleta'] == jogadores].iloc[0])
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
        font=dict(size=16, color='blue')
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
    max_value= max_value    # Maximum value for x-axis
)

st.plotly_chart(fig, use_container_width=True)

#################################################################################################################################
#################################################################################################################################

#Plotar Segundo Gráfico - Tabela de Métricas e Percentis do Jogador na liga:
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas do Jogador na Liga em 2024</h3>", unsafe_allow_html=True)
attribute_chart = pd.read_csv("patch_code.csv")
attribute_chart_per = pd.read_csv('patch_code_per.csv')
attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&(attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_per_1 = attribute_chart_per[(attribute_chart_per['Atleta']==jogadores)&(attribute_chart_per['Liga']==liga)&(attribute_chart_per['Temporada']==temporada) & (attribute_chart_per['função']=="Meio Campo") & (attribute_chart_per['Clube']==equipe)]
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
st.markdown("<h3 style='text-align: center; color: blue; '>Comparação com a Média da Liga em 2024</h3>", unsafe_allow_html=True)

attribute_chart_1 = attribute_chart[(attribute_chart['Atleta']==jogadores)&(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo") & (attribute_chart['Clube']==equipe)]
attribute_chart_2 = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
attribute_chart_mean = attribute_chart[(attribute_chart['Liga']==liga)&
                                    (attribute_chart['Temporada']==temporada) & (attribute_chart['função']=="Meio Campo")]
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

