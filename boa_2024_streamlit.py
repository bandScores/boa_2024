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

# Responsive CSS for both desktop and mobile
markdown = """
    <style>
    
    .ag-theme-streamlit .custom-border-right .ag-cell {
        border-right: 2px solid #000000;  /* Change border for custom class */
    }
    .ag-theme-streamlit .custom-border-left .ag-cell {
        border-left: 2px solid #000000;  /* Change border for another class */
    }

    .custom-header .ag-header-cell-label {
        justify-content: center !important;  /* Center align the header text */
        white-space: normal !important;      /* Enable text wrapping */
        text-align: center !important;       /* Ensure text is centered */
        overflow-wrap: break-word;           /* Break words for wrapping */
    }

    ag-header-cell {
        justify-content: center !important;  /* Center align the header text */
    }
    
    /* General grid container styles */
    .ag-theme-streamlit {
        width: 100vw !important;
        height: calc(100vh - 100px) !important;  /* Adjust based on viewport, with room for header/footer */
        overflow-y: auto !important;
    }

    /* Adjust for small screen sizes like mobile */
    @media only screen and (max-width: 600px) {
        .ag-theme-streamlit {
            width: 100vw !important;
            height: calc(100vh - 100px) !important;  /* Adjust based on viewport */
            overflow-x: scroll !important;  /* Allow horizontal scrolling */
            font-size: 12px !important;  /* Smaller font size on mobile */
        }
    }
    </style>
    """

st.markdown(markdown, unsafe_allow_html=True)

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
    'headerHeight':40,
    'cellStyle': {'fontSize': '5px'},
    'columnDefs': [
        {'headerName': 'Date', 'field': 'Date', 'width':85, 'pinned':'left', 'filter': 'true', 'hide':'true'}, #85
        {'headerName': 'Event', 'field': 'Event', 'width':150, 'pinned':'left', 'filter': 'true', 'hide':'true'}, #auto
        {'headerName': 'Round', 'field': 'Round', 'width':80, 'pinned':'left', 'filter': 'true', 'hide':'true'}, #80
        {'headerName': 'School', 'field': 'School', 'width':180, 'pinned':'left', 'filter': 'true'}, #auto
        {'headerName': 'Class', 'field': 'Class', 'width':70, 'pinned':'left', 'filter': 'true', 'hide':'true', "cellStyle": {"border-right": "4px solid #FF0000"}}, #70
        
        {'headerName': 'Music Ind.', 'field': 'MPI', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"textAlign": "center"}, "headerClass": "custom-header", 
         "valueGetter": "data.MPI.toFixed(3) + '  (' + data.MPI_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MPI - nodeB.data.MPI; }"},
        {'headerName': 'Music Ens.', 'field': 'MPE', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"textAlign": "center"}, "headerClass": "custom-header",
         "valueGetter": "data.MPE.toFixed(3) + '  (' + data.MPE_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MPE - nodeB.data.MPE; }"},     
        {'headerName': 'Music Average', 'field': 'Mus_Avg', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"textAlign": "center", "border-right": "4px solid #FF0000"}, 
         "headerClass": "custom-header", "valueGetter": "data.Mus_Avg.toFixed(3) + '  (' + data.Mus_Avg_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Mus_Avg - nodeB.data.Mus_Avg; }"},
        
        {'headerName': 'Visual Ind.', 'field': 'VPI', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center"},
         "valueGetter": "data.VPI.toFixed(3) + '  (' + data.VPI_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VPI - nodeB.data.VPI; }"},
        {'headerName': 'Visual Ens.', 'field': 'VPE', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center"},
         "valueGetter": "data.VPE.toFixed(3) + '  (' + data.VPE_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VPE - nodeB.data.VPE; }"},     
        {'headerName': 'Visual Average', 'field': 'Vis_Avg', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center", "border-right": "4px solid #FF0000"},
         "valueGetter": "data.Vis_Avg.toFixed(3) + '  (' + data.Vis_Avg_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Vis_Avg - nodeB.data.Vis_Avg; }"},

        {'headerName': 'Music GE1', 'field': 'MGE1', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center"},
         "valueGetter": "data.MGE1.toFixed(3) + '  (' + data.MGE1_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MGE1 - nodeB.data.MGE1; }"},
        {'headerName': 'Music GE2', 'field': 'MGE2', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center"},
         "valueGetter": "data.MGE2.toFixed(3) + '  (' + data.MGE2_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VPE - nodeB.data.VPE; }"},     
        {'headerName': 'Music GE Total', 'field': 'MGE_Tot', 'width':100, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center", "border-right": "4px solid #FF0000"},
         "valueGetter": "data.MGE_Tot.toFixed(3) + '  (' + data.MGE_Tot_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.MGE_Tot - nodeB.data.MGE_Tot; }"},

        {'headerName': 'Visual GE', 'field': 'VGE', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center"},
         "valueGetter": "data.VGE.toFixed(3) + '  (' + data.VGE_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.VGE - nodeB.data.VGE; }"},
        {'headerName': 'GE Total', 'field': 'GE_Tot', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center", "border-right": "4px solid #FF0000"},
         "valueGetter": "data.GE_Tot.toFixed(3) + '  (' + data.GE_Tot_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.GE_Tot - nodeB.data.GE_Tot; }"},

        {'headerName': 'Subtotal', 'field': 'Subtotal', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center"},
         "valueGetter": "data.Subtotal.toFixed(3) + '  (' + data.Subtotal_Rank + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Subtotal - nodeB.data.Subtotal; }"},
        
        {'headerName': 'Pen.', 'field': 'Pen', 'width':65, 'wrapHeaderText': 'true', 'valueFormatter': 'x.toFixed(1)', 'sortable':True, "cellStyle": {"text-align": "center"}},
        
         {'headerName': 'Total', 'field': 'Total', 'width':90, 'wrapHeaderText': 'true', "cellStyle": {"text-align": "center"},
         "valueGetter": "data.Total.toFixed(3) + '  (' + data.Place_Overall + ')'",  # Combine Score and Rank into one string
         "sortable": True,
         "sortComparator": "function(a, b, nodeA, nodeB, isInverted) { return nodeA.data.Total - nodeB.data.Total; }"},

        {'headerName': 'Place: Class', 'field': 'Place_Class', 'width':70, 'valueFormatter': 'x.toFixed(0)', 'wrapHeaderText': 'true', 'sortable':True, 
         'hide':'true', "cellStyle": {"text-align": "center"}},

        
        
         
        
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
if round is "Finals":
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

grid_table = AgGrid(display, 
                    gridOptions=gridOptions,
                    fit_columns_on_grid_load=False,
                    theme="streamlit",
                    enable_enterprise_modules=False,
                    enable_pagination=True,
                    fit_columns=False,
                    use_container_width=False,
                    #height=600
                    #style={'width': '100%', 'height': '500px'}
                   )


# styled_df = display.style.set_properties(**{'text-align': 'center'})
# st.write(styled_df.to_html(index=False, justify='center'), unsafe_allow_html=True)


# [theme]
# primaryColor="#bf2a25"
# backgroundColor="#e6e6e6"
# secondaryBackgroundColor="#ffffff"
# textColor="#11364d"


