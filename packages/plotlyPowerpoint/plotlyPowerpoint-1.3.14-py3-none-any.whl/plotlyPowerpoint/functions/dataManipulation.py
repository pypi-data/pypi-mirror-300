import pandas as pd

def prepareData(df, chartDefinition):

    #filter data if needed
    if 'filters' in chartDefinition:
        filters = []
        for item in chartDefinition['filters']:
            if item["type"] == "int":
                statement = "df['" + item["variable"] + "'] " + item["operation"] + " int(" + item["value"] + ")"
            elif item['type'] == 'str':
                statement = "df['" + item["variable"] + "'] " + item["operation"] + " '" + item["value"] + "'"
            elif item['type'] == 'date':
                statement = "df['" + item["variable"] + "'] " + item["operation"] + " '" + item["value"] + "'"
            elif (item['type'] == 'list') and (item['operation'] == 'in'):
                statement = "df['" + item["variable"] + "'].isin(" + str(item["value"]) + ")"
            elif (item['type'] == 'list') and (item['operation'] == 'not in'):
                statement = "~df['" + item["variable"] + "'].isin(" + str(item["value"]) + ")"
            filters.append(statement)

        #filter data
        for i in range(len(filters)):
            df = df.loc[eval(filters[i]), :]

    #group data by axis and breakdowns
    groupList = []
    if chartDefinition['type'] != 'table':
        #assembe list        
        if 'color' in chartDefinition:
            groupList.append(chartDefinition['color'])

        #add axis
        groupList.append(chartDefinition['axis'])

        #add facet if included
        if 'facet' in chartDefinition:
            groupList.append(chartDefinition['facet'])

        #assemble dictionary for aggregation
        metricDict = {}
        for metric in chartDefinition["metrics"]:
            metricDict[metric["name"]] = metric["method"]

        #finally group and summarise data
        df = df.groupby(groupList).agg(metricDict).reset_index()

    
    #return
    return {'dataframe': df, 'groupList': groupList}