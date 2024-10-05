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

raw = pd.read_csv('boa_2024.csv')
raw = raw.rename(columns={'P/S/F': 'Round', 'School Full':'School'})
raw['Week'] = 'Week ' + raw['Week Num'].astype('str')

st.title("2024 BOA Scores App")
st.write("This app shows recaps for Bands of America events from the 2024 season. Use the drop down selectors to filter by event or show round, or leave them empty to view all scores. Click on a column header to cycle through sorting options. When hovering over a column header, click the hamburger menu on the right to view more filtering options. \n")

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

gridOptions = {
    'defaultColDef': {
        'sortable': True,
        'filter': True,
        'resizable': True},
    #'domLayout': 'autoHeight',
    'pagination': True,
    'paginationPageSize': 100,
    'cellStyle': {'fontSize': '5px'},
    'columnDefs': [
        {'headerName': 'Date', 'field': 'Date', 'maxWidth':85, 'filter': 'true', 'pinned':'left', 'hide':'true', 'headerClass': 'parent-header-left'}, #85
        {'headerName': 'Event', 'field': 'Event', 'width':170, 'filter': 'true', 'pinned':'left', 'hide':'true', 'headerClass': 'parent-header-left'}, #auto
        {'headerName': 'Round', 'field': 'Round', 'maxWidth':80, 'pinned':'left', 'filter': 'true', 'hide':'true', 'headerClass': 'parent-header-left'}, #80
        {'headerName': 'School', 'field': 'School', 'width':190, 'pinned':'left', 'filter': 'true', 'headerClass': 'parent-header-left'}, #auto
        {'headerName': 'Class', 'field': 'Class', 'maxWidth':70, 'pinned':'left', 'filter': 'true', 'hide':'true', 'headerClass': 'parent-header-left',
         "cellStyle": {"border-right": "4px solid #FF0000"}}, #70

        {'headerName': 'Music', 'children': [
        {'headerName': 'Ind.', 'field': 'MPI', 'maxWidth':90,
         "valueGetter": "data.MPI.toFixed(3) + '  (' + data.MPI_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MPI - nodeB.data.MPI; }"},
        {'headerName': 'Ens.', 'field': 'MPE', 'maxWidth':90, 
         "valueGetter": "data.MPE.toFixed(3) + '  (' + data.MPE_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MPE - nodeB.data.MPE; }"},     
        {'headerName': 'Avg.', 'field': 'Mus_Avg', 'maxWidth':90, "cellStyle": {"border-right": "4px solid #FF0000"}, 
         'headerTextAlign':'center', "valueGetter": "data.Mus_Avg.toFixed(3) + '  (' + data.Mus_Avg_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Mus_Avg - nodeB.data.Mus_Avg; }"}], 'headerClass': 'parent-header-center'},
        
        {'headerName': 'Visual', 'children': [
        {'headerName': 'Ind.', 'field': 'VPI', 'maxWidth':90, 
         "valueGetter": "data.VPI.toFixed(3) + '  (' + data.VPI_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VPI - nodeB.data.VPI; }"},
        {'headerName': 'Ens.', 'field': 'VPE', 'maxWidth':90,
         "valueGetter": "data.VPE.toFixed(3) + '  (' + data.VPE_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VPE - nodeB.data.VPE; }"},     
        {'headerName': 'Avg.', 'field': 'Vis_Avg', 'maxWidth':90, "cellStyle": {"border-right": "4px solid #FF0000"},
         "valueGetter": "data.Vis_Avg.toFixed(3) + '  (' + data.Vis_Avg_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Vis_Avg - nodeB.data.Vis_Avg; }"}], 'headerClass': 'parent-header-center'},

        {'headerName': 'General Effect', 'children': [
        {'headerName': 'Mus GE1', 'field': 'MGE1', 'maxWidth':90,
         "valueGetter": "data.MGE1.toFixed(3) + '  (' + data.MGE1_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MGE1 - nodeB.data.MGE1; }"},
        {'headerName': 'Mus GE2', 'field': 'MGE2', 'maxWidth':90, 
         "valueGetter": "data.MGE2.toFixed(3) + '  (' + data.MGE2_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VPE - nodeB.data.VPE; }"},     
        {'headerName': 'MGE Total', 'field': 'MGE_Tot', 'maxWidth':100,
         "valueGetter": "data.MGE_Tot.toFixed(3) + '  (' + data.MGE_Tot_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MGE_Tot - nodeB.data.MGE_Tot; }"}, 
        {'headerName': 'Vis GE', 'field': 'VGE', 'maxWidth':90, 
         "valueGetter": "data.VGE.toFixed(3) + '  (' + data.VGE_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VGE - nodeB.data.VGE; }"},
        {'headerName': 'GE Total', 'field': 'GE_Tot', 'maxWidth':90, "cellStyle": {"border-right": "4px solid #FF0000"},
         "valueGetter": "data.GE_Tot.toFixed(3) + '  (' + data.GE_Tot_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.GE_Tot - nodeB.data.GE_Tot; }"}], 'headerClass': 'parent-header-center'},

        {'headerName': 'Subtotal', 'field': 'Subtotal', 'maxWidth':90, 
         "valueGetter": "data.Subtotal.toFixed(3) + '  (' + data.Subtotal_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Subtotal - nodeB.data.Subtotal; }"},
        
        {'headerName': 'Pen.', 'field': 'Pen', 'maxWidth':65, 'valueFormatter': 'x.toFixed(1)', 'sortable':True, "cellStyle": {"text-align": "center"}},
        
         {'headerName': 'Total', 'field': 'Total', 'maxWidth':90, 
         "valueGetter": "data.Total.toFixed(3) + '  (' + data.Place_Overall + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Total - nodeB.data.Total; }"},

        {'headerName': 'Place: Class', 'field': 'Place_Class', 'maxWidth':80, 'valueFormatter': 'x.toFixed(0)', 'wrapHeaderText':True, 
         'headerClass': 'header-center header-large', 'sortable':True, 'hide':'true', 'headerClass': 'parent-header-center'},

         
        
        # {'headerName': 'Visual GE', 'children':[
        #     {'headerName': 'Score','field': 'VGE', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
        #      'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
        #     {'headerName': '-', 'field': 'VGE Rank', 'width': 50, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
        #      'type': 'numericColumn'}]},
        # {'headerName': 'Total GE', 'children':[
        #     {'headerName': 'Score','field': 'GE Tot', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
        #      'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
        #     {'headerName': '-', 'field': 'GE Tot Rank', 'width': 50, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
        #      'type': 'numericColumn'}]},
        # {'headerName': 'Sub','field': 'Subtotal', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
        #      'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'}, 
        # {'headerName': 'Pen','field': 'Pen', 'width': 50, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
        #      'type': 'numericColumn', 'valueFormatter': 'x.toFixed(1)'}, 
        # {'headerName': 'Total','field': 'Total', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
        #      'type': 'numericColumn', 'valueFormatter': 'x.toFixed(3)'},
        # {'headerName': 'Ranks', 'children':[
        #     {'headerName': 'Ovr.','field': 'Place: Overall', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
        #      'type': 'numericColumn'},
        #     {'headerName': 'Class', 'field': 'Place: Class', 'width': 70, 'headerClass': 'left-header','cellStyle': {'textAlign': 'center'}, 
        #      'type': 'numericColumn'}]},
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

# Responsive CSS for both desktop and mobile
markdown = """
    <style>
    body {
    background-color: yellow;
    }
    
    /* Custom borders for cells */
    .custom-border-right .ag-cell {
        border-right: 2px solid #000000;
    }
    
    .custom-border-left .ag-cell {
        border-left: 2px solid #000000;
    }
    
    /* Center-align header */
    .header-center .ag-header-cell {
        text-align: center !important;
    }
    
    /* Left-align header */
    .header-left .ag-header-cell {
        text-align: left !important;
    }
    
    /* Font size customization */
    .header-large .ag-header-cell {
        font-size: 18px !important;
    }
    
    .header-small .ag-header-cell {
        font-size: 12px !important;
    }

    .header-center .ag-header-cell {
    background-color: red !important;
    }
    </style>
    """

custom_css = {
        #'.ag-header-cell': {'text-align': 'center !important;'},
        '.parent-header-center': {'justify-content': 'center !important;', 'font-size': '16px !important;', 'font-weight': 'bold !important;', 'color': 'black !important;'},
        '.parent-header-left': {'justify-content': 'left !important;', 'font-size': '16px !important;', 'font-weight': 'bold !important;', 'color': 'black !important;'},
        '.ag-header-cell-label': {'justify-content': 'left !important;', 'font-size': '12px !important;'}, 
        '.ag-cell': {'border-right': '2px solid #000000;'}, 
        '.ag-theme-streamlit': {'width': '100vw !important;', 'height': 'calc(100vh - 100px) !important;', 'overflow-y': 'auto !important;'}, 
        '@media only screen and (max-width: 600px)': {
                '.ag-header-cell-label': {
                    'font-size': '12px !important;',  # Smaller font for mobile
                    'padding': '5px !important;',  # Reduce padding to fit on small screens
                },
                '.ag-root-wrapper': {
                    'width': '100% !important;',  # Full width on mobile
                    'overflow-x': 'scroll !important;'  # Allow horizontal scrolling if needed
                },
                '.ag-cell': {
                    'font-size': '12px !important;',  # Smaller font in cells for mobile
                    'padding': '5px !important;'  # Adjust padding for mobile
                }}
        }



    #     .header-center .ag-header-cell {
    #     text-align: center !important;
    # }
    
    # /* Left-align header */
    # .header-left .ag-header-cell {
    #     text-align: left !important;
    # }
    
    # /* Font size customization */
    # .header-large .ag-header-cell {
    #     font-size: 18px !important;
    # }
    
    # .header-small .ag-header-cell {
    #     font-size: 12px !important;
    # }

    # .header-center .ag-header-cell {
    # background-color: red !important;
    # }
    # </style>
    # """



#st.markdown(markdown, unsafe_allow_html=True)

grid_table = AgGrid(display, 
                    gridOptions=gridOptions,
                    fit_columns_on_grid_load=False,
                    theme="streamlit",
                    enable_enterprise_modules=False,
                    enable_pagination=True,
                    fit_columns=False,
                    use_container_width=True,
                    height=550, 
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


