import plotly.express as px
import plotly.graph_objects as go

def createBarChart(df, chartDefinition, colors, groupList):

    #First, define whether or not we have 1 or many metrics
    if len(chartDefinition['metrics']) == 1:
        
        #Find proper orientation of bar chart
        if 'options' in chartDefinition:
            if 'orientation' in chartDefinition['options']:
                if chartDefinition['options']['orientation'] == 'horizontal':
                    x = df[chartDefinition['metrics'][0]['name']]
                    y = df[chartDefinition['axis']]
                    orien='h'
                else:
                    x = df[chartDefinition['axis']]
                    y = df[chartDefinition['metrics'][0]['name']]
                    orien='v'
            else:
                x = df[chartDefinition['axis']]
                y = df[chartDefinition['metrics'][0]['name']]
                orien='v'
        else:
            x = df[chartDefinition['axis']]
            y = df[chartDefinition['metrics'][0]['name']]
            orien='v'
        
        #Setup figure, based on if color is set in function
        if 'color' in chartDefinition:
            fig = px.bar(df,
                            x=x,
                            y=y,
                            color=chartDefinition['color'],
                            orientation=orien,
                            color_discrete_sequence=colors
                        )
        else:
            fig = px.bar(df,
                            x=x,
                            y=y,
                            color=groupList[0],
                            orientation=orien,
                            color_discrete_sequence=colors
                        )

    else: #multiple metrics
    
            # Create fig
        fig = go.Figure()

        # Add all bars to chart
        for i in range(len(chartDefinition['metrics'])):

            #horizontal or vertical for bar chart
            if 'options' in chartDefinition:
                if 'orientation' in chartDefinition['options']:
                    if chartDefinition['options']['orientation'] == 'horizontal':
                        x = df[chartDefinition['metrics'][i]['name']]
                        y = df[chartDefinition['axis']]
                        orien='h'
                    else:
                        x = df[chartDefinition['axis']]
                        y = df[chartDefinition['metrics'][i]['name']]
                        orien='v'
                else:
                    x = df[chartDefinition['axis']]
                    y = df[chartDefinition['metrics'][i]['name']]
                    orien='v'
            else:
                x = df[chartDefinition['axis']]
                y = df[chartDefinition['metrics'][i]['name']]
                orien='v'

            #add trace to chart    
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=y,
                    name=chartDefinition['metrics'][i]['prettyName'],
                    marker_color=colors[i],
                    orientation=orien
                )
            ) 

    #change aesthetics
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    
    ### Handle Options
    if 'options' in chartDefinition:
        
        #If horizontal, reverse axis
        if 'orientation' in chartDefinition['options']:
            if chartDefinition['options']['orientation'] == 'horizontal':
                fig['layout']['yaxis']['autorange'] = "reversed"

#                 #add data labels
#                 if 'datalabels' in chartDefinition['options']:
#                     if chartDefinition['options']['datalabels'] == 'true':
#                         if chartDefinition['label_type'] == 'money':
#                             textFormat = '%{value:$.2s}'
#                         elif chartDefinition['label_type'] == 'percent':
#                             textFormat = '%{value:.1%}'

#                         fig.update_traces(texttemplate=textFormat, textposition='inside', textangle=0)
#                         fig.update_layout(uniformtext_minsize=12)

    

    #update legend
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="center",
        x=.5,
        y=-.3,
        title=""
    ))


    #return
    return fig