import os
import time
import logging
from tinydb import TinyDB
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime



class PerforMate:
    class _Section:
        """Internal class for managing sections and subsections."""
        def __init__(self, section_name):
            """Initialize a section with subsections."""
            self.section_name = section_name
            self.start_time = time.time()
            self.end_time = None
            self.subsections = {}
            logging.info(f"Section '{section_name}' started.")

        def add_subsection(self, subsection_name):
            """Add a subsection to the section."""
            self.subsections[subsection_name] = {
                'start_time': time.time(),
                'end_time': None
            }
            logging.info(f"Subsection '{subsection_name}' added to section '{self.section_name}'.")
            return self

        def end_subsection(self, subsection_name):
            """End a subsection by calculating time spent."""
            if subsection_name in self.subsections:
                self.subsections[subsection_name]['end_time'] = time.time()
                self.subsections[subsection_name]['time_spent'] = (
                    self.subsections[subsection_name]['end_time'] - 
                    self.subsections[subsection_name]['start_time']
                )
                logging.info(f"Subsection '{subsection_name}' in section '{self.section_name}' ended. "
                             f"Time spent: {self.subsections[subsection_name]['time_spent']} seconds.")
            else:
                logging.error(f"Subsection '{subsection_name}' does not exist in section '{self.section_name}'.")
                raise ValueError(f"Subsection '{subsection_name}' does not exist.")
        
        def end_section(self):
            """End the main section."""
            self.end_time = time.time()
            self.time_spent = self.end_time - self.start_time
            logging.info(f"Section '{self.section_name}' ended. Total time: {self.time_spent} seconds.")
            return self

    def __init__(self, app_name, db_path='/tmp/pitrack/pitrack', row_threshold=50):
        """
        Initialize PiTrack instance with app name, optional db path, and row threshold.
        The database is stored at /tmp/pitrack/pitrack by default, with chunking when row_threshold is exceeded.
        """
        self.app_name = app_name
        self.sections = {}
        self.row_threshold = row_threshold
        self.db_path = db_path
        self.chunk_counter = 1
        self.current_db_file = f"{db_path}_{self.chunk_counter}.json"
        self.db = TinyDB(self.current_db_file)
        logging.info(f"PiTrack initialized for app '{app_name}'. Database path: {self.current_db_file}")

    def start_section(self, section_name):
        """Start a new section and return the section object."""
        try:
            section = self._Section(section_name)
            self.sections[section_name] = section
            return section
        except Exception as e:
            self.log_exception("start_section", e, verbose=True)

    def end_section(self, section_name):
        """End tracking for a section."""
        try:
            if section_name in self.sections:
                section = self.sections[section_name]
                section.end_section()
                timestamp = datetime.now().isoformat()
                self.save_results(section_name, section, timestamp)
            else:
                logging.error(f"Section '{section_name}' does not exist.")
                raise ValueError(f"Section '{section_name}' does not exist.")
        except Exception as e:
            self.log_exception("end_section", e, verbose=True)

    def save_results(self, section_name, section, timestamp):
        """Save the section and subsection timing results into TinyDB."""
        try:
            subsections_data = {}
            for subsection_name, subsection_data in section.subsections.items():
                subsections_data[subsection_name] = subsection_data.get('time_spent', 0)

            data = {
                'app_name': self.app_name,
                'section_name': section_name,
                'subsections': subsections_data,
                'total_time': section.time_spent,
                'timestamp': timestamp
            }

            # Check if we need to create a new chunk
            if len(self.db) >= self.row_threshold:
                self.chunk_counter += 1
                self.current_db_file = f"{self.db_path}_{self.chunk_counter}.json"
                self.db = TinyDB(self.current_db_file)
                logging.info(f"New chunk created: {self.current_db_file}")

            self.db.insert(data)
            logging.info(f"Results saved for section '{section_name}'.")
        except Exception as e:
            self.log_exception("save_results", e, verbose=True)

    def _load_all_data(self):
        """Helper function to load data from all chunked files."""
        try:
            all_data = []
            for chunk in range(1, self.chunk_counter + 1):
                chunk_file = f"{self.db_path}_{chunk}.json"
                if os.path.exists(chunk_file):
                    db_chunk = TinyDB(chunk_file)
                    all_data.extend(db_chunk.all())
            logging.info(f"Loaded data from all chunks.")
            return all_data
        except Exception as e:
            self.log_exception("_load_all_data", e, verbose=True)

    def log_exception(self, location, exception, verbose=False):
        """Log exceptions and capture as a subsection."""
        # Create an exception subsection in the current section
        current_section = None
        if len(self.sections) > 0:
            current_section = list(self.sections.values())[-1]
        
        if current_section:
            current_section.add_subsection(f"Exception in {location}")
            current_section.end_subsection(f"Exception in {location}")

        # Log the exception with verbosity control
        if verbose:
            logging.exception(f"Exception occurred in {location}: {exception}")
        else:
            logging.error(f"Exception in {location}: {exception}")

    def summarize_results(self):
        """Summarize the results into a DataFrame, loading data from all chunked files."""
        try:
            results = self._load_all_data()

            if not results:
                logging.warning("No results found.")
                return None

            # Flatten the results for pandas
            summary_data = {
                'app_name': [],
                'section': [],
                'subsection': [],
                'time_spent': [],
                'timestamp': []
            }
            for result in results:
                for subsection, time_spent in result['subsections'].items():
                    summary_data['app_name'].append(result['app_name'])
                    summary_data['section'].append(result['section_name'])
                    summary_data['subsection'].append(subsection)
                    summary_data['time_spent'].append(time_spent)
                    summary_data['timestamp'].append(result['timestamp'])

                summary_data['app_name'].append(result['app_name'])
                summary_data['section'].append(result['section_name'])
                summary_data['subsection'].append(None)
                summary_data['time_spent'].append(result['total_time'])
                summary_data['timestamp'].append(result['timestamp'])

            df = pd.DataFrame(summary_data)
            logging.info("Results summarized.")
            return df
        except Exception as e:
            self.log_exception("summarize_results", e, verbose=True)
            
    def plot_histogram_stats(self):
        """Plot a histogram showing the mean, median, and mode of time spent for each section."""
        try:
            df = self.summarize_results()
            if df is not None:
                # Ensure we're only using relevant numeric data (time_spent)
                section_df = df[df['subsection'].isnull()]  # Focus on sections
                section_df = section_df[['section', 'time_spent']]  # Select only relevant columns
                
                # Convert 'time_spent' to numeric just in case there are any non-numeric values
                section_df['time_spent'] = pd.to_numeric(section_df['time_spent'], errors='coerce')

                # Drop NaN values that might have arisen from non-numeric conversions
                section_df.dropna(subset=['time_spent'], inplace=True)

                # Group by section and calculate mean, median, and mode per section
                section_stats = section_df.groupby('section').agg(
                    mean_time=('time_spent', 'mean'),
                    median_time=('time_spent', 'median'),
                    mode_time=('time_spent', lambda x: x.mode()[0] if not x.mode().empty else 0)
                ).reset_index()

                # Prepare data for plotting
                labels = section_stats['section']
                mean_values = section_stats['mean_time']
                median_values = section_stats['median_time']
                mode_values = section_stats['mode_time']

                # Plot the histogram with the mean, median, and mode for each section
                x = np.arange(len(labels))  # Label locations
                width = 0.1  # Width of the bars

                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Plot bars for mean, median, and mode
                ax.bar(x - width, mean_values, width, label='Mean', color='#73e6bb')
                ax.bar(x, median_values, width, label='Median', color='#ddd866')
                ax.bar(x + width, mode_values, width, label='Mode', color='#87e85b')

                # Add some text for labels, title, and custom x-axis tick labels
                ax.set_xlabel('Sections')
                ax.set_ylabel('Time (seconds)')
                ax.set_title(f'Mean, Median, and Mode of Time Spent per Section for {self.app_name}')
                ax.set_xticks(x)
                ax.set_xticklabels(labels, rotation=45)
                ax.legend()

                # Final adjustments and show plot
                plt.tight_layout()
                plt.show()
                logging.info("Histogram of mean, median, and mode per section generated.")
        except Exception as e:
            self.log_exception("plot_histogram_stats_per_section", e, verbose=True)
    def detect_anomalies_in_sections(self, threshold=3, subsections=False):
        """
        Detect anomalies in section or subsection time data using Z-Score.
        
        Args:
        - tracker (PiTrack object): An instance of the PiTrack object to analyze.
        - threshold (float): The Z-score threshold to flag anomalies. Default is 3 (99.7% confidence interval).
        - subsections (bool): Whether to detect anomalies in subsections. Default is False (sections).
        
        Returns:
        - list: A list of section or subsection names where anomalies were detected.
        """
        df = self.summarize_results()
        if df is None:
            print("No data available for analysis.")
            return []

        # Filter data for sections or subsections
        if subsections:
            data_df = df[df['subsection'].notnull()].copy()  # Explicitly create a copy
            group_column = 'subsection'
        else:
            data_df = df[df['subsection'].isnull()].copy()  # Explicitly create a copy
            group_column = 'section'

        # Ensure we have only numeric time_spent values, using .loc to avoid SettingWithCopyWarning
        data_df.loc[:, 'time_spent'] = pd.to_numeric(data_df['time_spent'], errors='coerce')
        
        # Drop NaN values that might have arisen from non-numeric conversions
        data_df.dropna(subset=['time_spent'], inplace=True)

        # Detect anomalies using Z-Score
        anomalies = []
        mean = np.mean(data_df['time_spent'])
        std_dev = np.std(data_df['time_spent'])

        for _, row in data_df.iterrows():
            z_score = (row['time_spent'] - mean) / std_dev
            if np.abs(z_score) > threshold:
                r = {
                    'section': row[group_column],
                    'subsection': row['subsection'],
                    'time_spent': row['time_spent'],
                    'timestamp':row['timestamp'],
                    'z_score': z_score
                    
                }
                anomalies.append(r)
        
        return anomalies


    def plot_sections(self):
        """Plot the time spent on each section."""
        try:
            df = self.summarize_results()
            if df is not None:
                # Ensure we're only using relevant numeric data (time_spent) for plotting
                section_df = df[df['subsection'].isnull()]  # Ignore subsections, focus on sections
                section_df = section_df[['section', 'time_spent']]  # Select only relevant columns
                
                # Convert 'time_spent' to numeric just in case there are any non-numeric values
                section_df['time_spent'] = pd.to_numeric(section_df['time_spent'], errors='coerce')
                
                # Group by 'section' and sum the time spent in each section
                section_df = section_df.groupby('section').mean()

                # Plot the time spent in each section
                section_df.plot(kind='bar', figsize=(10, 6))
                plt.title(f"Time Spent in Each Section for App: {self.app_name}")
                plt.ylabel('Time (seconds)')
                plt.xlabel('Section')
                plt.tight_layout()
                plt.show()
                logging.info("Section plot generated.")
        except Exception as e:
            self.log_exception("plot_sections", e, verbose=True)
    def dump_to_service(self, export_service):
        """Export data using a custom export service."""
        data = self.summarize_results()
        if data is not None:
            export_service.send_data(data.to_dict(orient='records'))
        else:
            print("No data to export.")
    def plot_subsections(self, section_name):
        """Plot the time spent on subsections within a section."""
        try:
            df = self.summarize_results()
            if df is not None:
                # Filter the DataFrame to get only the relevant section and non-null subsections
                subsection_df = df[(df['section'] == section_name) & df['subsection'].notnull()]

                if subsection_df.empty:
                    logging.warning(f"No subsections found for section '{section_name}'")
                    return

                # Group by 'subsection' and sum the 'time_spent' for each subsection
                subsection_times = subsection_df.groupby('subsection')['time_spent'].mean()

                # Plot the time spent on subsections
                subsection_times.plot(kind='bar', figsize=(10, 6))
                plt.title(f"Time Spent on Subsections in Section: {section_name}")
                plt.ylabel('Time (seconds)')
                plt.xlabel('Subsection')
                plt.tight_layout()
                plt.show()
                logging.info(f"Subsection plot generated for section '{section_name}'.")
        except Exception as e:
            self.log_exception(f"plot_subsections: {section_name}", e, verbose=True)


    def plot_pie_chart(self):
        """Plot a pie chart to show the distribution of time spent across sections."""
        try:
            df = self.summarize_results()
            if df is not None:
                # Focus only on sections (ignore subsections)
                section_df = df[df['subsection'].isnull()]  # Filter to only sections
                
                # Group by 'section' and sum the 'time_spent' for each section
                section_times = section_df.groupby('section')['time_spent'].sum()

                # Generate pie chart
                section_times.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 8))
                plt.title(f"Time Distribution Across Sections for App - {self.app_name}")
                plt.ylabel('')  # Remove the y-label as it doesn't make sense for a pie chart
                plt.tight_layout()
                plt.show()
                logging.info("Pie chart generated.")
        except Exception as e:
            self.log_exception("plot_pie_chart", e, verbose=True)

    def get_subsection_data(self, section_name):
        """Retrieve data for all subsections within a section."""
        try:
            df = self.summarize_results()
            if df is not None:
                subsection_df = df[(df['section'] == section_name) & df['subsection'].notnull()]
                return subsection_df
        except Exception as e:
            self.log_exception(f"get_subsection_data: {section_name}", e, verbose=True)
        return None

    def delete(self):
        """Delete all chunked database files."""
        try:
            for chunk in range(1, self.chunk_counter + 1):
                chunk_file = f"{self.db_path}_{chunk}.json"
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
                    logging.info(f"Deleted {chunk_file}")
            logging.info("All chunked data files have been deleted.")
        except Exception as e:
            self.log_exception("delete", e, verbose=True)
