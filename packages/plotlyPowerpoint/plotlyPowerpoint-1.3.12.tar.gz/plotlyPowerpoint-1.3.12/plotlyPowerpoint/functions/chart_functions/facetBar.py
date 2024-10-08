import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def createFacetBarChart(df, chartDefinition, colors):

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
                    barColor = colors[position]
                elif chartDefinition['options']['color-grouping'] == 'axis':
                    axisPoints = temp2[chartDefinition['axis']].unique()
                    barColor = colors[0:len(axisPoints)]
                else:
                    barColor = colors[i]
            else:
                barColor = colors[i]

            fig.add_trace(
                go.Bar(
                    x=temp2[chartDefinition['axis']],
                    y=temp2[chartDefinition['metrics'][i]['name']],
                    name=facet,
                    marker=dict(color=barColor)
                ), 
                position + 1 if chartDefinition['facet-direction'] == 'rows' else 1,
                position + 1 if chartDefinition['facet-direction'] == 'columns' else 1
            )

    #change aesthetics
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

#             #make facet titles just the value
#             fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

#             #add data labels
#             if chartDefinition['label_type'] == 'normal':
#                 fig.update_traces(texttemplate='%{value:.2s}', textposition='outside', textangle=0)
#             elif chartDefinition['label_type'] == 'money':
#                 fig.update_traces(texttemplate='%{value:$.2s}', textposition='inside', textangle=0)

#             #update size and labels
#             fig.update_xaxes(title_text = "Date", tickfont=dict(size=6))
#             fig.update_yaxes(tickfont=dict(size=6))

    #update legend, margins, font size, etc.
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            xanchor="center",
            x=.5,
            y=-.3,
            title=""
        ),
        margin=dict(
            l=0, r=0, t=40, b=70
        )
    )

    #return
    return fig
