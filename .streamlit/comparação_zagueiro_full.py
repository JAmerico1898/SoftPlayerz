métricas_participação = ['xG gerado na construção (p90)', 'Toques (p90)', 
                        'Ações defensivas (p90)','Disputas aéreas (p90)']

#Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis e Métricas de<br>Participação</h3>", unsafe_allow_html=True)
Participação_Zagueiro_Charts_1 = Zagueiro_Charts_1.copy()

metrics = Participação_Zagueiro_Charts_1.iloc[:, np.r_[3, 72:74, 31, 74]].reset_index(drop=True)
## parameter names
params = list(metrics.columns[1:])

## range values
ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
a_values = []
b_values = []

# Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
for i, atleta in enumerate(metrics['Atleta']):
    if atleta == jogador_1:
        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
    elif atleta == jogador_2:
        b_values = metrics.iloc[i, 1:].tolist()

values = [a_values, b_values]

## title values
title = dict(
    title_name=jogador_1,
    title_color='#B6282F',
    subtitle_name=f"{equipe_1} ({temporada_1})",
    subtitle_color='#B6282F',
    title_name_2=jogador_2,
    title_color_2='#344D94',
    subtitle_name_2=f"{equipe_2} ({temporada_2})",
    subtitle_color_2='#344D94',
    title_fontsize=20,
    subtitle_fontsize=18,
)

## endnote 
endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

## instantiate object
#radar = Radar()

radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig, ax = radar.plot_radar(
    ranges=ranges,
    params=params,
    values=values,
    radar_color=['#B6282F', '#344D94'],
    dpi=600,
    alphas=[.8, .6],
    title=title,
    endnote=endnote,
    compare=True
)
st.pyplot(fig)

######################################################################################################################################
######################################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_1_scores = pd.read_csv('patch_code.csv')
jogador_1_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_1
jogador_1_scores = jogador_1_scores[
((jogador_1_scores['Atleta'] == jogador_1) & (jogador_1_scores['Clube'] == equipe_1) & (jogador_1_scores['Temporada'] == temporada_1))]
jogador_1_scores = jogador_1_scores.iloc[:, np.r_[3, 52:54, 11, 54]].reset_index(drop=True)
jogador_1_scores = jogador_1_scores.round(decimals=2)
jogador_1_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_1
jogador_1_percs = jogador_1_percs[
((jogador_1_percs['Atleta'] == jogador_1) & (jogador_1_percs['Clube'] == equipe_1)  & (jogador_1_percs['Temporada'] == temporada_1))]
jogador_1_percs = jogador_1_percs.iloc[:, np.r_[3, 72:74, 31, 74]].reset_index(drop=True)
jogador_1_percs = jogador_1_percs.round(decimals=0)
jogador_1_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_1 + "_percent"
jogador_1_percs.iloc[0, 0] = jogador_1 + "_percent"

# Create a dictionary of columns to rename by removing the '_percentil' suffix
#columns_to_rename = {
#    col: col.replace('_Percentil', '') for col in jogador_1_percs.columns if '_Percentil' in col
#}            

#Collecting data to plot
#jogador_1_percs.rename(columns=columns_to_rename, inplace=True)
                    
#Concatenating scores and percentiles for jogador 1
jogador_1_scores = pd.concat([jogador_1_scores, jogador_1_percs])
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores = jogador_1_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_1_scores.columns = jogador_1_scores.iloc[0]  # Set the first row as the header
jogador_1_scores = jogador_1_scores.drop(jogador_1_scores.index[0])  # Drop the old header row
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores.insert(0, 'Métricas', métricas_participação)

#################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_2_scores = pd.read_csv('patch_code.csv')
jogador_2_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_2
jogador_2_scores = jogador_2_scores[
((jogador_2_scores['Atleta'] == jogador_2) & (jogador_2_scores['Clube'] == equipe_2) & (jogador_2_scores['Temporada'] == temporada_2))]
jogador_2_scores = jogador_2_scores.iloc[:, np.r_[3, 52:54, 11, 54]].reset_index(drop=True)
jogador_2_scores = jogador_2_scores.round(decimals=2)
jogador_2_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_2
jogador_2_percs = jogador_2_percs[
((jogador_2_percs['Atleta'] == jogador_2) & (jogador_2_percs['Clube'] == equipe_2)  & (jogador_2_percs['Temporada'] == temporada_2))]
jogador_2_percs = jogador_2_percs.iloc[:, np.r_[3, 72:74, 31, 74]].reset_index(drop=True)
jogador_2_percs = jogador_2_percs.round(decimals=0)
jogador_2_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_2 + "_percent"
jogador_2_percs.iloc[0, 0] = jogador_2 + "_percent"

# Create a dictionary of columns to rename by removing the '_percentil' suffix
#columns_to_rename = {
#    col: col.replace('_Percentil', '') for col in jogador_2_percs.columns if '_Percentil' in col
#}            

#Collecting data to plot
#jogador_2_percs.rename(columns=columns_to_rename, inplace=True)
                    
#Concatenating scores and percentiles for jogador 1
jogador_2_scores = pd.concat([jogador_2_scores, jogador_2_percs])
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores = jogador_2_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_2_scores.columns = jogador_2_scores.iloc[0]  # Set the first row as the header
jogador_2_scores = jogador_2_scores.drop(jogador_2_scores.index[0])  # Drop the old header row
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores.insert(0, 'Métricas', métricas_participação)

#################################################################################################################
#################################################################################################################

# Function to apply conditional formatting based on the percentile values
def apply_colormap_based_on_value(val):
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    if pd.isna(val):
        return ''  # No styling for NaN values
    elif val >= 90:
        color = cmap2(0.70)  # "Elite"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 75 <= val < 90:
        color = cmap2(0.50)  # "Destaque"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 60 <= val < 75:
        color = cmap(0.50)  # "Razoável"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 40 <= val < 60:
        color = cmap(0.25)  # "Mediano"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 20 <= val < 40:
        color = cmap1(0.30)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    else:
        color = cmap1(0.50)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
# Function to apply the colormap to a specified column based on the corresponding percentiles column
def apply_colormap_to_column_based_on_percentiles(styler, df, values_col, percentiles_col):
    colormap_styles = [apply_colormap_based_on_value(val) for val in df[percentiles_col]]
    return styler.apply(lambda _: colormap_styles, subset=[values_col])

# Function to merge jogador_1_scores and jogador_2_scores
def merge_scores_tables(jogador_1_scores, jogador_2_scores):
    # Rename the columns for each player
    jogador_1_scores.columns = ['Métricas', jogador_1, 'Player 1 Percentiles']
    jogador_2_scores.columns = ['Métricas', jogador_2, 'Player 2 Percentiles']

    # Merge the two DataFrames on the "Métricas" column
    merged_df = pd.merge(jogador_1_scores[['Métricas', jogador_1, 'Player 1 Percentiles']],
                        jogador_2_scores[['Métricas', jogador_2, 'Player 2 Percentiles']],
                        on='Métricas')

    return merged_df

#################################################################################################################

# Styling function for merged DataFrame
def style_merged_table(merged_df):
    # Create a Styler object from the merged DataFrame
    styled_df = merged_df.style

    # Apply colormap to jogador_1 values based on Player 1 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_1, 'Player 1 Percentiles')

    # Apply colormap to jogador_2 values based on Player 2 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_2, 'Player 2 Percentiles')
    
    # Format both jogador_1 and jogador_2 columns to display 2 decimal places
    styled_df = styled_df.format({jogador_1: "{:.2f}", jogador_2: "{:.2f}"})
    
    # Left-align column[0] ("Métricas") and center columns[1, 2] ("jogador_1" and "jogador_2")
    styled_df = styled_df.set_properties(subset=['Métricas'], **{'text-align': 'left'})
    styled_df = styled_df.set_properties(subset=[jogador_1, jogador_2], **{'text-align': 'center'})

    # Drop both percentile columns from the final display
    styled_df = styled_df.hide(axis='columns', subset=['Player 1 Percentiles', 'Player 2 Percentiles'])

    # Apply table styles as in the LAST CODE
    styled_df = styled_df.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('font-weight', 'bold'),
                    ('border-style', 'solid'),
                    ('border-width', '0px 0px 2px 0px'),
                    ('border-color', 'black')]
        }, {
            'selector': 'thead th:not(:first-child)',
            'props': [('text-align', 'center')]  # Center headers except the first
        }, {
            'selector': 'thead th:last-child',
            'props': [('color', 'black')]  # Make last column header black
        }, {
            'selector': 'td',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'center')]
        }, {
            'selector': 'th',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'left')]
        }, {
            'selector': '.index_name',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of the index
        }, {
            'selector': '.row_heading',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of row headers
        }]
    ).set_properties(**{'padding': '2px', 'font-size': '16px'})

    return styled_df

#################################################################################################################

# Main function to process the data
def main():
    # Assuming jogador_1_scores and jogador_2_scores are already defined with the necessary columns (Métricas, Values, Percentiles)

    # Merge the two tables
    merged_scores = merge_scores_tables(jogador_1_scores, jogador_2_scores)

    # Style the merged table
    styled_merged_scores = style_merged_table(merged_scores)

    # Convert to HTML and display (for Streamlit, you'd use st.markdown)
    merged_html = styled_merged_scores.to_html(escape=False, index=False)
    center_html = f"<div style='margin-left: auto; margin-right: auto; width: fit-content;'>{merged_html}</div>"

    # Output the final table (for Streamlit, you'd use st.markdown)
    st.markdown(center_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()

#################################################################################################################

# Function to plot the legend using the same colors as the apply_colormap_based_on_value function
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

####################################################################################################                            
####################################################################################################                            

métricas_intensidade_defensiva = ['Sucesso em desarmes (%)', 
                                    'Posses recuperadas (p90)', 
                                    'Ações defensivas (p90)',
                                    'Sucesso em 1v1 defensivo (%)'
]

#Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis e Métricas de<br>Intensidade Defensiva</h3>", unsafe_allow_html=True)

Intensidade_Defensiva_Zagueiro_Charts = Zagueiro_Charts_1.copy()

#Collecting data to plot
metrics = Intensidade_Defensiva_Zagueiro_Charts.iloc[:, np.r_[3, 29:33]].reset_index(drop=True)
## parameter names
params = list(metrics.columns[1:])

## range values
ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
a_values = []
b_values = []

# Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
for i, atleta in enumerate(metrics['Atleta']):
    if atleta == jogador_1:
        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
    elif atleta == jogador_2:
        b_values = metrics.iloc[i, 1:].tolist()

values = [a_values, b_values]

## title values
title = dict(
    title_name=jogador_1,
    title_color='#B6282F',
    subtitle_name=f"{equipe_1} ({temporada_1})",
    subtitle_color='#B6282F',
    title_name_2=jogador_2,
    title_color_2='#344D94',
    subtitle_name_2=f"{equipe_2} ({temporada_2})",
    subtitle_color_2='#344D94',
    title_fontsize=20,
    subtitle_fontsize=18,
)

## endnote 
endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

## instantiate object
#radar = Radar()

radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig, ax = radar.plot_radar(
    ranges=ranges,
    params=params,
    values=values,
    radar_color=['#B6282F', '#344D94'],
    dpi=600,
    alphas=[.8, .6],
    title=title,
    endnote=endnote,
    compare=True
)
st.pyplot(fig)

######################################################################################################################################
######################################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_1_scores = pd.read_csv('patch_code.csv')
jogador_1_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_1
jogador_1_scores = jogador_1_scores[
((jogador_1_scores['Atleta'] == jogador_1) & (jogador_1_scores['Clube'] == equipe_1) & (jogador_1_scores['Temporada'] == temporada_1))]
jogador_1_scores = jogador_1_scores.iloc[:, np.r_[3, 9:13]].reset_index(drop=True)
jogador_1_scores = jogador_1_scores.round(decimals=2)
jogador_1_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_1
jogador_1_percs = jogador_1_percs[
((jogador_1_percs['Atleta'] == jogador_1) & (jogador_1_percs['Clube'] == equipe_1)  & (jogador_1_percs['Temporada'] == temporada_1))]
jogador_1_percs = jogador_1_percs.iloc[:, np.r_[3, 29:33]].reset_index(drop=True)
jogador_1_percs = jogador_1_percs.round(decimals=0)
jogador_1_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_1 + "_percent"
jogador_1_percs.iloc[0, 0] = jogador_1 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_1_scores = pd.concat([jogador_1_scores, jogador_1_percs])
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores = jogador_1_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_1_scores.columns = jogador_1_scores.iloc[0]  # Set the first row as the header
jogador_1_scores = jogador_1_scores.drop(jogador_1_scores.index[0])  # Drop the old header row
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores.insert(0, 'Métricas', métricas_intensidade_defensiva)

#################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_2_scores = pd.read_csv('patch_code.csv')
jogador_2_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_2
jogador_2_scores = jogador_2_scores[
((jogador_2_scores['Atleta'] == jogador_2) & (jogador_2_scores['Clube'] == equipe_2) & (jogador_2_scores['Temporada'] == temporada_2))]
jogador_2_scores = jogador_2_scores.iloc[:, np.r_[3, 9:13]].reset_index(drop=True)
jogador_2_scores = jogador_2_scores.round(decimals=2)
jogador_2_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_2
jogador_2_percs = jogador_2_percs[
((jogador_2_percs['Atleta'] == jogador_2) & (jogador_2_percs['Clube'] == equipe_2)  & (jogador_2_percs['Temporada'] == temporada_2))]
jogador_2_percs = jogador_2_percs.iloc[:, np.r_[3, 29:33]].reset_index(drop=True)
jogador_2_percs = jogador_2_percs.round(decimals=0)
jogador_2_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_2 + "_percent"
jogador_2_percs.iloc[0, 0] = jogador_2 + "_percent"

# Create a dictionary of columns to rename by removing the '_percentil' suffix
#columns_to_rename = {
#    col: col.replace('_Percentil', '') for col in jogador_2_percs.columns if '_Percentil' in col
#}            

#Collecting data to plot
#jogador_2_percs.rename(columns=columns_to_rename, inplace=True)
                    
#Concatenating scores and percentiles for jogador 1
jogador_2_scores = pd.concat([jogador_2_scores, jogador_2_percs])
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores = jogador_2_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_2_scores.columns = jogador_2_scores.iloc[0]  # Set the first row as the header
jogador_2_scores = jogador_2_scores.drop(jogador_2_scores.index[0])  # Drop the old header row
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores.insert(0, 'Métricas', métricas_intensidade_defensiva)

#################################################################################################################
#################################################################################################################

# Function to apply conditional formatting based on the percentile values
def apply_colormap_based_on_value(val):
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    if pd.isna(val):
        return ''  # No styling for NaN values
    elif val >= 90:
        color = cmap2(0.70)  # "Elite"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 75 <= val < 90:
        color = cmap2(0.50)  # "Destaque"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 60 <= val < 75:
        color = cmap(0.50)  # "Razoável"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 40 <= val < 60:
        color = cmap(0.25)  # "Mediano"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 20 <= val < 40:
        color = cmap1(0.30)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    else:
        color = cmap1(0.50)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
# Function to apply the colormap to a specified column based on the corresponding percentiles column
def apply_colormap_to_column_based_on_percentiles(styler, df, values_col, percentiles_col):
    colormap_styles = [apply_colormap_based_on_value(val) for val in df[percentiles_col]]
    return styler.apply(lambda _: colormap_styles, subset=[values_col])

# Function to merge jogador_1_scores and jogador_2_scores
def merge_scores_tables(jogador_1_scores, jogador_2_scores):
    # Rename the columns for each player
    jogador_1_scores.columns = ['Métricas', jogador_1, 'Player 1 Percentiles']
    jogador_2_scores.columns = ['Métricas', jogador_2, 'Player 2 Percentiles']

    # Merge the two DataFrames on the "Métricas" column
    merged_df = pd.merge(jogador_1_scores[['Métricas', jogador_1, 'Player 1 Percentiles']],
                        jogador_2_scores[['Métricas', jogador_2, 'Player 2 Percentiles']],
                        on='Métricas')

    return merged_df

#################################################################################################################

# Styling function for merged DataFrame
def style_merged_table(merged_df):
    # Create a Styler object from the merged DataFrame
    styled_df = merged_df.style

    # Apply colormap to jogador_1 values based on Player 1 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_1, 'Player 1 Percentiles')

    # Apply colormap to jogador_2 values based on Player 2 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_2, 'Player 2 Percentiles')
    
    # Format both jogador_1 and jogador_2 columns to display 2 decimal places
    styled_df = styled_df.format({jogador_1: "{:.2f}", jogador_2: "{:.2f}"})
    
    # Left-align column[0] ("Métricas") and center columns[1, 2] ("jogador_1" and "jogador_2")
    styled_df = styled_df.set_properties(subset=['Métricas'], **{'text-align': 'left'})
    styled_df = styled_df.set_properties(subset=[jogador_1, jogador_2], **{'text-align': 'center'})

    # Drop both percentile columns from the final display
    styled_df = styled_df.hide(axis='columns', subset=['Player 1 Percentiles', 'Player 2 Percentiles'])

    # Apply table styles as in the LAST CODE
    styled_df = styled_df.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('font-weight', 'bold'),
                    ('border-style', 'solid'),
                    ('border-width', '0px 0px 2px 0px'),
                    ('border-color', 'black')]
        }, {
            'selector': 'thead th:not(:first-child)',
            'props': [('text-align', 'center')]  # Center headers except the first
        }, {
            'selector': 'thead th:last-child',
            'props': [('color', 'black')]  # Make last column header black
        }, {
            'selector': 'td',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'center')]
        }, {
            'selector': 'th',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'left')]
        }, {
            'selector': '.index_name',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of the index
        }, {
            'selector': '.row_heading',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of row headers
        }]
    ).set_properties(**{'padding': '2px', 'font-size': '16px'})

    return styled_df

#################################################################################################################

# Main function to process the data
def main():
    # Assuming jogador_1_scores and jogador_2_scores are already defined with the necessary columns (Métricas, Values, Percentiles)

    # Merge the two tables
    merged_scores = merge_scores_tables(jogador_1_scores, jogador_2_scores)

    # Style the merged table
    styled_merged_scores = style_merged_table(merged_scores)

    # Convert to HTML and display (for Streamlit, you'd use st.markdown)
    merged_html = styled_merged_scores.to_html(escape=False, index=False)
    center_html = f"<div style='margin-left: auto; margin-right: auto; width: fit-content;'>{merged_html}</div>"

    # Output the final table (for Streamlit, you'd use st.markdown)
    st.markdown(center_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()

#################################################################################################################

# Function to plot the legend using the same colors as the apply_colormap_based_on_value function
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


####################################################################################################

métricas_inteligência_defensiva = ['Interceptações (p90)', 
                                    'Contra-pressão (p90)', 
                                    'Recuperações de bola (p90)'
]

#Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis e Métricas de<br>Inteligência Defensiva</h3>", unsafe_allow_html=True)

Inteligência_Defensiva_Zagueiro_Charts = Zagueiro_Charts_1.copy()

#Collecting data to plot
metrics = Inteligência_Defensiva_Zagueiro_Charts.iloc[:, np.r_[3, 69:72]].reset_index(drop=True)
## parameter names
params = list(metrics.columns[1:])

## range values
ranges = [(0, 100), (0, 100), (0, 100)]
a_values = []
b_values = []

# Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
for i, atleta in enumerate(metrics['Atleta']):
    if atleta == jogador_1:
        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
    elif atleta == jogador_2:
        b_values = metrics.iloc[i, 1:].tolist()

values = [a_values, b_values]

## title values
title = dict(
    title_name=jogador_1,
    title_color='#B6282F',
    subtitle_name=f"{equipe_1} ({temporada_1})",
    subtitle_color='#B6282F',
    title_name_2=jogador_2,
    title_color_2='#344D94',
    subtitle_name_2=f"{equipe_2} ({temporada_2})",
    subtitle_color_2='#344D94',
    title_fontsize=20,
    subtitle_fontsize=18,
)

## endnote 
endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

## instantiate object
#radar = Radar()

radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig, ax = radar.plot_radar(
    ranges=ranges,
    params=params,
    values=values,
    radar_color=['#B6282F', '#344D94'],
    dpi=600,
    alphas=[.8, .6],
    title=title,
    endnote=endnote,
    compare=True
)
st.pyplot(fig)

####################################################################################################
######################################################################################################################################
######################################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_1_scores = pd.read_csv('patch_code.csv')
jogador_1_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_1
jogador_1_scores = jogador_1_scores[
((jogador_1_scores['Atleta'] == jogador_1) & (jogador_1_scores['Clube'] == equipe_1) & (jogador_1_scores['Temporada'] == temporada_1))]
jogador_1_scores = jogador_1_scores.iloc[:, np.r_[3, 49:52]].reset_index(drop=True)
jogador_1_scores = jogador_1_scores.round(decimals=2)
jogador_1_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_1
jogador_1_percs = jogador_1_percs[
((jogador_1_percs['Atleta'] == jogador_1) & (jogador_1_percs['Clube'] == equipe_1)  & (jogador_1_percs['Temporada'] == temporada_1))]
jogador_1_percs = jogador_1_percs.iloc[:, np.r_[3, 69:72]].reset_index(drop=True)
jogador_1_percs = jogador_1_percs.round(decimals=0)
jogador_1_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_1 + "_percent"
jogador_1_percs.iloc[0, 0] = jogador_1 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_1_scores = pd.concat([jogador_1_scores, jogador_1_percs])
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores = jogador_1_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_1_scores.columns = jogador_1_scores.iloc[0]  # Set the first row as the header
jogador_1_scores = jogador_1_scores.drop(jogador_1_scores.index[0])  # Drop the old header row
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores.insert(0, 'Métricas', métricas_inteligência_defensiva)

#################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_2_scores = pd.read_csv('patch_code.csv')
jogador_2_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_2
jogador_2_scores = jogador_2_scores[
((jogador_2_scores['Atleta'] == jogador_2) & (jogador_2_scores['Clube'] == equipe_2) & (jogador_2_scores['Temporada'] == temporada_2))]
jogador_2_scores = jogador_2_scores.iloc[:, np.r_[3, 49:52]].reset_index(drop=True)
jogador_2_scores = jogador_2_scores.round(decimals=2)
jogador_2_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_2
jogador_2_percs = jogador_2_percs[
((jogador_2_percs['Atleta'] == jogador_2) & (jogador_2_percs['Clube'] == equipe_2)  & (jogador_2_percs['Temporada'] == temporada_2))]
jogador_2_percs = jogador_2_percs.iloc[:, np.r_[3, 69:72]].reset_index(drop=True)
jogador_2_percs = jogador_2_percs.round(decimals=0)
jogador_2_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_2 + "_percent"
jogador_2_percs.iloc[0, 0] = jogador_2 + "_percent"

# Create a dictionary of columns to rename by removing the '_percentil' suffix
#columns_to_rename = {
#    col: col.replace('_Percentil', '') for col in jogador_2_percs.columns if '_Percentil' in col
#}            

#Collecting data to plot
#jogador_2_percs.rename(columns=columns_to_rename, inplace=True)
                    
#Concatenating scores and percentiles for jogador 1
jogador_2_scores = pd.concat([jogador_2_scores, jogador_2_percs])
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores = jogador_2_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_2_scores.columns = jogador_2_scores.iloc[0]  # Set the first row as the header
jogador_2_scores = jogador_2_scores.drop(jogador_2_scores.index[0])  # Drop the old header row
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores.insert(0, 'Métricas', métricas_inteligência_defensiva)

#################################################################################################################
#################################################################################################################

# Function to apply conditional formatting based on the percentile values
def apply_colormap_based_on_value(val):
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    if pd.isna(val):
        return ''  # No styling for NaN values
    elif val >= 90:
        color = cmap2(0.70)  # "Elite"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 75 <= val < 90:
        color = cmap2(0.50)  # "Destaque"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 60 <= val < 75:
        color = cmap(0.50)  # "Razoável"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 40 <= val < 60:
        color = cmap(0.25)  # "Mediano"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 20 <= val < 40:
        color = cmap1(0.30)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    else:
        color = cmap1(0.50)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
# Function to apply the colormap to a specified column based on the corresponding percentiles column
def apply_colormap_to_column_based_on_percentiles(styler, df, values_col, percentiles_col):
    colormap_styles = [apply_colormap_based_on_value(val) for val in df[percentiles_col]]
    return styler.apply(lambda _: colormap_styles, subset=[values_col])

# Function to merge jogador_1_scores and jogador_2_scores
def merge_scores_tables(jogador_1_scores, jogador_2_scores):
    # Rename the columns for each player
    jogador_1_scores.columns = ['Métricas', jogador_1, 'Player 1 Percentiles']
    jogador_2_scores.columns = ['Métricas', jogador_2, 'Player 2 Percentiles']

    # Merge the two DataFrames on the "Métricas" column
    merged_df = pd.merge(jogador_1_scores[['Métricas', jogador_1, 'Player 1 Percentiles']],
                        jogador_2_scores[['Métricas', jogador_2, 'Player 2 Percentiles']],
                        on='Métricas')

    return merged_df

#################################################################################################################

# Styling function for merged DataFrame
def style_merged_table(merged_df):
    # Create a Styler object from the merged DataFrame
    styled_df = merged_df.style

    # Apply colormap to jogador_1 values based on Player 1 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_1, 'Player 1 Percentiles')

    # Apply colormap to jogador_2 values based on Player 2 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_2, 'Player 2 Percentiles')
    
    # Format both jogador_1 and jogador_2 columns to display 2 decimal places
    styled_df = styled_df.format({jogador_1: "{:.2f}", jogador_2: "{:.2f}"})
    
    # Left-align column[0] ("Métricas") and center columns[1, 2] ("jogador_1" and "jogador_2")
    styled_df = styled_df.set_properties(subset=['Métricas'], **{'text-align': 'left'})
    styled_df = styled_df.set_properties(subset=[jogador_1, jogador_2], **{'text-align': 'center'})

    # Drop both percentile columns from the final display
    styled_df = styled_df.hide(axis='columns', subset=['Player 1 Percentiles', 'Player 2 Percentiles'])

    # Apply table styles as in the LAST CODE
    styled_df = styled_df.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('font-weight', 'bold'),
                    ('border-style', 'solid'),
                    ('border-width', '0px 0px 2px 0px'),
                    ('border-color', 'black')]
        }, {
            'selector': 'thead th:not(:first-child)',
            'props': [('text-align', 'center')]  # Center headers except the first
        }, {
            'selector': 'thead th:last-child',
            'props': [('color', 'black')]  # Make last column header black
        }, {
            'selector': 'td',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'center')]
        }, {
            'selector': 'th',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'left')]
        }, {
            'selector': '.index_name',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of the index
        }, {
            'selector': '.row_heading',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of row headers
        }]
    ).set_properties(**{'padding': '2px', 'font-size': '16px'})

    return styled_df

#################################################################################################################

# Main function to process the data
def main():
    # Assuming jogador_1_scores and jogador_2_scores are already defined with the necessary columns (Métricas, Values, Percentiles)

    # Merge the two tables
    merged_scores = merge_scores_tables(jogador_1_scores, jogador_2_scores)

    # Style the merged table
    styled_merged_scores = style_merged_table(merged_scores)

    # Convert to HTML and display (for Streamlit, you'd use st.markdown)
    merged_html = styled_merged_scores.to_html(escape=False, index=False)
    center_html = f"<div style='margin-left: auto; margin-right: auto; width: fit-content;'>{merged_html}</div>"

    # Output the final table (for Streamlit, you'd use st.markdown)
    st.markdown(center_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()

#################################################################################################################

# Function to plot the legend using the same colors as the apply_colormap_based_on_value function
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


####################################################################################################

métricas_controle_espaço = [
        'Passes adversários bem-sucedidos na área defensiva (%)', 
        'Área defensiva (m²)',
        'Altura da linha defensiva (m)'
        ]

#Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis e Métricas de<br>Controle de espaço</h3>", unsafe_allow_html=True)

Controle_Espaço_Zagueiro_Charts = Zagueiro_Charts_1.copy()

#Collecting data to plot
metrics = Controle_Espaço_Zagueiro_Charts.iloc[:, np.r_[3, 94, 96:98]].reset_index(drop=True)

## parameter names
params = list(metrics.columns[1:])

## range values
ranges = [(0, 100), (0, 100), (0, 100)]
a_values = []
b_values = []

# Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
for i, atleta in enumerate(metrics['Atleta']):
    if atleta == jogador_1:
        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
    elif atleta == jogador_2:
        b_values = metrics.iloc[i, 1:].tolist()

values = [a_values, b_values]

## title values
title = dict(
    title_name=jogador_1,
    title_color='#B6282F',
    subtitle_name=f"{equipe_1} ({temporada_1})",
    subtitle_color='#B6282F',
    title_name_2=jogador_2,
    title_color_2='#344D94',
    subtitle_name_2=f"{equipe_2} ({temporada_2})",
    subtitle_color_2='#344D94',
    title_fontsize=20,
    subtitle_fontsize=18,
)

## endnote 
endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

## instantiate object
#radar = Radar()

radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig, ax = radar.plot_radar(
    ranges=ranges,
    params=params,
    values=values,
    radar_color=['#B6282F', '#344D94'],
    dpi=600,
    alphas=[.8, .6],
    title=title,
    endnote=endnote,
    compare=True
)
st.pyplot(fig)

####################################################################################################
######################################################################################################################################
######################################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_1_scores = pd.read_csv('patch_code.csv')
jogador_1_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_1
jogador_1_scores = jogador_1_scores[
((jogador_1_scores['Atleta'] == jogador_1) & (jogador_1_scores['Clube'] == equipe_1) & (jogador_1_scores['Temporada'] == temporada_1))]
jogador_1_scores = jogador_1_scores.iloc[:, np.r_[3, 74, 76:78]].reset_index(drop=True)
jogador_1_scores = jogador_1_scores.round(decimals=2)
jogador_1_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_1
jogador_1_percs = jogador_1_percs[
((jogador_1_percs['Atleta'] == jogador_1) & (jogador_1_percs['Clube'] == equipe_1)  & (jogador_1_percs['Temporada'] == temporada_1))]
jogador_1_percs = jogador_1_percs.iloc[:, np.r_[3, 94, 96:98]].reset_index(drop=True)
jogador_1_percs = jogador_1_percs.round(decimals=0)
jogador_1_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_1 + "_percent"
jogador_1_percs.iloc[0, 0] = jogador_1 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_1_scores = pd.concat([jogador_1_scores, jogador_1_percs])
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores = jogador_1_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_1_scores.columns = jogador_1_scores.iloc[0]  # Set the first row as the header
jogador_1_scores = jogador_1_scores.drop(jogador_1_scores.index[0])  # Drop the old header row
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores.insert(0, 'Métricas', métricas_controle_espaço)

#################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_2_scores = pd.read_csv('patch_code.csv')
jogador_2_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_2
jogador_2_scores = jogador_2_scores[
((jogador_2_scores['Atleta'] == jogador_2) & (jogador_2_scores['Clube'] == equipe_2) & (jogador_2_scores['Temporada'] == temporada_2))]
jogador_2_scores = jogador_2_scores.iloc[:, np.r_[3, 74, 76:78]].reset_index(drop=True)
jogador_2_scores = jogador_2_scores.round(decimals=2)
jogador_2_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_2
jogador_2_percs = jogador_2_percs[
((jogador_2_percs['Atleta'] == jogador_2) & (jogador_2_percs['Clube'] == equipe_2)  & (jogador_2_percs['Temporada'] == temporada_2))]
jogador_2_percs = jogador_2_percs.iloc[:, np.r_[3, 94, 96:98]].reset_index(drop=True)
jogador_2_percs = jogador_2_percs.round(decimals=0)
jogador_2_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_2 + "_percent"
jogador_2_percs.iloc[0, 0] = jogador_2 + "_percent"

# Create a dictionary of columns to rename by removing the '_percentil' suffix
#columns_to_rename = {
#    col: col.replace('_Percentil', '') for col in jogador_2_percs.columns if '_Percentil' in col
#}            

#Collecting data to plot
#jogador_2_percs.rename(columns=columns_to_rename, inplace=True)
                    
#Concatenating scores and percentiles for jogador 1
jogador_2_scores = pd.concat([jogador_2_scores, jogador_2_percs])
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores = jogador_2_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_2_scores.columns = jogador_2_scores.iloc[0]  # Set the first row as the header
jogador_2_scores = jogador_2_scores.drop(jogador_2_scores.index[0])  # Drop the old header row
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores.insert(0, 'Métricas', métricas_controle_espaço)

#################################################################################################################
#################################################################################################################

# Function to apply conditional formatting based on the percentile values
def apply_colormap_based_on_value(val):
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    if pd.isna(val):
        return ''  # No styling for NaN values
    elif val >= 90:
        color = cmap2(0.70)  # "Elite"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 75 <= val < 90:
        color = cmap2(0.50)  # "Destaque"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 60 <= val < 75:
        color = cmap(0.50)  # "Razoável"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 40 <= val < 60:
        color = cmap(0.25)  # "Mediano"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 20 <= val < 40:
        color = cmap1(0.30)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    else:
        color = cmap1(0.50)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
# Function to apply the colormap to a specified column based on the corresponding percentiles column
def apply_colormap_to_column_based_on_percentiles(styler, df, values_col, percentiles_col):
    colormap_styles = [apply_colormap_based_on_value(val) for val in df[percentiles_col]]
    return styler.apply(lambda _: colormap_styles, subset=[values_col])

# Function to merge jogador_1_scores and jogador_2_scores
def merge_scores_tables(jogador_1_scores, jogador_2_scores):
    # Rename the columns for each player
    jogador_1_scores.columns = ['Métricas', jogador_1, 'Player 1 Percentiles']
    jogador_2_scores.columns = ['Métricas', jogador_2, 'Player 2 Percentiles']

    # Merge the two DataFrames on the "Métricas" column
    merged_df = pd.merge(jogador_1_scores[['Métricas', jogador_1, 'Player 1 Percentiles']],
                        jogador_2_scores[['Métricas', jogador_2, 'Player 2 Percentiles']],
                        on='Métricas')

    return merged_df

#################################################################################################################

# Styling function for merged DataFrame
def style_merged_table(merged_df):
    # Create a Styler object from the merged DataFrame
    styled_df = merged_df.style

    # Apply colormap to jogador_1 values based on Player 1 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_1, 'Player 1 Percentiles')

    # Apply colormap to jogador_2 values based on Player 2 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_2, 'Player 2 Percentiles')
    
    # Format both jogador_1 and jogador_2 columns to display 2 decimal places
    styled_df = styled_df.format({jogador_1: "{:.2f}", jogador_2: "{:.2f}"})
    
    # Left-align column[0] ("Métricas") and center columns[1, 2] ("jogador_1" and "jogador_2")
    styled_df = styled_df.set_properties(subset=['Métricas'], **{'text-align': 'left'})
    styled_df = styled_df.set_properties(subset=[jogador_1, jogador_2], **{'text-align': 'center'})

    # Drop both percentile columns from the final display
    styled_df = styled_df.hide(axis='columns', subset=['Player 1 Percentiles', 'Player 2 Percentiles'])

    # Apply table styles as in the LAST CODE
    styled_df = styled_df.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('font-weight', 'bold'),
                    ('border-style', 'solid'),
                    ('border-width', '0px 0px 2px 0px'),
                    ('border-color', 'black')]
        }, {
            'selector': 'thead th:not(:first-child)',
            'props': [('text-align', 'center')]  # Center headers except the first
        }, {
            'selector': 'thead th:last-child',
            'props': [('color', 'black')]  # Make last column header black
        }, {
            'selector': 'td',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'center')]
        }, {
            'selector': 'th',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'left')]
        }, {
            'selector': '.index_name',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of the index
        }, {
            'selector': '.row_heading',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of row headers
        }]
    ).set_properties(**{'padding': '2px', 'font-size': '16px'})

    return styled_df

#################################################################################################################

# Main function to process the data
def main():
    # Assuming jogador_1_scores and jogador_2_scores are already defined with the necessary columns (Métricas, Values, Percentiles)

    # Merge the two tables
    merged_scores = merge_scores_tables(jogador_1_scores, jogador_2_scores)

    # Style the merged table
    styled_merged_scores = style_merged_table(merged_scores)

    # Convert to HTML and display (for Streamlit, you'd use st.markdown)
    merged_html = styled_merged_scores.to_html(escape=False, index=False)
    center_html = f"<div style='margin-left: auto; margin-right: auto; width: fit-content;'>{merged_html}</div>"

    # Output the final table (for Streamlit, you'd use st.markdown)
    st.markdown(center_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()

#################################################################################################################

# Function to plot the legend using the same colors as the apply_colormap_based_on_value function
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


####################################################################################################

métricas_controle_defensivo = ['Passes progressivos do adversário na área defensiva (%)',
                'xT do adversário na área defensiva (p100 passes)', 
                'xG do adversário na área defensiva (p100 posses)',
                'xG do adversário após ação defensiva (p100 posses)'
]

#Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis e Métricas de<br>Controle Defensivo</h3>", unsafe_allow_html=True)

Controle_Defensivo_Zagueiro_Charts = Zagueiro_Charts_1.copy()

#Collecting data to plot
metrics = Controle_Defensivo_Zagueiro_Charts.iloc[:, np.r_[3, 43:47]].reset_index(drop=True)

## parameter names
params = list(metrics.columns[1:])

## range values
ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
a_values = []
b_values = []

# Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
for i, atleta in enumerate(metrics['Atleta']):
    if atleta == jogador_1:
        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
    elif atleta == jogador_2:
        b_values = metrics.iloc[i, 1:].tolist()

values = [a_values, b_values]

## title values
title = dict(
    title_name=jogador_1,
    title_color='#B6282F',
    subtitle_name=f"{equipe_1} ({temporada_1})",
    subtitle_color='#B6282F',
    title_name_2=jogador_2,
    title_color_2='#344D94',
    subtitle_name_2=f"{equipe_2} ({temporada_2})",
    subtitle_color_2='#344D94',
    title_fontsize=20,
    subtitle_fontsize=18,
)

## endnote 
endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

## instantiate object
#radar = Radar()

radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig, ax = radar.plot_radar(
    ranges=ranges,
    params=params,
    values=values,
    radar_color=['#B6282F', '#344D94'],
    dpi=600,
    alphas=[.8, .6],
    title=title,
    endnote=endnote,
    compare=True
)
st.pyplot(fig)

####################################################################################################
######################################################################################################################################
######################################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_1_scores = pd.read_csv('patch_code.csv')
jogador_1_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_1
jogador_1_scores = jogador_1_scores[
((jogador_1_scores['Atleta'] == jogador_1) & (jogador_1_scores['Clube'] == equipe_1) & (jogador_1_scores['Temporada'] == temporada_1))]
jogador_1_scores = jogador_1_scores.iloc[:, np.r_[3, 23:27]].reset_index(drop=True)
jogador_1_scores = jogador_1_scores.round(decimals=2)
jogador_1_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_1
jogador_1_percs = jogador_1_percs[
((jogador_1_percs['Atleta'] == jogador_1) & (jogador_1_percs['Clube'] == equipe_1)  & (jogador_1_percs['Temporada'] == temporada_1))]
jogador_1_percs = jogador_1_percs.iloc[:, np.r_[3, 43:47]].reset_index(drop=True)
jogador_1_percs = jogador_1_percs.round(decimals=0)
jogador_1_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_1 + "_percent"
jogador_1_percs.iloc[0, 0] = jogador_1 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_1_scores = pd.concat([jogador_1_scores, jogador_1_percs])
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores = jogador_1_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_1_scores.columns = jogador_1_scores.iloc[0]  # Set the first row as the header
jogador_1_scores = jogador_1_scores.drop(jogador_1_scores.index[0])  # Drop the old header row
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores.insert(0, 'Métricas', métricas_controle_defensivo)

#################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_2_scores = pd.read_csv('patch_code.csv')
jogador_2_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_2
jogador_2_scores = jogador_2_scores[
((jogador_2_scores['Atleta'] == jogador_2) & (jogador_2_scores['Clube'] == equipe_2) & (jogador_2_scores['Temporada'] == temporada_2))]
jogador_2_scores = jogador_2_scores.iloc[:, np.r_[3, 23:27]].reset_index(drop=True)
jogador_2_scores = jogador_2_scores.round(decimals=2)
jogador_2_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_2
jogador_2_percs = jogador_2_percs[
((jogador_2_percs['Atleta'] == jogador_2) & (jogador_2_percs['Clube'] == equipe_2)  & (jogador_2_percs['Temporada'] == temporada_2))]
jogador_2_percs = jogador_2_percs.iloc[:, np.r_[3, 43:47]].reset_index(drop=True)
jogador_2_percs = jogador_2_percs.round(decimals=0)
jogador_2_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_2 + "_percent"
jogador_2_percs.iloc[0, 0] = jogador_2 + "_percent"

# Create a dictionary of columns to rename by removing the '_percentil' suffix
#columns_to_rename = {
#    col: col.replace('_Percentil', '') for col in jogador_2_percs.columns if '_Percentil' in col
#}            

#Collecting data to plot
#jogador_2_percs.rename(columns=columns_to_rename, inplace=True)
                    
#Concatenating scores and percentiles for jogador 1
jogador_2_scores = pd.concat([jogador_2_scores, jogador_2_percs])
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores = jogador_2_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_2_scores.columns = jogador_2_scores.iloc[0]  # Set the first row as the header
jogador_2_scores = jogador_2_scores.drop(jogador_2_scores.index[0])  # Drop the old header row
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores.insert(0, 'Métricas', métricas_controle_defensivo)

#################################################################################################################
#################################################################################################################

# Function to apply conditional formatting based on the percentile values
def apply_colormap_based_on_value(val):
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    if pd.isna(val):
        return ''  # No styling for NaN values
    elif val >= 90:
        color = cmap2(0.70)  # "Elite"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 75 <= val < 90:
        color = cmap2(0.50)  # "Destaque"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 60 <= val < 75:
        color = cmap(0.50)  # "Razoável"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 40 <= val < 60:
        color = cmap(0.25)  # "Mediano"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 20 <= val < 40:
        color = cmap1(0.30)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    else:
        color = cmap1(0.50)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
# Function to apply the colormap to a specified column based on the corresponding percentiles column
def apply_colormap_to_column_based_on_percentiles(styler, df, values_col, percentiles_col):
    colormap_styles = [apply_colormap_based_on_value(val) for val in df[percentiles_col]]
    return styler.apply(lambda _: colormap_styles, subset=[values_col])

# Function to merge jogador_1_scores and jogador_2_scores
def merge_scores_tables(jogador_1_scores, jogador_2_scores):
    # Rename the columns for each player
    jogador_1_scores.columns = ['Métricas', jogador_1, 'Player 1 Percentiles']
    jogador_2_scores.columns = ['Métricas', jogador_2, 'Player 2 Percentiles']

    # Merge the two DataFrames on the "Métricas" column
    merged_df = pd.merge(jogador_1_scores[['Métricas', jogador_1, 'Player 1 Percentiles']],
                        jogador_2_scores[['Métricas', jogador_2, 'Player 2 Percentiles']],
                        on='Métricas')

    return merged_df

#################################################################################################################

# Styling function for merged DataFrame
def style_merged_table(merged_df):
    # Create a Styler object from the merged DataFrame
    styled_df = merged_df.style

    # Apply colormap to jogador_1 values based on Player 1 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_1, 'Player 1 Percentiles')

    # Apply colormap to jogador_2 values based on Player 2 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_2, 'Player 2 Percentiles')
    
    # Format both jogador_1 and jogador_2 columns to display 2 decimal places
    styled_df = styled_df.format({jogador_1: "{:.2f}", jogador_2: "{:.2f}"})
    
    # Left-align column[0] ("Métricas") and center columns[1, 2] ("jogador_1" and "jogador_2")
    styled_df = styled_df.set_properties(subset=['Métricas'], **{'text-align': 'left'})
    styled_df = styled_df.set_properties(subset=[jogador_1, jogador_2], **{'text-align': 'center'})

    # Drop both percentile columns from the final display
    styled_df = styled_df.hide(axis='columns', subset=['Player 1 Percentiles', 'Player 2 Percentiles'])

    # Apply table styles as in the LAST CODE
    styled_df = styled_df.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('font-weight', 'bold'),
                    ('border-style', 'solid'),
                    ('border-width', '0px 0px 2px 0px'),
                    ('border-color', 'black')]
        }, {
            'selector': 'thead th:not(:first-child)',
            'props': [('text-align', 'center')]  # Center headers except the first
        }, {
            'selector': 'thead th:last-child',
            'props': [('color', 'black')]  # Make last column header black
        }, {
            'selector': 'td',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'center')]
        }, {
            'selector': 'th',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'left')]
        }, {
            'selector': '.index_name',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of the index
        }, {
            'selector': '.row_heading',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of row headers
        }]
    ).set_properties(**{'padding': '2px', 'font-size': '16px'})

    return styled_df

#################################################################################################################

# Main function to process the data
def main():
    # Assuming jogador_1_scores and jogador_2_scores are already defined with the necessary columns (Métricas, Values, Percentiles)

    # Merge the two tables
    merged_scores = merge_scores_tables(jogador_1_scores, jogador_2_scores)

    # Style the merged table
    styled_merged_scores = style_merged_table(merged_scores)

    # Convert to HTML and display (for Streamlit, you'd use st.markdown)
    merged_html = styled_merged_scores.to_html(escape=False, index=False)
    center_html = f"<div style='margin-left: auto; margin-right: auto; width: fit-content;'>{merged_html}</div>"

    # Output the final table (for Streamlit, you'd use st.markdown)
    st.markdown(center_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()

#################################################################################################################

# Function to plot the legend using the same colors as the apply_colormap_based_on_value function
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

##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################

metrics_bola_aérea_defensiva = ['Duelos aéreos defensivos vencidos (%)', 
                                'Duelos aéreos defensivos vencidos (p90)',
                                'Duelos aéreos vencidos (%)',
                                'Duelos aéreos vencidos (p90)'
]

#Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis e Métricas de<br>Bola Aérea Defensiva</h3>", unsafe_allow_html=True)

Bola_Aérea_Defensiva_Zagueiro_Charts = Zagueiro_Charts_1.copy()

#Collecting data to plot
metrics = Bola_Aérea_Defensiva_Zagueiro_Charts.iloc[:, np.r_[3, 52:54, 36:38]].reset_index(drop=True)
## parameter names
params = list(metrics.columns[1:])

## range values
ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
a_values = []
b_values = []

# Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
for i, atleta in enumerate(metrics['Atleta']):
    if atleta == jogador_1:
        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
    elif atleta == jogador_2:
        b_values = metrics.iloc[i, 1:].tolist()

values = [a_values, b_values]

## title values
title = dict(
    title_name=jogador_1,
    title_color='#B6282F',
    subtitle_name=f"{equipe_1} ({temporada_1})",
    subtitle_color='#B6282F',
    title_name_2=jogador_2,
    title_color_2='#344D94',
    subtitle_name_2=f"{equipe_2} ({temporada_2})",
    subtitle_color_2='#344D94',
    title_fontsize=20,
    subtitle_fontsize=18,
)

## endnote 
endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

## instantiate object
#radar = Radar()

radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig, ax = radar.plot_radar(
    ranges=ranges,
    params=params,
    values=values,
    radar_color=['#B6282F', '#344D94'],
    dpi=600,
    alphas=[.8, .6],
    title=title,
    endnote=endnote,
    compare=True
)
st.pyplot(fig)

####################################################################################################
######################################################################################################################################
######################################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_1_scores = pd.read_csv('patch_code.csv')
jogador_1_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_1
jogador_1_scores = jogador_1_scores[
((jogador_1_scores['Atleta'] == jogador_1) & (jogador_1_scores['Clube'] == equipe_1) & (jogador_1_scores['Temporada'] == temporada_1))]
jogador_1_scores = jogador_1_scores.iloc[:, np.r_[3, 32:34, 16:18]].reset_index(drop=True)
jogador_1_scores = jogador_1_scores.round(decimals=2)
jogador_1_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_1
jogador_1_percs = jogador_1_percs[
((jogador_1_percs['Atleta'] == jogador_1) & (jogador_1_percs['Clube'] == equipe_1)  & (jogador_1_percs['Temporada'] == temporada_1))]
jogador_1_percs = jogador_1_percs.iloc[:, np.r_[3, 52:54, 36:38]].reset_index(drop=True)
jogador_1_percs = jogador_1_percs.round(decimals=0)
jogador_1_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_1 + "_percent"
jogador_1_percs.iloc[0, 0] = jogador_1 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_1_scores = pd.concat([jogador_1_scores, jogador_1_percs])
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores = jogador_1_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_1_scores.columns = jogador_1_scores.iloc[0]  # Set the first row as the header
jogador_1_scores = jogador_1_scores.drop(jogador_1_scores.index[0])  # Drop the old header row
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores.insert(0, 'Métricas', metrics_bola_aérea_defensiva)

#################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_2_scores = pd.read_csv('patch_code.csv')
jogador_2_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_2
jogador_2_scores = jogador_2_scores[
((jogador_2_scores['Atleta'] == jogador_2) & (jogador_2_scores['Clube'] == equipe_2) & (jogador_2_scores['Temporada'] == temporada_2))]
jogador_2_scores = jogador_2_scores.iloc[:, np.r_[3, 32:34, 16:18]].reset_index(drop=True)
jogador_2_scores = jogador_2_scores.round(decimals=2)
jogador_2_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_2
jogador_2_percs = jogador_2_percs[
((jogador_2_percs['Atleta'] == jogador_2) & (jogador_2_percs['Clube'] == equipe_2)  & (jogador_2_percs['Temporada'] == temporada_2))]
jogador_2_percs = jogador_2_percs.iloc[:, np.r_[3, 52:54, 36:38]].reset_index(drop=True)
jogador_2_percs = jogador_2_percs.round(decimals=0)
jogador_2_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_2 + "_percent"
jogador_2_percs.iloc[0, 0] = jogador_2 + "_percent"

# Create a dictionary of columns to rename by removing the '_percentil' suffix
#columns_to_rename = {
#    col: col.replace('_Percentil', '') for col in jogador_2_percs.columns if '_Percentil' in col
#}            

#Collecting data to plot
#jogador_2_percs.rename(columns=columns_to_rename, inplace=True)
                    
#Concatenating scores and percentiles for jogador 1
jogador_2_scores = pd.concat([jogador_2_scores, jogador_2_percs])
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores = jogador_2_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_2_scores.columns = jogador_2_scores.iloc[0]  # Set the first row as the header
jogador_2_scores = jogador_2_scores.drop(jogador_2_scores.index[0])  # Drop the old header row
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores.insert(0, 'Métricas', metrics_bola_aérea_defensiva)

#################################################################################################################
#################################################################################################################

# Function to apply conditional formatting based on the percentile values
def apply_colormap_based_on_value(val):
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    if pd.isna(val):
        return ''  # No styling for NaN values
    elif val >= 90:
        color = cmap2(0.70)  # "Elite"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 75 <= val < 90:
        color = cmap2(0.50)  # "Destaque"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 60 <= val < 75:
        color = cmap(0.50)  # "Razoável"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 40 <= val < 60:
        color = cmap(0.25)  # "Mediano"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 20 <= val < 40:
        color = cmap1(0.30)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    else:
        color = cmap1(0.50)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
# Function to apply the colormap to a specified column based on the corresponding percentiles column
def apply_colormap_to_column_based_on_percentiles(styler, df, values_col, percentiles_col):
    colormap_styles = [apply_colormap_based_on_value(val) for val in df[percentiles_col]]
    return styler.apply(lambda _: colormap_styles, subset=[values_col])

# Function to merge jogador_1_scores and jogador_2_scores
def merge_scores_tables(jogador_1_scores, jogador_2_scores):
    # Rename the columns for each player
    jogador_1_scores.columns = ['Métricas', jogador_1, 'Player 1 Percentiles']
    jogador_2_scores.columns = ['Métricas', jogador_2, 'Player 2 Percentiles']

    # Merge the two DataFrames on the "Métricas" column
    merged_df = pd.merge(jogador_1_scores[['Métricas', jogador_1, 'Player 1 Percentiles']],
                        jogador_2_scores[['Métricas', jogador_2, 'Player 2 Percentiles']],
                        on='Métricas')

    return merged_df

#################################################################################################################

# Styling function for merged DataFrame
def style_merged_table(merged_df):
    # Create a Styler object from the merged DataFrame
    styled_df = merged_df.style

    # Apply colormap to jogador_1 values based on Player 1 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_1, 'Player 1 Percentiles')

    # Apply colormap to jogador_2 values based on Player 2 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_2, 'Player 2 Percentiles')
    
    # Format both jogador_1 and jogador_2 columns to display 2 decimal places
    styled_df = styled_df.format({jogador_1: "{:.2f}", jogador_2: "{:.2f}"})
    
    # Left-align column[0] ("Métricas") and center columns[1, 2] ("jogador_1" and "jogador_2")
    styled_df = styled_df.set_properties(subset=['Métricas'], **{'text-align': 'left'})
    styled_df = styled_df.set_properties(subset=[jogador_1, jogador_2], **{'text-align': 'center'})

    # Drop both percentile columns from the final display
    styled_df = styled_df.hide(axis='columns', subset=['Player 1 Percentiles', 'Player 2 Percentiles'])

    # Apply table styles as in the LAST CODE
    styled_df = styled_df.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('font-weight', 'bold'),
                    ('border-style', 'solid'),
                    ('border-width', '0px 0px 2px 0px'),
                    ('border-color', 'black')]
        }, {
            'selector': 'thead th:not(:first-child)',
            'props': [('text-align', 'center')]  # Center headers except the first
        }, {
            'selector': 'thead th:last-child',
            'props': [('color', 'black')]  # Make last column header black
        }, {
            'selector': 'td',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'center')]
        }, {
            'selector': 'th',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'left')]
        }, {
            'selector': '.index_name',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of the index
        }, {
            'selector': '.row_heading',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of row headers
        }]
    ).set_properties(**{'padding': '2px', 'font-size': '16px'})

    return styled_df

#################################################################################################################

# Main function to process the data
def main():
    # Assuming jogador_1_scores and jogador_2_scores are already defined with the necessary columns (Métricas, Values, Percentiles)

    # Merge the two tables
    merged_scores = merge_scores_tables(jogador_1_scores, jogador_2_scores)

    # Style the merged table
    styled_merged_scores = style_merged_table(merged_scores)

    # Convert to HTML and display (for Streamlit, you'd use st.markdown)
    merged_html = styled_merged_scores.to_html(escape=False, index=False)
    center_html = f"<div style='margin-left: auto; margin-right: auto; width: fit-content;'>{merged_html}</div>"

    # Output the final table (for Streamlit, you'd use st.markdown)
    st.markdown(center_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()

#################################################################################################################

# Function to plot the legend using the same colors as the apply_colormap_based_on_value function
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

##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################

métricas_resistência_pressão = ['Retenção de posse sob pressão (p90)', 
                                'Resistência à pressão (%)', 
                                'Perdas de posse (p90)',
                                'Perdas de posse na linha baixa (p90)', 
                                'Erros (p100 passes)'
]

#Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis e Métricas de<br>Resistência à Pressão</h3>", unsafe_allow_html=True)

Resistência_Pressão_Zagueiro_Charts = Zagueiro_Charts_1.copy()

#Collecting data to plot
metrics = Resistência_Pressão_Zagueiro_Charts.iloc[:, np.r_[3, 47:52]].reset_index(drop=True)
## parameter names
params = list(metrics.columns[1:])

## range values
ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
a_values = []
b_values = []

# Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
for i, atleta in enumerate(metrics['Atleta']):
    if atleta == jogador_1:
        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
    elif atleta == jogador_2:
        b_values = metrics.iloc[i, 1:].tolist()

values = [a_values, b_values]

## title values
title = dict(
    title_name=jogador_1,
    title_color='#B6282F',
    subtitle_name=f"{equipe_1} ({temporada_1})",
    subtitle_color='#B6282F',
    title_name_2=jogador_2,
    title_color_2='#344D94',
    subtitle_name_2=f"{equipe_2} ({temporada_2})",
    subtitle_color_2='#344D94',
    title_fontsize=20,
    subtitle_fontsize=18,
)

## endnote 
endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

## instantiate object
#radar = Radar()

radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig, ax = radar.plot_radar(
    ranges=ranges,
    params=params,
    values=values,
    radar_color=['#B6282F', '#344D94'],
    dpi=600,
    alphas=[.8, .6],
    title=title,
    endnote=endnote,
    compare=True
)
st.pyplot(fig)

####################################################################################################
######################################################################################################################################
######################################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_1_scores = pd.read_csv('patch_code.csv')
jogador_1_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_1
jogador_1_scores = jogador_1_scores[
((jogador_1_scores['Atleta'] == jogador_1) & (jogador_1_scores['Clube'] == equipe_1) & (jogador_1_scores['Temporada'] == temporada_1))]
jogador_1_scores = jogador_1_scores.iloc[:, np.r_[3, 27:32]].reset_index(drop=True)
jogador_1_scores = jogador_1_scores.round(decimals=2)
jogador_1_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_1
jogador_1_percs = jogador_1_percs[
((jogador_1_percs['Atleta'] == jogador_1) & (jogador_1_percs['Clube'] == equipe_1)  & (jogador_1_percs['Temporada'] == temporada_1))]
jogador_1_percs = jogador_1_percs.iloc[:, np.r_[3, 47:52]].reset_index(drop=True)
jogador_1_percs = jogador_1_percs.round(decimals=0)
jogador_1_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_1 + "_percent"
jogador_1_percs.iloc[0, 0] = jogador_1 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_1_scores = pd.concat([jogador_1_scores, jogador_1_percs])
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores = jogador_1_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_1_scores.columns = jogador_1_scores.iloc[0]  # Set the first row as the header
jogador_1_scores = jogador_1_scores.drop(jogador_1_scores.index[0])  # Drop the old header row
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores.insert(0, 'Métricas', métricas_resistência_pressão)

#################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_2_scores = pd.read_csv('patch_code.csv')
jogador_2_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_2
jogador_2_scores = jogador_2_scores[
((jogador_2_scores['Atleta'] == jogador_2) & (jogador_2_scores['Clube'] == equipe_2) & (jogador_2_scores['Temporada'] == temporada_2))]
jogador_2_scores = jogador_2_scores.iloc[:, np.r_[3, 27:32]].reset_index(drop=True)
jogador_2_scores = jogador_2_scores.round(decimals=2)
jogador_2_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_2
jogador_2_percs = jogador_2_percs[
((jogador_2_percs['Atleta'] == jogador_2) & (jogador_2_percs['Clube'] == equipe_2)  & (jogador_2_percs['Temporada'] == temporada_2))]
jogador_2_percs = jogador_2_percs.iloc[:, np.r_[3, 47:52]].reset_index(drop=True)
jogador_2_percs = jogador_2_percs.round(decimals=0)
jogador_2_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_2 + "_percent"
jogador_2_percs.iloc[0, 0] = jogador_2 + "_percent"

# Create a dictionary of columns to rename by removing the '_percentil' suffix
#columns_to_rename = {
#    col: col.replace('_Percentil', '') for col in jogador_2_percs.columns if '_Percentil' in col
#}            

#Collecting data to plot
#jogador_2_percs.rename(columns=columns_to_rename, inplace=True)
                    
#Concatenating scores and percentiles for jogador 1
jogador_2_scores = pd.concat([jogador_2_scores, jogador_2_percs])
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores = jogador_2_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_2_scores.columns = jogador_2_scores.iloc[0]  # Set the first row as the header
jogador_2_scores = jogador_2_scores.drop(jogador_2_scores.index[0])  # Drop the old header row
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores.insert(0, 'Métricas', métricas_resistência_pressão)

#################################################################################################################
#################################################################################################################

# Function to apply conditional formatting based on the percentile values
def apply_colormap_based_on_value(val):
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    if pd.isna(val):
        return ''  # No styling for NaN values
    elif val >= 90:
        color = cmap2(0.70)  # "Elite"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 75 <= val < 90:
        color = cmap2(0.50)  # "Destaque"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 60 <= val < 75:
        color = cmap(0.50)  # "Razoável"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 40 <= val < 60:
        color = cmap(0.25)  # "Mediano"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 20 <= val < 40:
        color = cmap1(0.30)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    else:
        color = cmap1(0.50)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
# Function to apply the colormap to a specified column based on the corresponding percentiles column
def apply_colormap_to_column_based_on_percentiles(styler, df, values_col, percentiles_col):
    colormap_styles = [apply_colormap_based_on_value(val) for val in df[percentiles_col]]
    return styler.apply(lambda _: colormap_styles, subset=[values_col])

# Function to merge jogador_1_scores and jogador_2_scores
def merge_scores_tables(jogador_1_scores, jogador_2_scores):
    # Rename the columns for each player
    jogador_1_scores.columns = ['Métricas', jogador_1, 'Player 1 Percentiles']
    jogador_2_scores.columns = ['Métricas', jogador_2, 'Player 2 Percentiles']

    # Merge the two DataFrames on the "Métricas" column
    merged_df = pd.merge(jogador_1_scores[['Métricas', jogador_1, 'Player 1 Percentiles']],
                        jogador_2_scores[['Métricas', jogador_2, 'Player 2 Percentiles']],
                        on='Métricas')

    return merged_df

#################################################################################################################

# Styling function for merged DataFrame
def style_merged_table(merged_df):
    # Create a Styler object from the merged DataFrame
    styled_df = merged_df.style

    # Apply colormap to jogador_1 values based on Player 1 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_1, 'Player 1 Percentiles')

    # Apply colormap to jogador_2 values based on Player 2 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_2, 'Player 2 Percentiles')
    
    # Format both jogador_1 and jogador_2 columns to display 2 decimal places
    styled_df = styled_df.format({jogador_1: "{:.2f}", jogador_2: "{:.2f}"})
    
    # Left-align column[0] ("Métricas") and center columns[1, 2] ("jogador_1" and "jogador_2")
    styled_df = styled_df.set_properties(subset=['Métricas'], **{'text-align': 'left'})
    styled_df = styled_df.set_properties(subset=[jogador_1, jogador_2], **{'text-align': 'center'})

    # Drop both percentile columns from the final display
    styled_df = styled_df.hide(axis='columns', subset=['Player 1 Percentiles', 'Player 2 Percentiles'])

    # Apply table styles as in the LAST CODE
    styled_df = styled_df.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('font-weight', 'bold'),
                    ('border-style', 'solid'),
                    ('border-width', '0px 0px 2px 0px'),
                    ('border-color', 'black')]
        }, {
            'selector': 'thead th:not(:first-child)',
            'props': [('text-align', 'center')]  # Center headers except the first
        }, {
            'selector': 'thead th:last-child',
            'props': [('color', 'black')]  # Make last column header black
        }, {
            'selector': 'td',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'center')]
        }, {
            'selector': 'th',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'left')]
        }, {
            'selector': '.index_name',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of the index
        }, {
            'selector': '.row_heading',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of row headers
        }]
    ).set_properties(**{'padding': '2px', 'font-size': '16px'})

    return styled_df

#################################################################################################################

# Main function to process the data
def main():
    # Assuming jogador_1_scores and jogador_2_scores are already defined with the necessary columns (Métricas, Values, Percentiles)

    # Merge the two tables
    merged_scores = merge_scores_tables(jogador_1_scores, jogador_2_scores)

    # Style the merged table
    styled_merged_scores = style_merged_table(merged_scores)

    # Convert to HTML and display (for Streamlit, you'd use st.markdown)
    merged_html = styled_merged_scores.to_html(escape=False, index=False)
    center_html = f"<div style='margin-left: auto; margin-right: auto; width: fit-content;'>{merged_html}</div>"

    # Output the final table (for Streamlit, you'd use st.markdown)
    st.markdown(center_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()

#################################################################################################################

# Function to plot the legend using the same colors as the apply_colormap_based_on_value function
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

##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################

métricas_transição_ofensiva = ['Passes de criação de jogadas (90)', 
                                'xT Passes para último terço (p90)', 
                                'xT Progressão com bola (p90)'
]

#Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis e Métricas de<br>Transição Ofensiva</h3>", unsafe_allow_html=True)

Transição_Ofensiva_Zagueiro_Charts = Zagueiro_Charts_1.copy()

#Collecting data to plot
metrics = Transição_Ofensiva_Zagueiro_Charts.iloc[:, np.r_[3, 84, 77, 85]].reset_index(drop=True)
## parameter names
params = list(metrics.columns[1:])

## range values
ranges = [(0, 100), (0, 100), (0, 100)]
a_values = []
b_values = []

# Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
for i, atleta in enumerate(metrics['Atleta']):
    if atleta == jogador_1:
        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
    elif atleta == jogador_2:
        b_values = metrics.iloc[i, 1:].tolist()

values = [a_values, b_values]

## title values
title = dict(
    title_name=jogador_1,
    title_color='#B6282F',
    subtitle_name=f"{equipe_1} ({temporada_1})",
    subtitle_color='#B6282F',
    title_name_2=jogador_2,
    title_color_2='#344D94',
    subtitle_name_2=f"{equipe_2} ({temporada_2})",
    subtitle_color_2='#344D94',
    title_fontsize=20,
    subtitle_fontsize=18,
)

## endnote 
endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

## instantiate object
#radar = Radar()

radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig, ax = radar.plot_radar(
    ranges=ranges,
    params=params,
    values=values,
    radar_color=['#B6282F', '#344D94'],
    dpi=600,
    alphas=[.8, .6],
    title=title,
    endnote=endnote,
    compare=True
)
st.pyplot(fig)

####################################################################################################
######################################################################################################################################
######################################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_1_scores = pd.read_csv('patch_code.csv')
jogador_1_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_1
jogador_1_scores = jogador_1_scores[
((jogador_1_scores['Atleta'] == jogador_1) & (jogador_1_scores['Clube'] == equipe_1) & (jogador_1_scores['Temporada'] == temporada_1))]
jogador_1_scores = jogador_1_scores.iloc[:, np.r_[3, 64, 57, 65]].reset_index(drop=True)
jogador_1_scores = jogador_1_scores.round(decimals=2)
jogador_1_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_1
jogador_1_percs = jogador_1_percs[
((jogador_1_percs['Atleta'] == jogador_1) & (jogador_1_percs['Clube'] == equipe_1)  & (jogador_1_percs['Temporada'] == temporada_1))]
jogador_1_percs = jogador_1_percs.iloc[:, np.r_[3, 84, 77, 85]].reset_index(drop=True)
jogador_1_percs = jogador_1_percs.round(decimals=0)
jogador_1_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_1 + "_percent"
jogador_1_percs.iloc[0, 0] = jogador_1 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_1_scores = pd.concat([jogador_1_scores, jogador_1_percs])
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores = jogador_1_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_1_scores.columns = jogador_1_scores.iloc[0]  # Set the first row as the header
jogador_1_scores = jogador_1_scores.drop(jogador_1_scores.index[0])  # Drop the old header row
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores.insert(0, 'Métricas', métricas_transição_ofensiva)

#################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_2_scores = pd.read_csv('patch_code.csv')
jogador_2_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_2
jogador_2_scores = jogador_2_scores[
((jogador_2_scores['Atleta'] == jogador_2) & (jogador_2_scores['Clube'] == equipe_2) & (jogador_2_scores['Temporada'] == temporada_2))]
jogador_2_scores = jogador_2_scores.iloc[:, np.r_[3, 64, 57, 65]].reset_index(drop=True)
jogador_2_scores = jogador_2_scores.round(decimals=2)
jogador_2_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_2
jogador_2_percs = jogador_2_percs[
((jogador_2_percs['Atleta'] == jogador_2) & (jogador_2_percs['Clube'] == equipe_2)  & (jogador_2_percs['Temporada'] == temporada_2))]
jogador_2_percs = jogador_2_percs.iloc[:, np.r_[3, 84, 77, 85]].reset_index(drop=True)
jogador_2_percs = jogador_2_percs.round(decimals=0)
jogador_2_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_2 + "_percent"
jogador_2_percs.iloc[0, 0] = jogador_2 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_2_scores = pd.concat([jogador_2_scores, jogador_2_percs])
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores = jogador_2_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_2_scores.columns = jogador_2_scores.iloc[0]  # Set the first row as the header
jogador_2_scores = jogador_2_scores.drop(jogador_2_scores.index[0])  # Drop the old header row
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores.insert(0, 'Métricas', métricas_transição_ofensiva)

#################################################################################################################
#################################################################################################################

# Function to apply conditional formatting based on the percentile values
def apply_colormap_based_on_value(val):
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    if pd.isna(val):
        return ''  # No styling for NaN values
    elif val >= 90:
        color = cmap2(0.70)  # "Elite"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 75 <= val < 90:
        color = cmap2(0.50)  # "Destaque"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 60 <= val < 75:
        color = cmap(0.50)  # "Razoável"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 40 <= val < 60:
        color = cmap(0.25)  # "Mediano"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 20 <= val < 40:
        color = cmap1(0.30)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    else:
        color = cmap1(0.50)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
# Function to apply the colormap to a specified column based on the corresponding percentiles column
def apply_colormap_to_column_based_on_percentiles(styler, df, values_col, percentiles_col):
    colormap_styles = [apply_colormap_based_on_value(val) for val in df[percentiles_col]]
    return styler.apply(lambda _: colormap_styles, subset=[values_col])

# Function to merge jogador_1_scores and jogador_2_scores
def merge_scores_tables(jogador_1_scores, jogador_2_scores):
    # Rename the columns for each player
    jogador_1_scores.columns = ['Métricas', jogador_1, 'Player 1 Percentiles']
    jogador_2_scores.columns = ['Métricas', jogador_2, 'Player 2 Percentiles']

    # Merge the two DataFrames on the "Métricas" column
    merged_df = pd.merge(jogador_1_scores[['Métricas', jogador_1, 'Player 1 Percentiles']],
                        jogador_2_scores[['Métricas', jogador_2, 'Player 2 Percentiles']],
                        on='Métricas')

    return merged_df

#################################################################################################################

# Styling function for merged DataFrame
def style_merged_table(merged_df):
    # Create a Styler object from the merged DataFrame
    styled_df = merged_df.style

    # Apply colormap to jogador_1 values based on Player 1 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_1, 'Player 1 Percentiles')

    # Apply colormap to jogador_2 values based on Player 2 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_2, 'Player 2 Percentiles')
    
    # Format both jogador_1 and jogador_2 columns to display 2 decimal places
    styled_df = styled_df.format({jogador_1: "{:.2f}", jogador_2: "{:.2f}"})
    
    # Left-align column[0] ("Métricas") and center columns[1, 2] ("jogador_1" and "jogador_2")
    styled_df = styled_df.set_properties(subset=['Métricas'], **{'text-align': 'left'})
    styled_df = styled_df.set_properties(subset=[jogador_1, jogador_2], **{'text-align': 'center'})

    # Drop both percentile columns from the final display
    styled_df = styled_df.hide(axis='columns', subset=['Player 1 Percentiles', 'Player 2 Percentiles'])

    # Apply table styles as in the LAST CODE
    styled_df = styled_df.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('font-weight', 'bold'),
                    ('border-style', 'solid'),
                    ('border-width', '0px 0px 2px 0px'),
                    ('border-color', 'black')]
        }, {
            'selector': 'thead th:not(:first-child)',
            'props': [('text-align', 'center')]  # Center headers except the first
        }, {
            'selector': 'thead th:last-child',
            'props': [('color', 'black')]  # Make last column header black
        }, {
            'selector': 'td',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'center')]
        }, {
            'selector': 'th',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'left')]
        }, {
            'selector': '.index_name',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of the index
        }, {
            'selector': '.row_heading',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of row headers
        }]
    ).set_properties(**{'padding': '2px', 'font-size': '16px'})

    return styled_df

#################################################################################################################

# Main function to process the data
def main():
    # Assuming jogador_1_scores and jogador_2_scores are already defined with the necessary columns (Métricas, Values, Percentiles)

    # Merge the two tables
    merged_scores = merge_scores_tables(jogador_1_scores, jogador_2_scores)

    # Style the merged table
    styled_merged_scores = style_merged_table(merged_scores)

    # Convert to HTML and display (for Streamlit, you'd use st.markdown)
    merged_html = styled_merged_scores.to_html(escape=False, index=False)
    center_html = f"<div style='margin-left: auto; margin-right: auto; width: fit-content;'>{merged_html}</div>"

    # Output the final table (for Streamlit, you'd use st.markdown)
    st.markdown(center_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()

#################################################################################################################

# Function to plot the legend using the same colors as the apply_colormap_based_on_value function
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


####################################################################################################

métricas_superioridade_duelos = ['Sucesso em desarmes (%)', 'Desarmes vencidos (p90)', 
                                'Sucesso em 1v1 (p90)', 'Duelos defensivos vencidos (%)', 
                                'Duelos defensivos vencidos (p90)', 'Duelos aéreos vencidos (%)', 
                                'Duelos aéreos vencidos (p90)'
]

#Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: blue; '>Percentis e Métricas de<br>Superioridade em Duelos</h3>", unsafe_allow_html=True)

Superioridade_Duelos_Zagueiro_Charts = Zagueiro_Charts_1.copy()

#Collecting data to plot
metrics = Superioridade_Duelos_Zagueiro_Charts.iloc[:, np.r_[3, 29, 98:102, 36:38]].reset_index(drop=True)

## parameter names
params = list(metrics.columns[1:])

## range values
ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
a_values = []
b_values = []

# Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
for i, atleta in enumerate(metrics['Atleta']):
    if atleta == jogador_1:
        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
    elif atleta == jogador_2:
        b_values = metrics.iloc[i, 1:].tolist()

values = [a_values, b_values]

## title values
title = dict(
    title_name=jogador_1,
    title_color='#B6282F',
    subtitle_name=f"{equipe_1} ({temporada_1})",
    subtitle_color='#B6282F',
    title_name_2=jogador_2,
    title_color_2='#344D94',
    subtitle_name_2=f"{equipe_2} ({temporada_2})",
    subtitle_color_2='#344D94',
    title_fontsize=20,
    subtitle_fontsize=18,
)

## endnote 
endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

## instantiate object
#radar = Radar()

radar=Radar(fontfamily='Cursive', range_fontsize=8)
fig, ax = radar.plot_radar(
    ranges=ranges,
    params=params,
    values=values,
    radar_color=['#B6282F', '#344D94'],
    dpi=600,
    alphas=[.8, .6],
    title=title,
    endnote=endnote,
    compare=True
)
st.pyplot(fig)

####################################################################################################
######################################################################################################################################
######################################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_1_scores = pd.read_csv('patch_code.csv')
jogador_1_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_1
jogador_1_scores = jogador_1_scores[
((jogador_1_scores['Atleta'] == jogador_1) & (jogador_1_scores['Clube'] == equipe_1) & (jogador_1_scores['Temporada'] == temporada_1))]
jogador_1_scores = jogador_1_scores.iloc[:, np.r_[3, 9, 78:82, 16:18]].reset_index(drop=True)
jogador_1_scores = jogador_1_scores.round(decimals=2)
jogador_1_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_1
jogador_1_percs = jogador_1_percs[
((jogador_1_percs['Atleta'] == jogador_1) & (jogador_1_percs['Clube'] == equipe_1)  & (jogador_1_percs['Temporada'] == temporada_1))]
jogador_1_percs = jogador_1_percs.iloc[:, np.r_[3, 29, 98:102, 36:38]].reset_index(drop=True)
jogador_1_percs = jogador_1_percs.round(decimals=0)
jogador_1_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_1 + "_percent"
jogador_1_percs.iloc[0, 0] = jogador_1 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_1_scores = pd.concat([jogador_1_scores, jogador_1_percs])
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores = jogador_1_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_1_scores.columns = jogador_1_scores.iloc[0]  # Set the first row as the header
jogador_1_scores = jogador_1_scores.drop(jogador_1_scores.index[0])  # Drop the old header row
jogador_1_scores = jogador_1_scores.reset_index(drop=True)
jogador_1_scores.insert(0, 'Métricas', métricas_superioridade_duelos)

#################################################################################################################

# #Elaborar Tabela com Métricas do Atleta
jogador_2_scores = pd.read_csv('patch_code.csv')
jogador_2_percs = pd.read_csv('patch_code_per.csv')
#Collecting Z-scores for jogador_2
jogador_2_scores = jogador_2_scores[
((jogador_2_scores['Atleta'] == jogador_2) & (jogador_2_scores['Clube'] == equipe_2) & (jogador_2_scores['Temporada'] == temporada_2))]
jogador_2_scores = jogador_2_scores.iloc[:, np.r_[3, 9, 78:82, 16:18]].reset_index(drop=True)
jogador_2_scores = jogador_2_scores.round(decimals=2)
jogador_2_scores.rename(columns={'Atleta': 'Métricas'}, inplace=True)
            
#Collecting percentiles for jogador_2
jogador_2_percs = jogador_2_percs[
((jogador_2_percs['Atleta'] == jogador_2) & (jogador_2_percs['Clube'] == equipe_2)  & (jogador_2_percs['Temporada'] == temporada_2))]
jogador_2_percs = jogador_2_percs.iloc[:, np.r_[3, 29, 98:102, 36:38]].reset_index(drop=True)
jogador_2_percs = jogador_2_percs.round(decimals=0)
jogador_2_percs.rename(columns={'Atleta': 'Métricas'}, inplace=True)
# Replace the cell at [0, 0] with jogador_2 + "_percent"
jogador_2_percs.iloc[0, 0] = jogador_2 + "_percent"

#Concatenating scores and percentiles for jogador 1
jogador_2_scores = pd.concat([jogador_2_scores, jogador_2_percs])
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores = jogador_2_scores.transpose()
# Remove the index by resetting it and using new headers
jogador_2_scores.columns = jogador_2_scores.iloc[0]  # Set the first row as the header
jogador_2_scores = jogador_2_scores.drop(jogador_2_scores.index[0])  # Drop the old header row
jogador_2_scores = jogador_2_scores.reset_index(drop=True)
jogador_2_scores.insert(0, 'Métricas', métricas_superioridade_duelos)

#################################################################################################################
#################################################################################################################

# Function to apply conditional formatting based on the percentile values
def apply_colormap_based_on_value(val):
    cmap = plt.get_cmap("Blues")
    cmap1 = plt.get_cmap("Reds")
    cmap2 = plt.get_cmap("Greens")

    if pd.isna(val):
        return ''  # No styling for NaN values
    elif val >= 90:
        color = cmap2(0.70)  # "Elite"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 75 <= val < 90:
        color = cmap2(0.50)  # "Destaque"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 60 <= val < 75:
        color = cmap(0.50)  # "Razoável"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 40 <= val < 60:
        color = cmap(0.25)  # "Mediano"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    elif 20 <= val < 40:
        color = cmap1(0.30)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
    else:
        color = cmap1(0.50)  # Orange color for "Frágil"
        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, 0.8); color: black'
# Function to apply the colormap to a specified column based on the corresponding percentiles column
def apply_colormap_to_column_based_on_percentiles(styler, df, values_col, percentiles_col):
    colormap_styles = [apply_colormap_based_on_value(val) for val in df[percentiles_col]]
    return styler.apply(lambda _: colormap_styles, subset=[values_col])

# Function to merge jogador_1_scores and jogador_2_scores
def merge_scores_tables(jogador_1_scores, jogador_2_scores):
    # Rename the columns for each player
    jogador_1_scores.columns = ['Métricas', jogador_1, 'Player 1 Percentiles']
    jogador_2_scores.columns = ['Métricas', jogador_2, 'Player 2 Percentiles']

    # Merge the two DataFrames on the "Métricas" column
    merged_df = pd.merge(jogador_1_scores[['Métricas', jogador_1, 'Player 1 Percentiles']],
                        jogador_2_scores[['Métricas', jogador_2, 'Player 2 Percentiles']],
                        on='Métricas')

    return merged_df

#################################################################################################################

# Styling function for merged DataFrame
def style_merged_table(merged_df):
    # Create a Styler object from the merged DataFrame
    styled_df = merged_df.style

    # Apply colormap to jogador_1 values based on Player 1 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_1, 'Player 1 Percentiles')

    # Apply colormap to jogador_2 values based on Player 2 percentiles
    styled_df = apply_colormap_to_column_based_on_percentiles(styled_df, merged_df, jogador_2, 'Player 2 Percentiles')
    
    # Format both jogador_1 and jogador_2 columns to display 2 decimal places
    styled_df = styled_df.format({jogador_1: "{:.2f}", jogador_2: "{:.2f}"})
    
    # Left-align column[0] ("Métricas") and center columns[1, 2] ("jogador_1" and "jogador_2")
    styled_df = styled_df.set_properties(subset=['Métricas'], **{'text-align': 'left'})
    styled_df = styled_df.set_properties(subset=[jogador_1, jogador_2], **{'text-align': 'center'})

    # Drop both percentile columns from the final display
    styled_df = styled_df.hide(axis='columns', subset=['Player 1 Percentiles', 'Player 2 Percentiles'])

    # Apply table styles as in the LAST CODE
    styled_df = styled_df.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('font-weight', 'bold'),
                    ('border-style', 'solid'),
                    ('border-width', '0px 0px 2px 0px'),
                    ('border-color', 'black')]
        }, {
            'selector': 'thead th:not(:first-child)',
            'props': [('text-align', 'center')]  # Center headers except the first
        }, {
            'selector': 'thead th:last-child',
            'props': [('color', 'black')]  # Make last column header black
        }, {
            'selector': 'td',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'center')]
        }, {
            'selector': 'th',
            'props': [('border-style', 'solid'),
                    ('border-width', '0px 0px 1px 0px'),
                    ('border-color', 'black'),
                    ('text-align', 'left')]
        }, {
            'selector': '.index_name',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of the index
        }, {
            'selector': '.row_heading',
            'props': [('font-size', '15px'), ('color', 'white')]  # Adjust font size of row headers
        }]
    ).set_properties(**{'padding': '2px', 'font-size': '16px'})

    return styled_df

#################################################################################################################

# Main function to process the data
def main():
    # Assuming jogador_1_scores and jogador_2_scores are already defined with the necessary columns (Métricas, Values, Percentiles)

    # Merge the two tables
    merged_scores = merge_scores_tables(jogador_1_scores, jogador_2_scores)

    # Style the merged table
    styled_merged_scores = style_merged_table(merged_scores)

    # Convert to HTML and display (for Streamlit, you'd use st.markdown)
    merged_html = styled_merged_scores.to_html(escape=False, index=False)
    center_html = f"<div style='margin-left: auto; margin-right: auto; width: fit-content;'>{merged_html}</div>"

    # Output the final table (for Streamlit, you'd use st.markdown)
    st.markdown(center_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()

#################################################################################################################

# Function to plot the legend using the same colors as the apply_colormap_based_on_value function
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


#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
