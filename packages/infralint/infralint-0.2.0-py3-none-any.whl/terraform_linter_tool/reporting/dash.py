import json
import logging

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dash_table, dcc, html

logger = logging.getLogger()
# Sidebar styles - reducing the width to make more space for the table
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",  # Reduced sidebar width
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Content styles - ensuring the content uses the remaining space
CONTENT_STYLE = {
    "margin-left": "12rem",  # Adjusted to match the reduced sidebar width
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


class DashDashboard:
    def __init__(self, report_path, base_directory):
        self.app = dash.Dash(
            __name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True
        )
        self.base_directory = base_directory
        self.report_path = report_path
        self.linter_data = []

        # Load the report data
        self.load_report()

    def load_report(self):
        """Load the linting report data from the report path."""
        with open(self.report_path, 'r') as file:
            report = json.load(file)
            for linter_name, linter_results in report.get('linters', {}).items():
                for issue in linter_results:
                    self.linter_data.append(issue)

    def create_sidebar(self):
        """Create a sidebar for navigating between linters."""
        enabled_linters = list(set([entry['Linter'] for entry in self.linter_data]))
        links = [dbc.NavLink(linter, href=f"/{linter.lower()}", active="exact") for linter in enabled_linters]
        return html.Div(
            [
                html.H2("Linters", className="display-4"),
                html.Hr(),
                dbc.Nav(links, vertical=True, pills=True),
            ],
            style=SIDEBAR_STYLE,
        )

    def run(self):
        """Define the layout and run the Dash application."""
        # Create a DataFrame from the linter data for dynamic display
        df = pd.DataFrame(self.linter_data)
        if df is None:
            logger.error("No data to display")
            return

        # Define app layout
        self.app.layout = html.Div([
            dcc.Location(id="url"),
            self.create_sidebar(),
            html.Div(id="page-content", style=CONTENT_STYLE),
        ])

        # Callback to filter data based on the selected linter
        @self.app.callback(
            Output('page-content', 'children'),
            Input('url', 'pathname')
        )
        def display_page(pathname):
            if pathname == "/":
                return self.render_home_page()
            elif pathname == "/tflint":
                return self.render_linter_page('TFLint')
            elif pathname == "/tfsec":
                return self.render_linter_page('TFSec')
            elif pathname == "/checkov":
                return self.render_linter_page('Checkov')
            else:
                return html.Div("404: Not found", className="text-danger")

        # Callback to update URL when pie chart section is clicked
        @self.app.callback(
            Output('url', 'pathname'),
            Input('pie-chart', 'clickData')  # <-- Listens to pie chart click event
        )
        def navigate_on_click(clickData):
            if clickData:
                linter_name = clickData['points'][0]['label']
                return f'/{linter_name.lower()}'
            return '/'

        # Run the Dash server
        self.app.run_server(debug=True)

    def render_home_page(self):
        """Render a summary page with a pie chart of total issues from both linters."""
        df = pd.DataFrame(self.linter_data)

        # Group data by linter and count the number of issues
        issue_counts = df.groupby('Linter').size().reset_index(name='Count')

        # Create a pie chart for issue distribution
        fig = px.pie(
            issue_counts,
            names='Linter',
            values='Count',
            title="Total Issues by Linter",
            hole=0.3  # Add a donut shape to help improve readability
        )

        return html.Div([
            dcc.Graph(id='pie-chart', figure=fig),
            html.H2("Click on a section to view detailed issues.", style={'text-align': 'center', 'margin-top': '20px'})
        ])

    def render_linter_page(self, linter_name):
        """Render the page for a specific linter."""
        df = pd.DataFrame([d for d in self.linter_data if d['Linter'] == linter_name])

        if df.empty:
            return html.P(f"No data for {linter_name}.")

        # Sort by Severity in descending order
        severity_order = {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 1}
        df['SeveritySort'] = df['Severity'].map(severity_order)
        df = df.sort_values(by='SeveritySort', ascending=False).drop(columns=['SeveritySort'])

        # Fill NaN/None values to avoid rendering issues
        df = df.fillna('')

        # Safely handle the 'Context' column only for Checkov
        if linter_name == 'Checkov':
            if 'Context' in df.columns:
                df['Context'] = df['Context'].apply(lambda context: context.replace('Summary:', '').strip())
        else:
            df['Context'] = ''  # Leave Context blank for TFLint and TFSec

        # Convert Links from list to Markdown string
        if 'Links' in df.columns:
            df['Links'] = df['Links'].apply(lambda links: ', '.join([f'[{link}]({link})' for link in links]))

        # Define the columns to be displayed dynamically based on the linter
        columns = [
            {"name": "File", "id": "File"},
            {"name": "Line", "id": "Line"},
            {"name": "Description", "id": "Description"},
            {"name": "Severity", "id": "Severity"},
            {"name": "Context", "id": "Context"} if linter_name == 'Checkov' else None,
            {"name": "Links", "id": "Links", "presentation": "markdown"}
        ]
        columns = [col for col in columns if col is not None]  # Filter out None columns

        # Style updates for hover-over, truncation, and wider columns
        table = dash_table.DataTable(
            id='linting-table',
            columns=columns,  # Dynamic columns
            data=df.to_dict('records'),
            filter_action="native",  # Enable column filtering
            sort_action="native",  # Enable column sorting
            style_cell={
                'whiteSpace': 'normal',  # Allow text to wrap in all cells
                'height': 'auto',  # Auto height adjustment
                'textAlign': 'left',  # Align text to left
                'maxWidth': '120px',  # Ensure lines break if going above 120px
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_data_conditional=[
                {'if': {'filter_query': '{Severity} = "CRITICAL"'}, 'backgroundColor': '#FF6F61', 'color': 'white'},
                {'if': {'filter_query': '{Severity} = "HIGH"'}, 'backgroundColor': '#FFA07A', 'color': 'white'},
                {'if': {'filter_query': '{Severity} = "MEDIUM"'}, 'backgroundColor': '#FFD700', 'color': 'black'},
                {'if': {'filter_query': '{Severity} = "LOW"'}, 'backgroundColor': '#90EE90', 'color': 'black'},
            ],
            style_table={
                'overflowX': 'auto',  # Allow table scrolling if needed
                'minWidth': '100%',  # Ensure table takes up full width
            },
        )
        # Pie chart for issue severity distribution
        fig = px.pie(df, names='Severity', title=f'{linter_name} Severity Distribution', color='Severity', color_discrete_map={
            'CRITICAL': '#FF6F61',  # Light Coral
            'HIGH': '#FFA07A',  # Light Salmon
            'MEDIUM': '#FFD700',  # Light Yellow
            'LOW': '#90EE90',  # Light Green
        })
        return html.Div([
            html.H1(f"{linter_name} Linting Results", style={
                'font-size': '1.75em',
                'font-weight': '600',
                'color': '#212529',
                'text-align': 'center',
                'margin-top': '20px',
                'margin-bottom': '15px',
                'border-bottom': '2px solid #6c757d',
                'padding-bottom': '10px',
                'font-family': '"Helvetica Neue", Helvetica, Arial, sans-serif'
            }),
            table,
            dcc.Graph(figure=fig),
        ])


if __name__ == '__main__':
    dashboard = DashDashboard(report_path="path/to/report.json", base_directory="path/to/base/directory")
    dashboard.run()
