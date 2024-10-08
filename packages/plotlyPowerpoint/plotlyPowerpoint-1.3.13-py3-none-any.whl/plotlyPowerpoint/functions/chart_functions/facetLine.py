import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def createFacetLineChart(df, chartDefinition, colors):

    #Create Fig
    facets = df[chartDefinition['facet']].unique().tolist()
    facetSpacing = chartDefinition['options']['facet-spacing'] if 'facet-spacing' in chartDefinition['options'] else 0.1
    
    if chartDefinition['facet-direction'] == 'rows':
        fig = make_subplots(len(facets), 1, vertical_spacing=facetSpacing)
    else:
        fig = make_subplots(1, len(facets), horizontal_spacing=facetSpacing)

    #add traces for all metrics and all facets
    for i in range(len(chartDefinition['metrics'])):
        for facet in facets:

            #filter data for only current facet
            temp2 = df[df[chartDefinition['facet']] == facet]
            position = facets.index(facet)

            #get proper color for line
            if 'color-grouping' in chartDefinition['options']:
                if chartDefinition['options']['color-grouping'] == 'facet':
                    lineColor = colors[position]
                else:
                    lineColor = colors[i]
            else:
                lineColor = colors[i]

            fig.add_trace(
                go.Scatter(
                    x=temp2[chartDefinition['axis']],
                    y=temp2[chartDefinition['metrics'][i]['name']],
                    mode='lines',
                    name=facet,
                    line = dict(color=lineColor)
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


    #return
    return fig