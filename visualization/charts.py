class ChartGenerator:
    def __init__(self, logger):
        self.logger = logger

    def generate_chart(self, data, chart_type, x_column, y_column, title, color_column=None):
        self.logger.info(f"Generating {chart_type} chart for {x_column} vs {y_column}")
        # Placeholder for chart generation logic
        return f"Chart: {chart_type} of {y_column} by {x_column}"

    def display_chart_in_streamlit(self, chart):
        import streamlit as st
        st.write(chart)