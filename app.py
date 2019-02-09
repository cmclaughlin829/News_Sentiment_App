# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_ui as dui
import plotly.graph_objs as go
import json
import pickle
from datetime import datetime, timedelta

#Import Data
with open('data/article_wordcount_dict.pkl', 'rb') as handle:
    article_wordcount_dict = pickle.load(handle)

with open('data/title_wordcount_dict.pkl', 'rb') as handle:
    title_wordcount_dict = pickle.load(handle)

with open('data/article_sentiment_dict.pkl', 'rb') as handle:
    article_sentiment_dict = pickle.load(handle)

with open('data/title_sentiment_dict.pkl', 'rb') as handle:
    title_sentiment_dict = pickle.load(handle)

with open('data/mean_share_count_dict.pkl', 'rb') as handle:
    mean_share_count_dict = pickle.load(handle)

with open('data/total_share_count_dict.pkl', 'rb') as handle:
    total_share_count_dict = pickle.load(handle)

with open('data/df_histogram.pkl', 'rb') as handle:
    df = pickle.load(handle)

#Set color scheme for candidate groups
colors_dict = {
    'trump_source': 'rgb(256, 0, 0)',
    'trump_shares': 'rgb(256, 180, 180)',
    'clinton_source': 'rgb(0, 0, 256)',
    'clinton_shares': 'rgb(180, 180, 256)'
}

#Set sentiment graph legend text
legend_dict = {
    'trump_source': 'Trump - Top Sources',
    'trump_shares': 'Trump - Most Shares',
    'clinton_source': 'Clinton - Top Sources',
    'clinton_shares': 'Clinton - Most Shares'
}

my_css_urls = [
  "https://codepen.io/cmclaughlin829/pen/pGwbvG.css",
  "https://use.fontawesome.com/releases/v5.1.0/css/all.css"
]

app = dash.Dash()

for url in my_css_urls:
    app.css.append_css({
        "external_url": url
    })

server = app.server

controlpanel = dui.ControlPanel(_id = 'controlpanel')

#Create control panel using dash_ui
controlpanel.create_group(
    group = 'body_title_group',
    group_title = 'Calculate Sentiment of Article Body or Title?'
)
body_title_select = dcc.RadioItems(
    id = 'body_title_radio',
    options = [
        {'label': 'Article Body', 'value': 'body'},
        {'label': 'Article Title', 'value': 'title'}
    ],
    labelStyle = {'display': 'inline-block'},
    value = 'body'
)
controlpanel.add_element(body_title_select, 'body_title_group')

controlpanel.create_group(
    group = 'week_month_group',
    group_title = 'Aggregate Mean Sentiment by Week or Month?'
)
week_month_select = dcc.RadioItems(
    id = 'week_month_radio',
    options = [
        {'label': 'Aggregate by Week', 'value': 'W-SAT'},
        {'label': 'Aggregate by Month', 'value': 'M'}
    ],
    labelStyle = {'display': 'inline-block'},
    value = 'W-SAT'
)
controlpanel.add_element(week_month_select, 'week_month_group')

controlpanel.create_group(
    group = 'mean_total_group',
    group_title = 'Rank Sources by Total Shares or Mean Shares?'
)
week_month_select = dcc.RadioItems(
    id = 'mean_total_radio',
    options = [
        {'label': 'Display Total Shares', 'value': 'total_shares'},
        {'label': 'Display Mean Shares', 'value': 'mean_shares'}
    ],
    labelStyle = {'display': 'inline-block'},
    value = 'total_shares'
)
controlpanel.add_element(week_month_select, 'mean_total_group')

controlpanel.create_group(
    group = 'candidate_group',
    group_title = 'Select Group of Articles to Display'
)
candidate_select = dcc.Checklist(
    id = 'trump_clinton_checklist',
    options = [
        {'label': 'Trump Articles - Top News Sources', 'value': 'trump_source'},
        {'label': 'Trump Articles - Most Facebook Shares', 'value': 'trump_shares'},
        {'label': 'Clinton Articles - Top News Sources', 'value': 'clinton_source'},
        {'label': 'Clinton Articles - Most Facebook Shares', 'value': 'clinton_shares'}
    ],
    values = ['trump_source', 'trump_shares', 'clinton_source', 'clinton_shares']
)
controlpanel.add_element(candidate_select, 'candidate_group')

controlpanel.create_group(
    group = 'spacer'
)

controlpanel.create_group(
    group = 'instructions_group2',
    group_title = '''All articles and data acquired from eventregistry.org.  \
                     Sentiment calculated using vaderSentiment. for additional \
                     information please visit https://github.com/cmclaughlin829
    '''
)

#Crete dashboard layout
grid = dui.Grid(
    _id = 'grid',
    num_rows = 12,
    num_cols = 12,
    grid_padding = 0
)

_iconStyle = {
    'font-size': 16,
    'padding': 2,
    'color': 'white'
}
_style = {
    "height": 32,
    "width": 32,
    "padding": 2,
    "border-radius": "2px",
    "flex": 1,
    "margin-right": 2
}

#dashboard title container
grid.add_element(
    col = 1,
    row = 1,
    width = 12,
    height = 1,
    element =
        html.Div([
            html.H1(
                children = 'News Sentiment Analysis of 2016 Presidential \
                            Election News Coverage',
                id = 'app_title',
                style = {
                    'font-family': 'Georgia',
                    'margin': '0 auto',
                    'text-align': 'center',
                    'fontSize': '1.75vw'
                }
            ),
            html.P(
                children = 'A Comparison of Articles Most Shared on Facebook \
                            vs. Articles from Top News Sources',
                id = 'app_subtitle',
                style = {
                    'font-family': 'Georgia',
                    'margin': '0 auto',
                    'text-align': 'center',
                    'fontSize': '1vw'
                }
            )
            ]
    )
)

#dashboard graph elements
grid.add_graph(col = 1, row = 2, width = 12, height = 4, graph_id = 'sentiment_graph')
grid.add_graph(col = 1, row = 6, width = 4, height = 6, graph_id = 'word_count_bar')
grid.add_graph(col = 5, row = 6, width = 4, height = 6, graph_id = 'share_count_bar')
grid.add_graph(col = 9, row = 6, width = 4, height = 6, graph_id = 'shares_scatter')

#dashboard article information containers
grid.add_element(
    col = 1,
    row = 12,
    width = 8,
    height = 1,
    element =
        html.Div(
            id = 'shared_article',
            style = {
                'background-color': 'white',
                #'margin': '10',
                'height': '100%',
                'width': '100%',
                'fontSize': '1.25vw'
                #'border': '1px solid'
            }
        )
)
grid.add_element(
    col = 9,
    row = 12,
    width = 4,
    height = 1,
    element =
        html.Div(
            id = 'shared_article_source',
            style = {
                'background-color': 'white',
                #'margin': '10',
                'height': '100%',
                'width': '100%',
                'fontSize': '1.25vw'
                #'border': '1px solid'
            }
        )
)

app.layout = html.Div(
    dui.Layout(
        grid=grid,
        controlpanel=controlpanel
    ),
    style={
        'height': '100vh',
        'width': '100vw'
    }
)

#callback to update sentiment graph based on control panel selections
@app.callback(
    Output('sentiment_graph', 'figure'),
    [Input('body_title_radio', 'value'),
     Input('week_month_radio', 'value'),
     Input('trump_clinton_checklist', 'values')]
)
def update_sentiment(body_title, week_month, trump_clinton):
    if body_title == 'body':
        sentiment_data = article_sentiment_dict
    else:
        sentiment_data = title_sentiment_dict

    if week_month =='W-SAT':
        week_month_str = 'Week'
    else:
        week_month_str = 'Month'

    traces = []
    for i in trump_clinton:
        traces.append(go.Scatter(
            x = list(sentiment_data[i][week_month].keys()),
            y = list(sentiment_data[i][week_month].values()),
            mode = 'lines+markers',
            name = legend_dict[i],
            marker = {
                'color': colors_dict[i]
            })
        )
    layout = go.Layout(
        yaxis = {
            'range': [-.25, .25],
            'automargin': True,
            'title': 'Mean Sentiment'
        },
        xaxis = {
            'automargin': True
        },
        clickmode = 'event+select',
        title = 'Mean Article {} Sentiment Aggregated by {}'\
                .format(body_title.capitalize(), week_month_str)
    )
    return {
        'data': traces,
        'layout': layout
    }

#callback to update word count bar chart
@app.callback(
    Output('word_count_bar', 'figure'),
    [Input('body_title_radio', 'value'),
     Input('week_month_radio', 'value'),
     Input('trump_clinton_checklist', 'values'),
     Input('sentiment_graph', 'clickData')]
)
def update_word_count(body_title, week_month, checklist, clickData):
    #set default value if clickData is empty
    if clickData:
        curve_number = clickData['points'][0]['curveNumber']
        trace_name = checklist[curve_number]
        date = clickData['points'][0]['x']
    elif clickData is None and week_month == 'W-SAT':
        trace_name = 'trump_shares'
        date = '01/09/2016'
    else:
        trace_name = 'trump_shares'
        date = '01/31/2016'

    if body_title == 'body':
        word_count_data = article_wordcount_dict
        body_title_str = 'Body'
    else:
        word_count_data = title_wordcount_dict
        body_title_str = 'Title'

    bars = [go.Bar(
                x = list(word_count_data[trace_name][week_month][date].keys()),
                y = list(word_count_data[trace_name][week_month][date].values()),
                marker = {
                    'color':colors_dict[trace_name]
                }
    )]
    layout = go.Layout(
        autosize = True,
        xaxis = {
            'automargin': True
        },
        yaxis = {
            'title': 'Word Frequency'
        },
        title = '20 Most Frequently Used Words<br>in Article {} ({})'\
                .format(body_title_str, date)
    )

    return {
        'data': bars,
        'layout': layout
    }

#callback to update share count bar chart
@app.callback(
    Output('share_count_bar', 'figure'),
    [Input('body_title_radio', 'value'),
     Input('week_month_radio', 'value'),
     Input('mean_total_radio', 'value'),
     Input('trump_clinton_checklist', 'values'),
     Input('sentiment_graph', 'clickData')]
)
def update_share_count(body_title, week_month, mean_total, checklist, clickData):
    if mean_total == 'mean_shares':
        share_count_dict = mean_share_count_dict
        mean_total_str = 'Mean'
    else:
        share_count_dict = total_share_count_dict
        mean_total_str = 'Total'

    #set default value if clickData is empty
    if clickData:
        curve_number = clickData['points'][0]['curveNumber']
        trace_name = checklist[curve_number]
        date = clickData['points'][0]['x']
    elif clickData is None and week_month == 'W-SAT':
        trace_name = 'trump_shares'
        date = '01/09/2016'
    else:
        trace_name = 'trump_shares'
        date = '01/31/2016'

    bars = [go.Bar(
                x = list(share_count_dict[trace_name][week_month][date].keys()),
                y = list(share_count_dict[trace_name][week_month][date].values()),
                marker = {
                    'color':colors_dict[trace_name]
                }
    )]
    layout = go.Layout(
        autosize = True,
        xaxis = {
            'automargin': True
        },
        yaxis = {
            'title': 'Shares'
        },
        title = 'Top 20 News Sources by<br>{} Shares ({})'.format(mean_total_str, date),
        clickmode = 'event+select'
    )

    return {
        'data': bars,
        'layout': layout
    }

#callback to update shares scatter plot
@app.callback(
    Output('shares_scatter', 'figure'),
    [Input('body_title_radio', 'value'),
     Input('week_month_radio', 'value'),
     Input('mean_total_radio', 'value'),
     Input('trump_clinton_checklist', 'values'),
     Input('sentiment_graph', 'clickData'),
     Input('share_count_bar', 'selectedData')]
)
def update_shares_scatter(body_title, week_month, mean_total, checklist, \
                         clickData, selectedData):
    #set default value if clickData is empty
    if clickData:
        end_date_str = clickData['points'][0]['x']
        curve_number = clickData['points'][0]['curveNumber']
        trace_name = checklist[curve_number]
    elif clickData is None and week_month == 'W-SAT':
        trace_name = 'trump_shares'
        end_date_str = '01/09/2016'
    else:
        trace_name = 'trump_shares'
        end_date_str = '01/31/2016'

    end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()

    if mean_total == 'mean_shares':
        share_count_dict = mean_share_count_dict
    else:
        share_count_dict = total_share_count_dict

    if week_month == 'M':
        start_date =  end_date.replace(day=1)
    else:
        start_date = end_date - timedelta(days = 6)

    if body_title == 'body':
        sentiment_str = 'articleSentiment'
    else:
        sentiment_str = 'titleSentiment'

    #set default value if selectedData is empty
    #if not empty, create list of selected news sources
    if selectedData:
        source_list = [selectedData['points'][i]['x'] for i in \
                    range(len(selectedData['points']))]
    else:
        source_list = list(share_count_dict[trace_name][week_month]\
                    [end_date_str].keys())

    #filter df based on selections
    df_filtered = df[(df['origin'] == trace_name) & (df['news_source'].\
                isin(source_list))].sort_index().loc[start_date:end_date]
    df_range = df[df['origin'] == trace_name].sort_index()\
                .loc[start_date:end_date]

    #determine static axis range
    max_shares = df_range.facebook_shares.max()
    padding = max_shares/20

    trace = [go.Scatter(
        y = df_filtered.facebook_shares,
        x = df_filtered[sentiment_str],
        marker = {
            'color':colors_dict[trace_name]
        },
        mode = 'markers',
        text = df_filtered.row_id,
        name = 'shares_sentiment'
    )]

    layout =  go.Layout(
        yaxis = {
            'range': [0, max_shares+padding],
            'automargin': True,
            'title': 'Shares'
        },
        xaxis = {
            'range': [-1, 1],
            'automargin': True,
            'title': 'Sentiment'
        },
        clickmode = 'event+select',
        title = 'Article Shares vs. {} Sentiment<br>({})'\
                .format(body_title.capitalize(), end_date_str)
    )

    return {
        'data': trace,
        'layout': layout
    }

#callback to update shared article title
@app.callback(
    Output('shared_article', 'children'),
    [Input('week_month_radio', 'value'),
     Input('body_title_radio', 'value'),
     Input('trump_clinton_checklist', 'values'),
     Input('sentiment_graph', 'clickData'),
     Input('shares_scatter', 'clickData')]
)
def update_shared_article(week_month, body_title, checklist, sent_clickData,\
                        scat_clickData):
    #set default value if sent_clickData is empty
    #account for empty data and both week_month options (different end dates)
    #avoids key error in dict lookup
    if sent_clickData:
        end_date_str = sent_clickData['points'][0]['x']
        curve_number = sent_clickData['points'][0]['curveNumber']
        trace_name = checklist[curve_number]
    elif sent_clickData is None and week_month == 'W-SAT':
        trace_name = 'trump_shares'
        end_date_str = '01/09/2016'
    else:
        trace_name = 'trump_shares'
        end_date_str = '01/31/2016'

    end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()

    if week_month == 'M':
        start_date =  end_date.replace(day=1)
    else:
        start_date = end_date - timedelta(days = 6)

    #create filtered df based on selections
    df_filtered = df[df['origin'] == trace_name].sort_index()\
                .loc[start_date:end_date]

    #set default value if scat_clickData is empty
    #if not empty identify df row containing selected article
    if scat_clickData:
        marker_id = scat_clickData['points'][0]['text']
        row = df_filtered[df_filtered['row_id'] == marker_id]
        title = row.title[0]
        text = u'Article Title: {}'.format(title)
    else:
        text = u'Select a Shares vs. Sentiment Point to Display Article Information'

    return text

#callback to update shared article title
@app.callback(
    Output('shared_article_source', 'children'),
    [Input('week_month_radio', 'value'),
     Input('body_title_radio', 'value'),
     Input('trump_clinton_checklist', 'values'),
     Input('sentiment_graph', 'clickData'),
     Input('shares_scatter', 'clickData')]
)
def update_shared_article_source(week_month, body_title, checklist, \
                                sent_clickData, scat_clickData):
    #set default value if sent_clickData is empty
    #account for empty data and both week_month options (different end dates)
    #avoids key error in dict lookup
    if sent_clickData:
        end_date_str = sent_clickData['points'][0]['x']
        curve_number = sent_clickData['points'][0]['curveNumber']
        trace_name = checklist[curve_number]
    elif sent_clickData is None and week_month == 'W-SAT':
        trace_name = 'trump_shares'
        end_date_str = '01/09/2016'
    else:
        trace_name = 'trump_shares'
        end_date_str = '01/31/2016'

    end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()

    if week_month == 'M':
        start_date =  end_date.replace(day=1)
    else:
        start_date = end_date - timedelta(days = 6)

    #create filtered df based on selections
    df_filtered = df[df['origin'] == trace_name].sort_index()\
                .loc[start_date:end_date]

    #set default value if scat_clickData is empty
    #if not empty identify df row containing selected article
    if scat_clickData:
        marker_id = scat_clickData['points'][0]['text']
        row = df_filtered[df_filtered['row_id'] == marker_id]
        news_source = row.news_source[0]
        text = u'Article Source: {}'.format(news_source)
    else:
        text = None

    return text

#callbacks to clear selectedData and clickData when new date is selected
@app.callback(
    Output('share_count_bar', 'selectedData'),
    [Input('sentiment_graph', 'clickData')]
)
def selectedData_clear(clickData):
    return None

@app.callback(
    Output('shares_scatter', 'clickData'),
    [Input('sentiment_graph', 'clickData')]
)
def selectedData_clear(clickData):
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
