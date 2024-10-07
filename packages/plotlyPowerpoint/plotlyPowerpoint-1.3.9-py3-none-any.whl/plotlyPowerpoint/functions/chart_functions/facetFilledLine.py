import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def createFacetFilledLineChart(df, chartDefinition, colors):
    #throw error if there are multiple metrics
    if len(chartDefinition['metrics']) > 1:
        raise ValueError('Filled line charts can only have one metric. Please convert your metrics into a variable:value format and break out the line chart by color')

    #Create Fig
    facets = df[chartDefinition['facet']].unique().tolist()
    facetSpacing = chartDefinition['options']['facet-spacing'] if 'facet-spacing' in chartDefinition['options'] else 0.1
    
    if chartDefinition['facet-direction'] == 'rows':
        fig = make_subplots(len(facets), 1, vertical_spacing=facetSpacing)
    else:
        fig = make_subplots(1, len(facets), horizontal_spacing=facetSpacing)

    #Add the figure to each subplot
    facetMemory = []
    for facet in facets:
        
        #filter data for only current facet
        temp2 = df[df[chartDefinition['facet']] == facet]
        position = facets.index(facet)
        
        #Add figure, based on whether we're breaking down by color                
        if 'color' in chartDefinition:
            colorOptions = list(temp2[chartDefinition['color']].unique())
            for clr in colorOptions:
                
                #set parameters we need later
                colorPosition = colorOptions.index(clr)
                showLegend = False if clr in facetMemory else True
                
                #form new temp
                temp3 = temp2[temp2[chartDefinition['color']] == clr]
                
                #add trace
                fig.add_trace(go.Scatter(
                        x=temp3[chartDefinition['axis']],
                        y=temp3[chartDefinition['metrics'][0]['name']],
                        hoverinfo='x+y',
                        mode='lines',
                        stackgroup='one',
                        fill='tonexty',
                        name=clr,
                        legendgroup=clr,
                        showlegend=showLegend,
                        line=dict(width=0.5, color=colors[colorPosition])
                    ),
                    position + 1 if chartDefinition['facet-direction'] == 'rows' else 1,
                    position + 1 if chartDefinition['facet-direction'] == 'columns' else 1
                )
                
                #add memory that we now used this color option within the faceting
                facetMemory.append(clr)

                
        else:
            fig.add_trace(go.Scatter(
                    x=temp2[chartDefinition['axis']],
                    y=temp2[chartDefinition['metrics'][0]['name']],
                    hoverinfo='x+y',
                    mode='lines',
                    fill='tonexty',
                    name=facet,
                    line=dict(width=0.5)
                ),
                position + 1 if chartDefinition['facet-direction'] == 'rows' else 1,
                position + 1 if chartDefinition['facet-direction'] == 'columns' else 1
            )
    
    #change aesthetics
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    
    
    ### Handle all options
    if 'options' in chartDefinition:

        ### Grid lines
        if 'horizontal-grid-lines' in chartDefinition['options']:
            if chartDefinition['options']['horizontal-grid-lines'] == 'true':
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ebebeb')

        if 'vertical-grid-lines' in chartDefinition['options']:
            if chartDefinition['options']['vertical-grid-lines'] == 'true':
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ebebeb')

    #update legend
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="center",
        x=.5,
        y=-.3,
        title=""
    ))

    #X axis title
    if 'x-axis-title' in chartDefinition:
        if chartDefinition['facet-direction'] == 'rows':
            fig.update_xaxes(title_text=chartDefinition['x-axis-title'], row=len(facets), col=1)
        else:
            for i in range(len(facets)):
                fig.update_xaxes(title_text=chartDefinition['x-axis-title'], row=1, col=i+1)

    #Y axis title
    if 'y-axis-title' in chartDefinition:
        if chartDefinition['facet-direction'] == 'rows':
            for i in range(len(facets)):
                fig.update_yaxes(title_text=chartDefinition['y-axis-title'], row=i+1, col=1)
        else:
            fig.update_yaxes(title_text=chartDefinition['y-axis-title'], row=1, col=1)