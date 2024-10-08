import plotly.express as px
import plotly.graph_objects as go

def createLineWithHighlightChart(df, chartDefinition, colors):

    #Form figure
    fig = go.Figure()

    #Iterate through metrics
    annotations = []
    for i in range(len(chartDefinition['metrics'])):

        #add main line
        fig.add_trace(go.Scatter(x=df[chartDefinition['axis']],
                                    y=df[chartDefinition['metrics'][i]['name']],
                                    mode='lines',
                                    name=chartDefinition['metrics'][i]['prettyName'],
                                    line = dict(color=colors[i])
                                )
                        )

        #Add the ending marker
        fig.add_trace(go.Scatter(            
            x=[df[chartDefinition['axis']][len(df)-1]],
            y=[df[chartDefinition['metrics'][i]['name']][len(df)-1]],
            mode='markers',
            marker=dict(color=colors[i], size=8)            
        ))

        #Add an annotation for the text itself   
        annotations.append(
            {
                'xref': 'paper', 'x': 1.01, 'y': df[chartDefinition['metrics'][i]['name']][len(df)-1],
                'xanchor': 'left', 'yanchor': 'middle', 'text': df[chartDefinition['metrics'][i]['prettyName']][len(df)-1],
                'showarrow': False, 'font': {'size': 14, 'color': colors[i]}
            }
        )

    #add annotations 
    fig.update_layout(
        annotations=annotations
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
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ebebeb', title="")

        ### X axis ticks rotation
        if 'x-axis-ticks-angle' in chartDefinition['options']:
            fig.update_xaxes(nticks=df[chartDefinition['axis']].nunique(), tickangle=chartDefinition['options']['x-axis-ticks-angle'])


    #hide legend for now
    fig.update_layout(showlegend=False)

    #X axis title
    if 'x-axis-title' in chartDefinition:
        fig.update_layout(
            xaxis_title=chartDefinition['x-axis-title']
        )

    #Y axis title
    if 'y-axis-title' in chartDefinition:
        fig.update_layout(
            yaxis_title=chartDefinition['y-axis-title']
        )

    #Force y axis to 0
    fig.update_yaxes(rangemode="tozero")

    #if we want to change the y axis type
    if 'y-axis-type' in chartDefinition:
        if chartDefinition['y-axis-type'] == 'percent':
            fig.layout.yaxis.tickformat = ',.0%'

    #return
    return fig