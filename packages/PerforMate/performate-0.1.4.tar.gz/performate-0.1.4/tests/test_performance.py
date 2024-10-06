from trackers.performance import PerforMate
from trackers.export import ExportService
import time,random,logging
# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
max_ = 10
def main():
   # Initialize PiTrack
    tracker = PerforMate("MyApp")

    # Start a section and simulate work
    section = tracker.start_section("Data Processing")
    
    time.sleep(random.randint(1, max_))
    subsec =section.add_subsection("Load Data")
    time.sleep(random.randint(1, max_))
    subsec.end_subsection("Load Data")
    
    time.sleep(random.randint(1, max_))
    subsec2 =section.add_subsection("Read File")
    time.sleep(random.randint(1, max_))
    subsec2.end_subsection("Read File")
    
    time.sleep(random.randint(1, max_))
    subsec3 =section.add_subsection("Fetch Data")
    time.sleep(random.randint(1, max_))
    subsec3.end_subsection("Fetch Data")
    
    tracker.end_section("Data Processing")

    # Start another section
    section = tracker.start_section("Model Training")
    time.sleep(random.randint(1, max_))
    subsec2 =section.add_subsection("Test Data")
    time.sleep(random.randint(1, max_))
    subsec2.end_subsection("Test Data")
    
    tracker.end_section("Model Training")


i=0
while i<1:
    main()
    i+=1
    
tracker = PerforMate("MyApp")
  # Plot the time spent in each section
tracker.plot_histogram_stats()
tracker.plot_pie_chart()

# x = tracker.detect_anomalies_in_sections()
# print(x)

class GetDataService(ExportService):
    def send_data(self, data):
        print(data)

tracker.plot_subsections("Data Processing")
# tracker.dump_to_service(GetDataService())
anomalous_subsections = tracker.detect_anomalies_in_sections(threshold=3, subsections=True)
print(f"Anomalous subsections: {anomalous_subsections}")
