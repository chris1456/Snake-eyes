from dash import Input, Output, State, no_update, html, dcc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.exceptions import PreventUpdate

def get_mode(x):
    values, counts = np.unique(x, return_counts=True)
    return values[np.argmax(counts)]

def register_callbacks(app):

        @app.callback(
            Output("Dropdown_var_2", "options"),
            Output("Dropdown_var_2", "value"),
            Input("Dropdown_var_1", "value")
        )
        def update_second_dropdown(number_dice):

            if number_dice is None:
                return [], None

            number_dice = int(number_dice)
            possible_values = list(range(number_dice, number_dice * 6 + 1))

            options = [
                {"label": value, "value": value}
                for value in possible_values
            ]

            return options, possible_values[0]

        @app.callback(
            Output("freq_table", "data"),
            Output("freq_table", "columns"),
            Output("summary_table", "data"),
            Output("summary_table", "columns"),
            Output("hist_plot", "figure"),
            Output("selected_number_text", "children"),
            Output("download_freq_btn", "disabled"),
            Output("download_summary_btn", "disabled"),
            Input("run_sim", "n_clicks"),
            State("Dropdown_var_1", "value"),
            State("Dropdown_var_2", "value"),
            State("n_sim", "value")
        )
        def run_dice_simulation(n_clicks, number_dice, selected_number, simulations):

            if not n_clicks:
                if not n_clicks:
                    return [], [], [], [], {}, "", True, True

            if number_dice is None or selected_number is None or simulations is None:
                return [], [], [], [], {}, "", True, True

            number_dice = int(number_dice)
            selected_number = int(selected_number)
            simulations = int(simulations)

            total_numb = np.zeros(simulations, dtype=int)

            for _ in range(number_dice):
                launches = np.random.randint(1, 7, size=simulations)
                total_numb += launches

            freq_table = (
                pd.Series(total_numb)
                .value_counts()
                .sort_index()
                .reset_index()
            )

            freq_table.columns = ["Number", "Frequency"]

            freq_table["Percentage"] = (
                    (freq_table["Frequency"] / simulations * 100)
                    .round(4)
                    .astype(str) + "%"
            )

            summary_table = pd.DataFrame({
                "Mean": [round(np.mean(total_numb), 2)],
                "SD": [round(np.std(total_numb, ddof=1), 2)],
                "Mode": [round(get_mode(total_numb), 2)],
                "Median": [round(np.median(total_numb), 2)]
            })

            freq_columns = [
                {"name": col, "id": col}
                for col in freq_table.columns
            ]

            summary_columns = [
                {"name": col, "id": col}
                for col in summary_table.columns
            ]

            fig = px.histogram(
                x=total_numb,
                title="Distribution of Dice Sum",
                labels={"x": "Sum of Dice", "y": "Frequency"}
            )

            fig.add_vline(
                x=selected_number,
                line_width=4,
                line_color="#DC143C"
            )

            fig.update_layout(
                plot_bgcolor="#f2f2f2",
                paper_bgcolor="#f2f2f2"
            )

            selected_row = freq_table[
                freq_table["Number"] == selected_number
                ]

            if selected_row.empty:
                selected_text = ""

            else:
                selected_frequency = selected_row["Frequency"].iloc[0]
                selected_percentage = selected_row["Percentage"].iloc[0]

                selected_text = html.Div([

                    html.B("Votre nombre sélectionné "),
                    f"{selected_number} ",

                    html.B("apparaît "),
                    f"{selected_frequency} ",

                    html.B("fois "),
                    f"({selected_percentage})."

                ])

            return (
                freq_table.to_dict("records"),
                freq_columns,
                summary_table.to_dict("records"),
                summary_columns,
                fig,
                selected_text,
                False,
                False
            )

        @app.callback(
            Output("download_freq_csv", "data"),
            Input("download_freq_btn", "n_clicks"),
            State("freq_table", "data"),
            prevent_initial_call=True
        )
        def download_frequency_table(n_clicks, data):

            df = pd.DataFrame(data)

            return dcc.send_data_frame(
                df.to_csv,
                "frequency_table.csv",
                index=False
            )

        @app.callback(
            Output("download_summary_csv", "data"),
            Input("download_summary_btn", "n_clicks"),
            State("summary_table", "data"),
            prevent_initial_call=True
        )
        def download_summary_table(n_clicks, data):

            df = pd.DataFrame(data)

            return dcc.send_data_frame(
                df.to_csv,
                "summary_table.csv",
                index=False
            )

        @app.callback(
            Output("freq_table_coins", "data"),
            Output("freq_table_coins", "columns"),
            Output("summary_table_coins", "data"),
            Output("summary_table_coins", "columns"),
            Output("hist_plot_coins", "figure"),

            Input("run_sim_coin", "n_clicks"),

            State("Dropdown_coin_2", "value"),
            State("n_sim_2", "value")
        )
        def update_coin_simulation(n_clicks, number_heads, n_sim):

            if n_clicks == 0:
                raise PreventUpdate

            number_heads = int(number_heads)
            n_sim = int(n_sim)

            total_flips = []

            for _ in range(n_sim):
                n_heads = 0
                attempts = 0

                while n_heads < number_heads:
                    toss = np.random.binomial(1, 0.5)
                    attempts += 1
                    n_heads += toss

                total_flips.append(attempts)

            x = np.array(total_flips)

            freq_df = (
                pd.Series(x)
                .value_counts()
                .sort_index()
                .reset_index()
            )

            freq_df.columns = ["Attempts", "Frequency"]
            freq_df["Percentage"] = (
                                            freq_df["Frequency"] / len(x) * 100
                                    ).round(4).astype(str) + "%"

            summary_df = pd.DataFrame({
                "Mean": [round(np.mean(x), 2)],
                "SD": [round(np.std(x, ddof=1), 2)],
                "Mode": [round(get_mode(x), 2)],
                "Median": [round(np.median(x), 2)]
            })

            fig = px.histogram(
                x=x,
                labels={
                    "x": "Number of Tosses Needed",
                    "y": "Frequency"
                },
                title=f"Tosses Needed to Get {number_heads} Heads"
            )

            mean_x = np.mean(x)
            median_x = np.median(x)

            fig.add_vline(
                x=mean_x,
                line_width=3,
                line_dash="dash",
                line_color="#DC143C",
                annotation_text=f"Mean: {round(mean_x, 2)}",
                annotation_position="top right"
            )

            fig.add_vline(
                x=median_x,
                line_width=3,
                line_dash="dot",
                line_color="#2E8B57",
                annotation_text=f"Median: {round(median_x, 2)}",
                annotation_position="top left"
            )

            fig.update_layout(
                plot_bgcolor="#f2f2f2",
                paper_bgcolor="#f2f2f2"
            )

            freq_columns = [
                {"name": col, "id": col}
                for col in freq_df.columns
            ]

            summary_columns = [
                {"name": col, "id": col}
                for col in summary_df.columns
            ]

            return (
                freq_df.to_dict("records"),
                freq_columns,
                summary_df.to_dict("records"),
                summary_columns,
                fig
            )