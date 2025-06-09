# 🚗 Turno Data Analysis

A comprehensive Python-based analysis tool for vehicle fleet data, focusing on battery performance, temporal patterns, and geographic distribution analysis.

## 📊 Overview

This project provides an end-to-end analysis solution for vehicle telemetry data, specifically designed for electric vehicle fleets. The analyzer processes CSV data containing vehicle information, battery charges, location data, and temporal patterns to generate actionable insights for fleet management.

## ✨ Features

- **📈 Comprehensive Data Analysis**: Battery performance, vehicle behavior, and fleet statistics
- **⏰ Temporal Pattern Analysis**: Hourly activity patterns and time-based insights
- **🌍 Geographic Analysis**: Location-based clustering and distribution mapping
- **🔋 Battery Health Monitoring**: Charge level analysis and efficiency tracking
- **📊 Rich Visualizations**: Six different chart types for data exploration
- **📁 Export Capabilities**: CSV reports and high-quality visualization exports
- **🛡️ Data Validation**: Robust error handling and data preprocessing

## 🔧 Installation

### Prerequisites

```bash
Python 3.7+
```

### Required Libraries

```bash
pip install pandas numpy matplotlib seaborn
```

Or install all dependencies at once:

```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
turno-analysis/
│
├── turno_analyzer.py          # Main analysis script
├── turno_data.csv            # Input data file (your dataset)
├── requirements.txt          # Python dependencies
├── README.md                # This file
│
└── outputs/                 # Generated files (auto-created)
    ├── turno_analysis_visualizations.png
    ├── turno_vehicle_summary.csv
    └── turno_hourly_summary.csv
```

## 📋 Data Format

Your CSV file should contain the following columns:

| Column | Description | Type |
|--------|-------------|------|
| `vin` | Vehicle Identification Number | String |
| `yearr` | Year | Integer |
| `mmm` | Month | Integer |
| `ddd` | Day | Integer |
| `hr` | Hour (0-23) | Integer |
| `half_hour` | Half-hour indicator | Integer |
| `avg_lat` | Average Latitude | Float |
| `avg_long` | Average Longitude | Float |
| `avg_bat_charge` | Average Battery Charge (%) | Float |

### Sample Data Format:
```csv
vin,yearr,mmm,ddd,hr,half_hour,avg_lat,avg_long,avg_bat_charge
VIN123456,2024,1,15,8,0,40.7128,-74.0060,85.5
VIN123456,2024,1,15,8,1,40.7130,-74.0058,84.2
```

## 🚀 Usage

### Basic Usage

```python
from turno_analyzer import TurnoDataAnalyzer

# Initialize the analyzer with your data file
analyzer = TurnoDataAnalyzer('turno_data.csv')

# Run complete analysis
results = analyzer.run_complete_analysis()
```

### Command Line Usage

```bash
python turno_analyzer.py
```

### Advanced Usage

```python
# Initialize analyzer
analyzer = TurnoDataAnalyzer('your_data.csv')

# Run individual analysis components
basic_stats = analyzer.basic_statistics()
vehicle_stats = analyzer.vehicle_analysis()
temporal_stats = analyzer.temporal_analysis()
geo_stats = analyzer.geographic_analysis()
battery_stats = analyzer.battery_analysis()

# Generate visualizations
analyzer.create_visualizations()

# Get insights and recommendations
insights = analyzer.generate_insights()

# Export summary reports
reports = analyzer.export_summary_report()
```

## 📊 Analysis Components

### 1. **Basic Statistics**
- Dataset overview and record counts
- Battery charge statistics (mean, median, std dev)
- Geographic coverage analysis
- Temporal pattern identification

### 2. **Vehicle Analysis**
- Individual vehicle performance metrics
- Battery usage consistency
- Activity level comparisons
- Fleet efficiency rankings

### 3. **Temporal Analysis**
- Hourly activity patterns
- Peak usage identification
- Time period categorization
- Battery performance by time

### 4. **Geographic Analysis**
- Location-based clustering
- Regional activity distribution
- Geographic battery performance
- Coverage area analysis

### 5. **Battery Analysis**
- Charge level distribution
- Critical battery alerts
- Performance patterns
- Efficiency recommendations

## 📈 Generated Outputs

### Visualizations
- **Battery Charge Distribution**: Histogram showing charge level patterns
- **Hourly Activity Pattern**: Bar chart of activity by hour
- **Battery Charge by Hour**: Line graph of charging patterns
- **Geographic Distribution**: Scatter plot with battery level overlay
- **Vehicle Activity Distribution**: Fleet usage patterns
- **Time Period Analysis**: Battery performance by time segments

### Reports
- **Vehicle Summary** (`turno_vehicle_summary.csv`): Per-vehicle statistics
- **Hourly Summary** (`turno_hourly_summary.csv`): Time-based patterns
- **Visualization Export** (`turno_analysis_visualizations.png`): High-res charts

## 💡 Key Insights Generated

- **Fleet Performance Metrics**: Overall fleet health and efficiency
- **Battery Management**: Charging patterns and low-battery alerts
- **Operational Optimization**: Peak hours and resource allocation
- **Geographic Insights**: Location-based performance patterns
- **Predictive Maintenance**: Battery degradation indicators

## 🛠️ Customization

### Modifying Analysis Parameters

```python
# Custom battery threshold for alerts
low_battery_threshold = 25  # Default: 30%

# Custom time period bins
time_bins = [0, 6, 12, 18, 24]
time_labels = ['Night', 'Morning', 'Afternoon', 'Evening']
```

### Adding Custom Visualizations

```python
def custom_visualization(self):
    # Add your custom plotting code here
    plt.figure(figsize=(10, 6))
    # Your visualization logic
    plt.savefig('custom_chart.png')
```

## 📚 Dependencies

```txt
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

## 🐛 Troubleshooting

### Common Issues

1. **File Not Found Error**
   ```
   Solution: Ensure 'turno_data.csv' is in the same directory as the script
   ```

2. **Missing Columns Error**
   ```
   Solution: Verify your CSV has all required columns with exact names
   ```

3. **Memory Issues with Large Datasets**
   ```
   Solution: Process data in chunks or increase system memory
   ```

### Error Handling

The analyzer includes comprehensive error handling for:
- Missing data files
- Invalid data formats
- Missing columns
- Data type inconsistencies

## 📋 Requirements.txt

```txt
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Thanks to the data science community for inspiration
- Built with Python, Pandas, and Matplotlib
- Designed for electric vehicle fleet management

---

## 📸 Screenshots

### Sample Visualization Output
![Screenshot 2025-06-09 103320](https://github.com/user-attachments/assets/f9d6f811-d3e3-4304-acc4-a098ff4e4d05)


### Console Output Example
```
🚀 STARTING COMPLETE TURNO DATA ANALYSIS
============================================================
🔄 STEP 1: LOADING DATA
--------------------------------------------------
✅ Dataset loaded successfully!
📊 Records: 10,000
📋 Columns: ['vin', 'yearr', 'mmm', 'ddd', 'hr', 'half_hour', 'avg_lat', 'avg_long', 'avg_bat_charge']

📊 STEP 2: BASIC STATISTICS
--------------------------------------------------
🗂️ DATASET OVERVIEW:
• Total records: 10,000
• Unique vehicles (VINs): 50
• Date range: 2024-2024
• Time span: 0:00 - 23:00
```

---

**Happy Analyzing! 🚗⚡📊**
