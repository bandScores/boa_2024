import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
#from src.agstyler import PINLEFT, PRECISION_TWO, draw_grid

st.set_page_config(layout="wide")
# st.markdown(
#             """
#             <style>
#             [data-testid="stElementToolbar"] {
#                 display: none;
#             }
#             </style>
#             """,
#             unsafe_allow_html=True
#         )

st.markdown(
    """
    <style>
    /* Full screen on desktop */
    .ag-theme-streamlit {
        width: 100vw;  /* Make grid width 100% of the viewport width */
        height: 80vh;  /* Adjust height based on available viewport height */
    }

    /* Adjust for mobile screens */
    @media only screen and (max-width: 600px) {
        .ag-theme-streamlit {
            width: 100vw !important;  /* Full width for mobile */
            height: 100vh !important;  /* Full height for mobile */
            overflow-x: auto;  /* Allow horizontal scroll if content overflows */
        }
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
freeze = st.radio('Freeze Date, Event, Round, School, and Class columns', ['Yes', 'No (recommended for mobile users)'])

gridOptions = {
    'defaultColDef': {
        'sortable': True,
        'filter': True,
        'resizable': True},
    'domLayout': 'autoHeight',
    'pagination': True,
    'paginationPageSize': 100,
    'cellStyle': {'fontSize': '5px'},
    'columnDefs': [
        {'headerName': 'Date', 'field': 'Date', 'flex':1, 'pinned':'left', 'filter': 'true', 'hide':'true'}, #85
        {'headerName': 'Event', 'field': 'Event', 'flex':1, 'pinned':'left', 'filter': 'true', 'hide':'true'}, #auto
        {'headerName': 'Round', 'field': 'Round', 'flex':1, 'pinned':'left', 'filter': 'true', 'hide':'true'}, #80
        {'headerName': 'School', 'field': 'School', 'flex':1, 'pinned':'left', 'filter': 'true'}, #auto
        {'headerName': 'Class', 'field': 'Class', 'flex':1, 'pinned':'left', 'filter': 'true'}, #70
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

if freeze != 'Yes':
            gridOptions['columnDefs'][0].pop('pinned', None)
            gridOptions['columnDefs'][1].pop('pinned', None)
            gridOptions['columnDefs'][2].pop('pinned', None)
            gridOptions['columnDefs'][3].pop('pinned', None)
            gridOptions['columnDefs'][4].pop('pinned', None)

if event is None: 
            gridOptions['columnDefs'][0].pop('hide', None)
            gridOptions['columnDefs'][1].pop('hide', None)

if round is None:
            gridOptions['columnDefs'][2].pop('hide', None)

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


