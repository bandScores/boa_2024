import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_gsheets import GSheetsConnection

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

url = "https://docs.google.com/spreadsheets/d/1dgV0saovQ5tVe6OeGYHLaLMzh-2qq1EfUVGfQg3XRhU/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)
raw = conn.read(spreadsheet=url)
#st.dataframe(data)

#raw = pd.read_csv('boa_2024_oct12.csv')
raw = raw.rename(columns={'P/S/F': 'Round', 'School Full':'School'})
raw['Week'] = 'Week ' + raw['Week Num'].astype('str')

#st.title("2024 BOA Scores App")
#st.write("This app shows recaps for Bands of America events from the 2024 season. Use the drop down selectors to filter by event or show round, or leave them empty to view all scores. Click on a column header to cycle through sorting options. When hovering over a column header, click the hamburger menu on the right to view more filtering options. \n")

cols = ['Date', 'Event', 'Round', 'School', 'Class', 
        'MPI', 'MPI Rank', 'MPE', 'MPE Rank', 'Mus Avg', 'Mus Avg Rank', 
        'VPI', 'VPI Rank', 'VPE', 'VPE Rank', 'Vis Avg', 'Vis Avg Rank',
        'MGE1', 'MGE1 Rank', 'MGE2', 'MGE2 Rank', 'MGE Tot', 'MGE Tot Rank',
        'VGE', 'VGE Rank', 'GE Tot', 'GE Tot Rank', 'Subtotal', 'Subtotal Rank',
        'Pen', 'Total', 'Place: Class', 'Place: Overall']

display = raw[cols]

cols_new = ['Date', 'Event', 'Round', 'School', 'Class', 
        'MPI', 'MPI_Rank', 'MPE', 'MPE_Rank', 'Mus_Avg', 'Mus_Avg_Rank', 
        'VPI', 'VPI_Rank', 'VPE', 'VPE_Rank', 'Vis_Avg', 'Vis_Avg_Rank',
        'MGE1', 'MGE1_Rank', 'MGE2', 'MGE2_Rank', 'MGE_Tot', 'MGE_Tot_Rank',
        'VGE', 'VGE_Rank', 'GE_Tot', 'GE_Tot_Rank', 'Subtotal', 'Subtotal_Rank',
        'Pen', 'Total', 'Place_Class', 'Place_Overall']

display = display.set_axis(cols_new, axis=1)
data = display.to_dict()

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
        
with row_input[1]:    
    round = st.selectbox('Select Show Round', list(display['Round'].unique()), placeholder='', index=None)
    if round is not None:
        fitered_string2 = 'Round=="'+round+'"'
        display = display.query(fitered_string2)

with row_input[2]:    
    class_ = st.selectbox('Select Class', ['AAAA', 'AAA', 'AA', 'A'], placeholder='', index=None)
    if class_ is not None:
        fitered_string3 = 'Class=="'+class_+'"'
        display = display.query(fitered_string3)

#with row_input[2]:
freeze = st.radio('Freeze Date, Event, Round, School, and Class columns', ['Yes', 'No (recommended for mobile users)'])

if event is None and round is None:
        if class_ is None:
                st.write(f'<p style="font-size:20px; font-weight:bold;">All scores from all events, classes, and rounds</p>', unsafe_allow_html=True)
        if class_ is not None:
                st.write(f'<p style="font-size:20px; font-weight:bold;">All {class_} scores from all events and rounds</p>', unsafe_allow_html=True)

if event is not None and round is None:
        if class_ is None:
                st.write(f'<p style="font-size:20px; font-weight:bold;">{event} - All Rounds and Classes</p>', unsafe_allow_html=True)
        if class_ is not None:
                st.write(f'<p style="font-size:20px; font-weight:bold;">{event} - {class_} Scores from All Rounds</p>', unsafe_allow_html=True)

if event is None and round is not None:
        if class_ is None:
                st.write(f'<p style="font-size:20px; font-weight:bold;">{round} scores from all events and classes</p>', unsafe_allow_html=True)
        if class_ is not None:
                st.write(f'<p style="font-size:20px; font-weight:bold;">{class_} scores from {round} rounds at all events</p>', unsafe_allow_html=True)

if event is not None and round is not None:
        if class_ is None:
                st.write(f'<p style="font-size:20px; font-weight:bold;">{event} - {round}</p>', unsafe_allow_html=True)
        if class_ is not None:
                st.write(f'<p style="font-size:20px; font-weight:bold;">{event} - {round} - {class_} Scores</p>', unsafe_allow_html=True)

gridOptions = {
    'defaultColDef': {
        'sortable': True,
        'filter': True,
        'resizable': True},
    #'domLayout': 'autoHeight',
    'pagination': True,
    'paginationPageSize': 100,
    'rowHeight': 40,
    'cellStyle': {'fontSize': '5px'},
    'columnDefs': [
        {'headerName': 'Date', 'field': 'Date', 'maxWidth':90, 'filter': 'true', 'pinned':'left', 'hide':'true', 'headerClass': 'parent-header-left', 'suppressMovable':'true'}, #85
        {'headerName': 'Event', 'field': 'Event', 'width':170, 'filter': 'true', 'pinned':'left', 'hide':'true', 'headerClass': 'parent-header-left', 'suppressMovable':'true'}, #auto
        {'headerName': 'Round', 'field': 'Round', 'maxWidth':80, 'pinned':'left', 'filter': 'true', 'hide':'true', 'headerClass': 'parent-header-left', 'suppressMovable':'true'}, #80
        {'headerName': 'School', 'field': 'School', 'width':190, 'pinned':'left', 'filter': 'true', 'headerClass': 'parent-header-left', 'suppressMovable':'true'}, #auto
        {'headerName': 'Class', 'field': 'Class', 'maxWidth':75, 'pinned':'left', 'filter': 'true', 'hide':'true', 'headerClass': 'parent-header-left', 'suppressMovable':'true',
         'cellClass': 'custom-border-right'}, #70

        {'headerName': 'Music', 'children': [
        {'headerName': 'Ind.', 'field': 'MPI', 'maxWidth':65, 'headerClass': 'group-header-center', 'textAlign': 'Center', 'suppressMovable':'true',
         'autoHeight':True, 'wrapText':True, "valueGetter": "data.MPI.toFixed(3) + ' (' + data.MPI_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True, "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MPI - nodeB.data.MPI; }"},
        {'headerName': 'Ens.', 'field': 'MPE', 'maxWidth': 65,  'headerClass': 'group-header-center', 'textAlign': 'Center', 'suppressMovable': 'true',
         'autoHeight':True, 'wrapText':True, "valueGetter": "data.MPE.toFixed(3) + ' (' + data.MPE_Rank + ')'",
         "sortable": True, "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MPE - nodeB.data.MPE; }"},
        {'headerName': 'Avg.', 'field': 'Mus_Avg', 'maxWidth':65, 'headerClass': 'group-header-center', 'cellClass': 'custom-border-right', 'textAlign': 'Center', 'suppressMovable':'true',
         'autoHeight':True, 'wrapText':True, "valueGetter": "data.Mus_Avg.toFixed(3) + ' (' + data.Mus_Avg_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True, "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Mus_Avg - nodeB.data.Mus_Avg; }"}], 'headerClass': 'parent-header-center'},
        
        {'headerName': 'Visual', 'children': [
        {'headerName': 'Ind.', 'field': 'VPI', 'maxWidth':93, 'headerClass': 'group-header-center', 'suppressMovable':'true',
         "valueGetter": "data.VPI.toFixed(3) + '  (' + data.VPI_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VPI - nodeB.data.VPI; }"},
        {'headerName': 'Ens.', 'field': 'VPE', 'maxWidth':93, 'headerClass': 'group-header-center', 'suppressMovable':'true',
         "valueGetter": "data.VPE.toFixed(3) + '  (' + data.VPE_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VPE - nodeB.data.VPE; }"},     
        {'headerName': 'Avg.', 'field': 'Vis_Avg', 'maxWidth':93, 'headerClass': 'group-header-center', 'cellClass': 'custom-border-right', 'suppressMovable':'true',
         "valueGetter": "data.Vis_Avg.toFixed(3) + '  (' + data.Vis_Avg_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Vis_Avg - nodeB.data.Vis_Avg; }"}], 'headerClass': 'parent-header-center'},

        {'headerName': 'General Effect', 'children': [
        {'headerName': 'Mus GE1', 'field': 'MGE1', 'maxWidth':93, 'headerClass': 'group-header-center', 'suppressMovable':'true',
         "valueGetter": "data.MGE1.toFixed(3) + '  (' + data.MGE1_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MGE1 - nodeB.data.MGE1; }"},
        {'headerName': 'Mus GE2', 'field': 'MGE2', 'maxWidth':93, 'headerClass': 'group-header-center', 'suppressMovable':'true',
         "valueGetter": "data.MGE2.toFixed(3) + '  (' + data.MGE2_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VPE - nodeB.data.VPE; }"},     
        {'headerName': 'MGE Total', 'field': 'MGE_Tot', 'maxWidth':103, 'headerClass': 'group-header-center', 'suppressMovable':'true',
         "valueGetter": "data.MGE_Tot.toFixed(3) + '  (' + data.MGE_Tot_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MGE_Tot - nodeB.data.MGE_Tot; }"}, 
        {'headerName': 'Vis GE', 'field': 'VGE', 'maxWidth':93, 'headerClass': 'group-header-center', 'suppressMovable':'true',
         "valueGetter": "data.VGE.toFixed(3) + '  (' + data.VGE_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VGE - nodeB.data.VGE; }"},
        {'headerName': 'GE Total', 'field': 'GE_Tot', 'maxWidth':93, 'headerClass': 'group-header-center', 'cellClass': 'custom-border-right', 'suppressMovable':'true',
         "valueGetter": "data.GE_Tot.toFixed(3) + '  (' + data.GE_Tot_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.GE_Tot - nodeB.data.GE_Tot; }"}], 'headerClass': 'parent-header-center'},

        {'headerName': 'Subtotal', 'field': 'Subtotal', 'maxWidth':93, 'headerClass': 'group-header-center', 'suppressMovable':'true',
         "valueGetter": "data.Subtotal.toFixed(3) + '  (' + data.Subtotal_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Subtotal - nodeB.data.Subtotal; }"},
        
        {'headerName': 'Pen.', 'field': 'Pen', 'maxWidth':65, 'valueFormatter': 'x.toFixed(1)', 'sortable':True, 'headerClass': 'group-header-center', 'suppressMovable':'true'},
        
         {'headerName': 'Total', 'field': 'Total', 'maxWidth':93, 'headerClass': 'group-header-center', 'suppressMovable':'true',
         "valueGetter": "data.Total.toFixed(3) + '  (' + data.Place_Overall + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Total - nodeB.data.Total; }"},

        {'headerName': 'Place: Class', 'field': 'Place_Class', 'maxWidth':80, 'valueFormatter': 'x.toFixed(0)', 'wrapHeaderText':True, 'suppressMovable':'true',
         'sortable':True, 'hide':'true', 'headerClass': 'group-header-center'},
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
if round != "Finals":
    gridOptions['columnDefs'][-1].pop('hide', None)

if class_ is None:
    gridOptions['columnDefs'][4].pop('hide', None)
    

custom_css = {
        #'.ag-header-cell': {'text-align': 'center !important;'},
        '.parent-header-center': {'justify-content': 'center !important;', 'font-size': '14px !important;', 'font-weight': 'bold !important;', 'color': 'black !important;'},
        '.parent-header-left': {'justify-content': 'left !important;', 'font-size': '14px !important;', 'font-weight': 'bold !important;', 'color': 'black !important;'},
        '.group-header-center': {'justify-content': 'center !important;', 'font-size': '12px !important;', 'color': 'black !important;'},
        #'.ag-header-cell-label': {'justify-content': 'left !important;', 'font-size': '14px !important;', 'font-weight': 'bold !important;', 'color': 'black !important;'}, 
        '.custom-border-right': {'border-right': '3px solid black !important;'},  # Thick black right border
        '.ag-theme-streamlit': {'overflow-y': 'auto !important;'}, 
        '@media only screen and (max-width: 600px)': {
                '.ag-header-cell-label': {
                    'font-size': '5px !important;',  # Smaller font for mobile
                    'padding': '2px !important;',  # Reduce padding to fit on small screens
                },
                '.ag-root-wrapper': {
                    'width': '100% !important;',  # Full width on mobile
                    'overflow-x': 'scroll !important;'  # Allow horizontal scrolling if needed
                },
                '.ag-cell': {
                    'font-size': '5px !important;',  # Smaller font in cells for mobile
                    'padding': '2px !important;'  # Adjust padding for mobile
                }}
        }

#st.markdown(markdown, unsafe_allow_html=True)

grid_table = AgGrid(display, 
                    gridOptions=gridOptions,
                    fit_columns_on_grid_load=False,
                    theme="streamlit",
                    enable_enterprise_modules=False,
                    enable_pagination=True,
                    fit_columns=False,
                    use_container_width=True,
                    height=600, 
                    spacing='4px',
                    custom_css = custom_css
                    #style={'width': '100%', 'height': '500px'}
                   )

# styled_df = display.style.set_properties(**{'text-align': 'center'})
# st.write(styled_df.to_html(index=False, justify='center'), unsafe_allow_html=True)


# [theme]
# primaryColor="#bf2a25"
# backgroundColor="#e6e6e6"
# secondaryBackgroundColor="#ffffff"
# textColor="#11364d"


