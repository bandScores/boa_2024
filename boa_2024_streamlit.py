import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
#from src.agstyler import PINLEFT, PRECISION_TWO, draw_grid

st.set_page_config(layout="wide")
st.markdown(
            """
            <style>
            [data-testid="stElementToolbar"] {
                display: none;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

data = pd.read_csv('boa_2024.csv')
data = data.rename(columns={'P/S/F': 'Round', 'School Full':'School'})
data['Week'] = 'Week ' + data['Week Num'].astype('str')

st.title("2024 BOA Scores App")
st.write("This app shows recaps for Bands of America events from the 2024 season. Use the drop down selectors to filter by event or show round, or leave them empty to view all scores. Click on a column header to cycle through sorting options. When hovering over a column header, click the hamburger menu on the right to view more filtering options. \n")

cols = ['Date', 'Event', 'Round', 'School', 'Class', 
        'MPI', 'MPI Rank', 'MPE', 'MPE Rank', 'Mus Avg', 'Mus Avg Rank', 
        'VPI', 'VPI Rank', 'VPE', 'VPE Rank', 'Vis Avg', 'Vis Avg Rank',
        'MGE1', 'MGE1 Rank', 'MGE2', 'MGE2 Rank', 'MGE Tot', 'MGE Tot Rank',
        'VGE', 'VGE Rank', 'GE Tot', 'GE Tot Rank', 'Subtotal', #'Subtotal Rank',
        'Pen', 'Total', 'Place: Class', 'Place: Overall']

display = data[cols]

#event_select = st.multiselect('Event:', list(display['Event'].unique()))
#display = display[display['Event'].isin(event_select)]

# date_select = st.multiselect('Date:', list(display['Date'].unique()))
# display = display[display['Date'].isin(date_select)]

# school_select = st.multiselect('School:', list(display['School'].unique()))
# display = display[display['School'].isin(school_select)]

# round_select = st.multiselect('Round:', ['Prelims', 'Finals'])
# display = display[display['Round'].isin(round_select)]

# class_select = st.multiselect('Class:', ['AAAA', 'AAA', 'AA', 'A'])
# display = display[display['Class'].isin(class_select)]

row_input = st.columns((1,1,1))

with row_input[0]:
    event = st.selectbox('Select Event', list(display['Event'].unique()), placeholder='', index=None)
    if event is not None:
        fitered_string1 = 'Event=="'+event+'"'
        display = display.query(fitered_string1)
        display.drop('Date', axis=1, inplace=True)
        display.drop('Event', axis=1, inplace=True)
        
with row_input[1]:    
    round = st.selectbox('Select Show Round', list(display['Round'].unique()), placeholder='', index=None)
    if round is not None:
        fitered_string2 = 'Round=="'+round+'"'
        display = display.query(fitered_string2)
        display.drop('Round', axis=1, inplace=True)
        if round == 'Finals':
            display.drop('Place: Class', axis=1, inplace=True)

#with row_input[2]:
freeze = st.radio('Freeze date, event, round, school, and class columns', ['Yes', 'No (recommended for mobile users)'])


# display = display.style.format({'MPI': '{:^20.3f}', 'MPI Rank': '{:^20.0f}', 
#                                   'MPE': '{:^20.3f}',  'MPE Rank': '{:^20.0f}',  
#                                   'Mus Avg': '{:^20.3f}',  'Mus Avg Rank': '{:^20.0f}', 
#                                   'VPI': '{:^20.3f}',  'VPI Rank': '{:^20.0f}',  
#                                   'VPE': '{:^20.3f}',  'VPE Rank': '{:^20.0f}',  
#                                   'Vis Avg': '{:^20.3f}',  'Vis Avg Rank': '{:^20.0f}', 
#                                   'MGE1':'{:^20.3f}',  'MGE1 Rank':'{:^20.0f}',  
#                                   'MGE2':'{:^20.3f}',  'MGE2 Rank':'{:^20.0f}',  
#                                   'MGE Tot':'{:^20.3f}',  'MGE Tot Rank':'{:^20.0f}', 
#                                   'VGE':'{:^20.3f}',  'VGE Rank':'{:^20.0f}',  
#                                   'GE Tot':'{:^20.3f}',  'GE Tot Rank':'{:^20.0f}',  
#                                   'Subtotal':'{:^20.3f}',  #'Subtotal Rank',
#                                   'Pen': '{:^20.0f}',  'Total': '{:^20.3f}',  
#                                   'Place: Class': '{:^20.0f}',  'Place: Overall': '{:^20.0f}'})

gridOptions = {
    'defaultColDef': {
        'sortable': True,
        'filter': True,
        'resizable': True},
    'domLayout': 'normal',
    'pagination': True,
    'paginationPageSize': 100,
    'cellStyle': {'fontSize': '5px'},
    'columnDefs': [
        {'headerName': 'Date', 'field': 'Date', 'width': 90, 'pinned': 'left', 'filter': 'true'},
        {'headerName': 'Event', 'field': 'Event', 'width': 170, 'pinned': 'left', 'filter': 'true'},
        {'headerName': 'Round', 'field': 'Round', 'width': 80, 'pinned': 'left', 'filter': 'true'},
        {'headerName': 'School', 'field': 'School', 'width': 250, 'pinned': 'left', 'filter': 'true'},
        {'headerName': 'Class', 'field': 'Class', 'width': 80, 'pinned': 'left', 'filter': 'true'},
        {'headerName': 'Music Individual', 'children':[
            {'headerName': 'Score','field': 'MPI', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'MPI Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Music Ensemble', 'children':[
            {'headerName': 'Score','field': 'MPE', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'MPE Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Music Average', 'children':[
            {'headerName': 'Score','field': 'Mus Avg', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'Mus Avg Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Visual Individual', 'children':[
            {'headerName': 'Score','field': 'VPI', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'VPI Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Visual Ensemble', 'children':[
            {'headerName': 'Score','field': 'VPE', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'VPE Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Visual Average', 'children':[
            {'headerName': 'Score','field': 'Vis Avg', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'Vis Avg Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Music GE 1', 'children':[
            {'headerName': 'Score','field': 'MGE1', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'MGE1 Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Music GE 2', 'children':[
            {'headerName': 'Score','field': 'MGE2', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'MGE2 Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Total Music GE', 'children':[
            {'headerName': 'Score','field': 'MGE Tot', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'MGE Tot Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Visual GE', 'children':[
            {'headerName': 'Score','field': 'VGE', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'VGE Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Total GE', 'children':[
            {'headerName': 'Score','field': 'GE Tot', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
            {'headerName': 'Rank', 'field': 'GE Tot Rank', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
        {'headerName': 'Sub','field': 'Subtotal', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'}, 
        {'headerName': 'Pen','field': 'Pen', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(1)'}, 
        {'headerName': 'Total','field': 'Total', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
        {'headerName': 'Ranks', 'children':[
            {'headerName': 'Overall','field': 'Place: Overall', 'width': 90, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'},
            {'headerName': 'Class', 'field': 'Place: Class', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
             'type': 'numericColumn'}]},
    ]
}

if round == 'Finals':
    gridOptions['columnDefs'][-1]= {'headerName': 'Final Ranks','children': [
        {'headerName': 'Overall.','field': 'Place: Overall','width': 90,
         'headerClass': 'left-header', 'cellStyle': {'textAlign': 'center'},'type': 'numericColumn'}]}
if event is not None:
    gridOptions['columnDefs'].remove({'headerName': 'Date', 'field': 'Date', 'width': 90, 'pinned': 'left', 'filter': 'true'})
    gridOptions['columnDefs'].remove({'headerName': 'Event', 'field': 'Event', 'width': 170, 'pinned': 'left', 'filter': 'true'})
if round is not None:
    gridOptions['columnDefs'].remove({'headerName': 'Round', 'field': 'Round', 'width': 80, 'pinned': 'left', 'filter': 'true'})

if freeze == 'No (recommended for mobile users)':
            gridOptions['columnDefs'][0] = {'headerName': 'Date', 'field': 'Date', 'width': 90, 'pinned': 'left', 'filter': 'true'}
            gridOptions['columnDefs'][1] = {'headerName': 'Event', 'field': 'Event', 'width': 170, 'pinned': 'left', 'filter': 'true'}
            gridOptions['columnDefs'][2] = {'headerName': 'Round', 'field': 'Round', 'width': 80, 'pinned': 'left', 'filter': 'true'}
            gridOptions['columnDefs'][3] = {'headerName': 'School', 'field': 'School', 'width': 250, 'pinned': 'left', 'filter': 'true'}
            gridOptions['columnDefs'][4] = {'headerName': 'Class', 'field': 'Class', 'width': 80, 'pinned': 'left', 'filter': 'true'}

if freeze == 'Yes':
            gridOptions['columnDefs'][0] = {'headerName': 'Date', 'field': 'Date', 'width': 90, 'filter': 'true'}
            gridOptions['columnDefs'][1] = {'headerName': 'Event', 'field': 'Event', 'width': 170, 'filter': 'true'}
            gridOptions['columnDefs'][2] = {'headerName': 'Round', 'field': 'Round', 'width': 80, 'filter': 'true'}
            gridOptions['columnDefs'][3] = {'headerName': 'School', 'field': 'School', 'width': 250,'filter': 'true'}
            gridOptions['columnDefs'][4] = {'headerName': 'Class', 'field': 'Class', 'width': 80, 'filter': 'true'}


# st.markdown(
#     """
#     <style>
#     .ag-theme-streamlit {
#         width: 100vw;  /* Make grid width responsive to browser width */
#         height: 100vh;  /* Make grid height responsive to browser height */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

grid_table = AgGrid(display, 
                    gridOptions=gridOptions,
                    fit_columns_on_grid_load=False,
                    theme="streamlit",
                    enable_enterprise_modules=False,
                    fit_columns=True,
                    use_container_width=True,
                    height=600
                    #style={'width': '100%', 'height': '500px'}
                   )


# styled_df = display.style.set_properties(**{'text-align': 'center'})
# st.write(styled_df.to_html(index=False, justify='center'), unsafe_allow_html=True)


# [theme]
# primaryColor="#bf2a25"
# backgroundColor="#e6e6e6"
# secondaryBackgroundColor="#ffffff"
# textColor="#11364d"


