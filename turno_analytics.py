import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TurnoDataAnalyzer:
    def __init__(self, filename='turno_data.csv'):
        self.filename = filename
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and validate the turno dataset"""
        print("🔄 STEP 1: LOADING DATA")
        print("-" * 50)
        print(f"Attempting to load: {self.filename}")
        
        try:
            # Load the dataset
            self.df = pd.read_csv(self.filename)
            print("✅ Dataset loaded successfully!")
            print(f"📊 Records: {len(self.df):,}")
            print(f"📋 Columns: {list(self.df.columns)}")
            
            # Expected columns
            expected_columns = ['vin', 'yearr', 'mmm', 'ddd', 'hr', 'half_hour', 
                              'avg_lat', 'avg_long', 'avg_bat_charge']
            
            # Check for missing columns
            missing_columns = [col for col in expected_columns if col not in self.df.columns]
            if missing_columns:
                print(f"⚠️ Missing columns: {missing_columns}")
                return False
            
            # Data cleaning and preprocessing
            self.preprocess_data()
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: File '{self.filename}' not found")
            return False
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def preprocess_data(self):
        """Clean and preprocess the data"""
        print("\n🔧 PREPROCESSING DATA...")
        
        # Remove any duplicate records
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        if len(self.df) < initial_count:
            print(f"Removed {initial_count - len(self.df):,} duplicate records")
        
        # Handle missing values
        missing_data = self.df.isnull().sum()
        if missing_data.sum() > 0:
            print("⚠️ MISSING VALUES FOUND:")
            for col, count in missing_data[missing_data > 0].items():
                print(f"• {col}: {count:,} missing ({count/len(self.df)*100:.1f}%)")
            
            # Fill missing battery charges with median
            if 'avg_bat_charge' in missing_data and missing_data['avg_bat_charge'] > 0:
                median_charge = self.df['avg_bat_charge'].median()
                self.df['avg_bat_charge'].fillna(median_charge, inplace=True)
                print(f"Filled missing battery charges with median: {median_charge:.1f}%")
        
        # Create datetime column for time-based analysis
        try:
            # Assuming yearr is year, mmm is month, ddd is day
            self.df['date'] = pd.to_datetime(
                self.df[['yearr', 'mmm', 'ddd']].rename(columns={
                    'yearr': 'year', 'mmm': 'month', 'ddd': 'day'
                })
            )
            print("✅ Created datetime column for time analysis")
        except:
            print("⚠️ Could not create datetime column")
        
        # Create time periods for analysis
        self.df['time_period'] = pd.cut(self.df['hr'], 
                                       bins=[0, 6, 12, 18, 24], 
                                       labels=['Night', 'Morning', 'Afternoon', 'Evening'],
                                       include_lowest=True)
        
        print("✅ Data preprocessing completed")
    
    def basic_statistics(self):
        """Generate basic statistics about the dataset"""
        print("\n📊 STEP 2: BASIC STATISTICS")
        print("-" * 50)
        
        # Dataset overview
        print("🗂️ DATASET OVERVIEW:")
        print(f"• Total records: {len(self.df):,}")
        print(f"• Unique vehicles (VINs): {self.df['vin'].nunique():,}")
        print(f"• Date range: {self.df['yearr'].min()}-{self.df['yearr'].max()}")
        print(f"• Time span: {self.df['hr'].min()}:00 - {self.df['hr'].max()}:00")
        
        # Battery statistics
        print(f"\n🔋 BATTERY STATISTICS:")
        battery_stats = self.df['avg_bat_charge'].describe()
        print(f"• Mean charge: {battery_stats['mean']:.1f}%")
        print(f"• Median charge: {battery_stats['50%']:.1f}%")
        print(f"• Standard deviation: {battery_stats['std']:.1f}%")
        print(f"• Min charge: {battery_stats['min']:.1f}%")
        print(f"• Max charge: {battery_stats['max']:.1f}%")
        
        # Location statistics
        print(f"\n🌍 GEOGRAPHIC COVERAGE:")
        print(f"• Latitude range: {self.df['avg_lat'].min():.4f}° to {self.df['avg_lat'].max():.4f}°")
        print(f"• Longitude range: {self.df['avg_long'].min():.4f}° to {self.df['avg_long'].max():.4f}°")
        print(f"• Geographic center: ({self.df['avg_lat'].mean():.4f}°, {self.df['avg_long'].mean():.4f}°)")
        
        # Temporal patterns
        print(f"\n⏰ TEMPORAL PATTERNS:")
        hourly_counts = self.df['hr'].value_counts().sort_index()
        peak_hour = hourly_counts.idxmax()
        print(f"• Peak activity hour: {peak_hour}:00 ({hourly_counts[peak_hour]:,} records)")
        print(f"• Lowest activity hour: {hourly_counts.idxmin()}:00 ({hourly_counts.min():,} records)")
        
        return battery_stats
    
    def vehicle_analysis(self):
        """Analyze vehicle-specific patterns"""
        print("\n🚗 STEP 3: VEHICLE ANALYSIS")
        print("-" * 50)
        
        # Vehicle activity patterns
        vehicle_stats = self.df.groupby('vin').agg({
            'avg_bat_charge': ['mean', 'std', 'min', 'max', 'count'],
            'avg_lat': 'std',
            'avg_long': 'std'
        }).round(2)
        
        vehicle_stats.columns = ['avg_charge', 'charge_std', 'min_charge', 'max_charge', 
                               'records_count', 'lat_mobility', 'long_mobility']
        
        print(f"📈 VEHICLE ACTIVITY SUMMARY:")
        print(f"• Most active vehicle: {vehicle_stats['records_count'].idxmax()} ({vehicle_stats['records_count'].max():,} records)")
        print(f"• Least active vehicle: {vehicle_stats['records_count'].idxmin()} ({vehicle_stats['records_count'].min():,} records)")
        print(f"• Average records per vehicle: {vehicle_stats['records_count'].mean():.0f}")
        
        print(f"\n🔋 BATTERY BEHAVIOR BY VEHICLE:")
        print(f"• Vehicle with highest avg charge: {vehicle_stats['avg_charge'].idxmax()} ({vehicle_stats['avg_charge'].max():.1f}%)")
        print(f"• Vehicle with lowest avg charge: {vehicle_stats['avg_charge'].idxmin()} ({vehicle_stats['avg_charge'].min():.1f}%)")
        print(f"• Most consistent battery usage: {vehicle_stats['charge_std'].idxmin()} (std: {vehicle_stats['charge_std'].min():.1f}%)")
        
        return vehicle_stats
    
    def temporal_analysis(self):
        """Analyze temporal patterns in the data"""
        print("\n📅 STEP 4: TEMPORAL ANALYSIS")
        print("-" * 50)
        
        # Hourly patterns
        hourly_stats = self.df.groupby('hr').agg({
            'avg_bat_charge': 'mean',
            'vin': 'count'
        }).round(2)
        hourly_stats.columns = ['avg_battery', 'activity_count']
        
        print("⏰ HOURLY PATTERNS:")
        peak_hours = hourly_stats['activity_count'].nlargest(3)
        for hour, count in peak_hours.items():
            avg_battery = hourly_stats.loc[hour, 'avg_battery']
            print(f"• {hour}:00 - {count:,} records (avg battery: {avg_battery:.1f}%)")
        
        # Time period analysis
        if 'time_period' in self.df.columns:
            period_stats = self.df.groupby('time_period').agg({
                'avg_bat_charge': 'mean',
                'vin': 'count'
            }).round(2)
            
            print(f"\n🌅 TIME PERIOD ANALYSIS:")
            for period in period_stats.index:
                count = period_stats.loc[period, 'vin']
                battery = period_stats.loc[period, 'avg_bat_charge']
                print(f"• {period}: {count:,} records (avg battery: {battery:.1f}%)")
        
        return hourly_stats
    
    def geographic_analysis(self):
        """Analyze geographic patterns"""
        print("\n🗺️ STEP 5: GEOGRAPHIC ANALYSIS")
        print("-" * 50)
        
        # Calculate geographic clusters (simplified)
        lat_bins = pd.cut(self.df['avg_lat'], bins=5, labels=['South', 'South-Mid', 'Central', 'North-Mid', 'North'])
        long_bins = pd.cut(self.df['avg_long'], bins=5, labels=['West', 'West-Mid', 'Central', 'East-Mid', 'East'])
        
        # Geographic distribution
        geo_stats = self.df.groupby([lat_bins, long_bins]).agg({
            'avg_bat_charge': 'mean',
            'vin': ['count', 'nunique']
        }).round(2)
        
        print("🌍 GEOGRAPHIC DISTRIBUTION:")
        top_regions = geo_stats[('vin', 'count')].nlargest(5)
        for (lat_region, long_region), count in top_regions.items():
            avg_battery = geo_stats.loc[(lat_region, long_region), ('avg_bat_charge', 'mean')]
            unique_vehicles = geo_stats.loc[(lat_region, long_region), ('vin', 'nunique')]
            print(f"• {lat_region}-{long_region}: {count:,} records, {unique_vehicles} vehicles (avg battery: {avg_battery:.1f}%)")
        
        return geo_stats
    
    def battery_analysis(self):
        """Detailed battery charge analysis"""
        print("\n🔋 STEP 6: BATTERY CHARGE ANALYSIS")
        print("-" * 50)
        
        # Battery charge distribution
        charge_ranges = pd.cut(self.df['avg_bat_charge'], 
                             bins=[0, 20, 40, 60, 80, 100], 
                             labels=['Critical (0-20%)', 'Low (20-40%)', 'Medium (40-60%)', 
                                   'Good (60-80%)', 'Full (80-100%)'])
        
        charge_distribution = charge_ranges.value_counts()
        print("📊 BATTERY CHARGE DISTRIBUTION:")
        for range_name, count in charge_distribution.items():
            percentage = (count / len(self.df)) * 100
            print(f"• {range_name}: {count:,} records ({percentage:.1f}%)")
        
        # Battery patterns by hour
        battery_by_hour = self.df.groupby('hr')['avg_bat_charge'].mean()
        peak_battery_hour = battery_by_hour.idxmax()
        lowest_battery_hour = battery_by_hour.idxmin()
        
        print(f"\n⚡ BATTERY PATTERNS BY TIME:")
        print(f"• Highest avg battery at {peak_battery_hour}:00 ({battery_by_hour[peak_battery_hour]:.1f}%)")
        print(f"• Lowest avg battery at {lowest_battery_hour}:00 ({battery_by_hour[lowest_battery_hour]:.1f}%)")
        
        return charge_distribution, battery_by_hour
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print("\n📈 STEP 7: CREATING VISUALIZATIONS")
        print("-" * 50)
        
        # Set up the plotting area
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Battery charge distribution
        plt.subplot(2, 3, 1)
        self.df['avg_bat_charge'].hist(bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.axvline(self.df['avg_bat_charge'].mean(), color='red', linestyle='--', label=f'Mean: {self.df["avg_bat_charge"].mean():.1f}%')
        plt.xlabel('Average Battery Charge (%)')
        plt.ylabel('Frequency')
        plt.title('Battery Charge Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. Hourly activity pattern
        plt.subplot(2, 3, 2)
        hourly_counts = self.df['hr'].value_counts().sort_index()
        hourly_counts.plot(kind='bar', color='lightcoral', alpha=0.8)
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Records')
        plt.title('Activity Pattern by Hour')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # 3. Battery charge by hour
        plt.subplot(2, 3, 3)
        battery_by_hour = self.df.groupby('hr')['avg_bat_charge'].mean()
        battery_by_hour.plot(kind='line', marker='o', color='green', linewidth=2, markersize=4)
        plt.xlabel('Hour of Day')
        plt.ylabel('Average Battery Charge (%)')
        plt.title('Battery Charge Pattern by Hour')
        plt.grid(True, alpha=0.3)
        
        # 4. Geographic scatter plot
        plt.subplot(2, 3, 4)
        scatter = plt.scatter(self.df['avg_long'], self.df['avg_lat'], 
                            c=self.df['avg_bat_charge'], cmap='RdYlGn', 
                            alpha=0.6, s=1)
        plt.colorbar(scatter, label='Battery Charge (%)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Geographic Distribution with Battery Levels')
        
        # 5. Vehicle activity distribution
        plt.subplot(2, 3, 5)
        vehicle_counts = self.df['vin'].value_counts()
        vehicle_counts.hist(bins=30, alpha=0.7, color='orange', edgecolor='black')
        plt.xlabel('Number of Records per Vehicle')
        plt.ylabel('Number of Vehicles')
        plt.title('Vehicle Activity Distribution')
        plt.grid(True, alpha=0.3)
        
        # 6. Time period analysis (if available)
        plt.subplot(2, 3, 6)
        if 'time_period' in self.df.columns:
            period_battery = self.df.groupby('time_period')['avg_bat_charge'].mean()
            period_battery.plot(kind='bar', color='purple', alpha=0.8)
            plt.xlabel('Time Period')
            plt.ylabel('Average Battery Charge (%)')
            plt.title('Battery Charge by Time Period')
            plt.xticks(rotation=45)
        else:
            # Alternative: Battery charge vs hour scatter
            plt.scatter(self.df['hr'], self.df['avg_bat_charge'], alpha=0.1, s=1)
            plt.xlabel('Hour')
            plt.ylabel('Battery Charge (%)')
            plt.title('Battery Charge vs Hour (Scatter)')
        
        plt.tight_layout()
        plt.savefig('turno_analysis_visualizations.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualizations created and saved as 'turno_analysis_visualizations.png'")
    
    def generate_insights(self):
        """Generate key insights and recommendations"""
        print("\n💡 STEP 8: KEY INSIGHTS & RECOMMENDATIONS")
        print("-" * 50)
        
        # Calculate key metrics
        avg_battery = self.df['avg_bat_charge'].mean()
        battery_std = self.df['avg_bat_charge'].std()
        low_battery_threshold = 30
        low_battery_records = len(self.df[self.df['avg_bat_charge'] < low_battery_threshold])
        
        peak_hour = self.df['hr'].value_counts().idxmax()
        unique_vehicles = self.df['vin'].nunique()
        total_records = len(self.df)
        
        print("🔍 KEY FINDINGS:")
        print(f"• Fleet consists of {unique_vehicles:,} unique vehicles")
        print(f"• Total {total_records:,} data points collected")
        print(f"• Average battery charge across fleet: {avg_battery:.1f}% (±{battery_std:.1f}%)")
        print(f"• {low_battery_records:,} records ({low_battery_records/total_records*100:.1f}%) show low battery (<{low_battery_threshold}%)")
        print(f"• Peak activity occurs at {peak_hour}:00")
        
        print(f"\n📋 RECOMMENDATIONS:")
        
        if low_battery_records > total_records * 0.1:  # More than 10% low battery
            print("🚨 HIGH PRIORITY:")
            print("• Implement proactive charging schedule - high percentage of low battery incidents")
            print("• Consider adding charging infrastructure in high-activity areas")
        
        if battery_std > 25:  # High battery variance
            print("⚠️ MEDIUM PRIORITY:")
            print("• Battery usage patterns vary significantly across vehicles")
            print("• Review vehicle allocation and route optimization")
        
        print("💡 OPERATIONAL INSIGHTS:")
        print("• Monitor battery levels during peak hours for optimal fleet management")
        print("• Use geographic data to optimize charging station placement")
        print("• Consider predictive maintenance based on battery degradation patterns")
        
        # Vehicle efficiency analysis
        vehicle_efficiency = self.df.groupby('vin')['avg_bat_charge'].mean().sort_values()
        print(f"\n🏆 FLEET PERFORMANCE:")
        print(f"• Most efficient vehicle (highest avg battery): {vehicle_efficiency.index[-1]} ({vehicle_efficiency.iloc[-1]:.1f}%)")
        print(f"• Least efficient vehicle (lowest avg battery): {vehicle_efficiency.index[0]} ({vehicle_efficiency.iloc[0]:.1f}%)")
        
        return {
            'avg_battery': avg_battery,
            'battery_std': battery_std,
            'low_battery_records': low_battery_records,
            'peak_hour': peak_hour,
            'unique_vehicles': unique_vehicles,
            'total_records': total_records
        }
    
    def export_summary_report(self):
        """Export a summary report to CSV"""
        print("\n💾 STEP 9: EXPORTING SUMMARY REPORT")
        print("-" * 50)
        
        # Vehicle summary
        vehicle_summary = self.df.groupby('vin').agg({
            'avg_bat_charge': ['mean', 'std', 'min', 'max', 'count'],
            'avg_lat': 'mean',
            'avg_long': 'mean'
        }).round(2)
        
        vehicle_summary.columns = ['avg_battery', 'battery_std', 'min_battery', 
                                 'max_battery', 'total_records', 'avg_latitude', 'avg_longitude']
        
        vehicle_summary.to_csv('turno_vehicle_summary.csv')
        print("✅ Vehicle summary exported to 'turno_vehicle_summary.csv'")
        
        # Hourly summary
        hourly_summary = self.df.groupby('hr').agg({
            'avg_bat_charge': 'mean',
            'vin': ['count', 'nunique']
        }).round(2)
        
        hourly_summary.columns = ['avg_battery', 'total_records', 'unique_vehicles']
        hourly_summary.to_csv('turno_hourly_summary.csv')
        print("✅ Hourly summary exported to 'turno_hourly_summary.csv'")
        
        return vehicle_summary, hourly_summary
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        if self.df is None:
            print("❌ No data loaded. Cannot proceed with analysis.")
            return None
        
        print("🚀 STARTING COMPLETE TURNO DATA ANALYSIS")
        print("=" * 60)
        
        # Run all analysis steps
        basic_stats = self.basic_statistics()
        vehicle_stats = self.vehicle_analysis()
        temporal_stats = self.temporal_analysis()
        geo_stats = self.geographic_analysis()
        battery_stats = self.battery_analysis()
        
        # Create visualizations
        self.create_visualizations()
        
        # Generate insights
        insights = self.generate_insights()
        
        # Export reports
        reports = self.export_summary_report()
        
        print("\n🎉 ANALYSIS COMPLETE!")
        print("=" * 60)
        print("📁 Generated files:")
        print("• turno_analysis_visualizations.png - Comprehensive charts")
        print("• turno_vehicle_summary.csv - Per-vehicle statistics")
        print("• turno_hourly_summary.csv - Hourly patterns")
        
        return {
            'basic_stats': basic_stats,
            'vehicle_stats': vehicle_stats,
            'temporal_stats': temporal_stats,
            'geo_stats': geo_stats,
            'battery_stats': battery_stats,
            'insights': insights,
            'reports': reports
        }

# Main execution
if __name__ == "__main__":
    # Initialize the analyzer
    analyzer = TurnoDataAnalyzer('turno_data.csv')
    
    # Run complete analysis
    results = analyzer.run_complete_analysis()
    
    if results:
        print("\n✨ Analysis completed successfully!")
        print("Check the generated files for detailed results and visualizations.")
    else:
        print("\n❌ Analysis failed. Please check your data file and try again.")