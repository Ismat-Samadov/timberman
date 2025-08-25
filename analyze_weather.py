import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime

# Create charts directory
os.makedirs('charts', exist_ok=True)

# Set style for better-looking charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_rainfall_data():
    """Load and process rainfall data"""
    df = pd.read_csv('data/rainfall_yagintinin-miqdari.csv', encoding='utf-8', sep=';')
    
    # Clean and process the data
    years = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', 
             '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', 
             '2020', '2021', '2022', '2023']
    
    # Extract country-wide annual rainfall data
    country_rainfall = []
    baku_rainfall = []
    ganja_rainfall = []
    
    # Row 4 contains country annual rainfall
    country_row = df.iloc[3]
    for year in years:
        try:
            val = str(country_row[year]).replace(',', '.').strip()
            if val and val != 'nan' and val != '':
                country_rainfall.append(float(val))
            else:
                country_rainfall.append(None)
        except:
            country_rainfall.append(None)
    
    # Row 8 contains Baku annual rainfall  
    baku_row = df.iloc[7]
    for year in years:
        try:
            val = str(baku_row[year]).replace(',', '.').strip()
            if val and val != 'nan' and val != '':
                baku_rainfall.append(float(val))
            else:
                baku_rainfall.append(None)
        except:
            baku_rainfall.append(None)
    
    # Row 14 contains Ganja annual rainfall
    ganja_row = df.iloc[13]
    for year in years:
        try:
            val = str(ganja_row[year]).replace(',', '.').strip()
            if val and val != 'nan' and val != '':
                ganja_rainfall.append(float(val))
            else:
                ganja_rainfall.append(None)
        except:
            ganja_rainfall.append(None)
    
    return pd.DataFrame({
        'Year': years,
        'Country': country_rainfall,
        'Baku': baku_rainfall,
        'Ganja': ganja_rainfall
    })

def load_temperature_data():
    """Load and process temperature data"""
    df = pd.read_csv('data/temperature_havanin-temperaturu.csv', encoding='utf-8', sep=';')
    
    years = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', 
             '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', 
             '2020', '2021', '2022', '2023']
    
    # Extract temperature data
    country_temp = []
    baku_temp = []
    ganja_temp = []
    
    # Row 4 contains country annual temperature
    country_row = df.iloc[3]
    for year in years:
        try:
            val = str(country_row[year]).replace(',', '.').strip()
            if val and val != 'nan' and val != '':
                country_temp.append(float(val))
            else:
                country_temp.append(None)
        except:
            country_temp.append(None)
    
    # Row 10 contains Baku annual temperature
    baku_row = df.iloc[9]
    for year in years:
        try:
            val = str(baku_row[year]).replace(',', '.').strip()
            if val and val != 'nan' and val != '':
                baku_temp.append(float(val))
            else:
                baku_temp.append(None)
        except:
            baku_temp.append(None)
    
    # Row 16 contains Ganja annual temperature
    ganja_row = df.iloc[15]
    for year in years:
        try:
            val = str(ganja_row[year]).replace(',', '.').strip()
            if val and val != 'nan' and val != '':
                ganja_temp.append(float(val))
            else:
                ganja_temp.append(None)
        except:
            ganja_temp.append(None)
    
    return pd.DataFrame({
        'Year': years,
        'Country': country_temp,
        'Baku': baku_temp,
        'Ganja': ganja_temp
    })

def load_current_weather_data():
    """Load and process current city weather data"""
    with open('data/city_weather_seher-merkezleri-uzre-cari-hava-melumatlari.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cities_data = []
    for city in data['datas']:
        cities_data.append({
            'lat': float(city['lat']),
            'lon': float(city['lon']),
            'temp': float(city['temp']),
            'temp_day': city.get('temp_day', None),
            'temp_night': city.get('temp_night', None),
            'icon': city.get('icon', 'unknown')
        })
    
    return pd.DataFrame(cities_data)

def create_rainfall_charts(rainfall_df):
    """Create rainfall analysis charts"""
    # Chart 1: Annual Rainfall Trends
    plt.figure(figsize=(12, 8))
    
    years_int = [int(y) for y in rainfall_df['Year']]
    
    plt.subplot(2, 2, 1)
    plt.plot(years_int, rainfall_df['Country'], marker='o', linewidth=2, label='Country Average')
    plt.plot(years_int, rainfall_df['Baku'], marker='s', linewidth=2, label='Baku')
    plt.plot(years_int, rainfall_df['Ganja'], marker='^', linewidth=2, label='Ganja')
    plt.title('Annual Rainfall Trends (2002-2023)', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Rainfall (mm)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Chart 2: Average Rainfall Comparison
    plt.subplot(2, 2, 2)
    avg_rainfall = [
        rainfall_df['Country'].mean(),
        rainfall_df['Baku'].mean(),
        rainfall_df['Ganja'].mean()
    ]
    locations = ['Country', 'Baku', 'Ganja']
    bars = plt.bar(locations, avg_rainfall, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Average Annual Rainfall (2002-2023)', fontsize=14, fontweight='bold')
    plt.ylabel('Rainfall (mm)')
    
    # Add value labels on bars
    for bar, value in zip(bars, avg_rainfall):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                f'{value:.1f}mm', ha='center', va='bottom')
    
    # Chart 3: Rainfall Variability
    plt.subplot(2, 2, 3)
    rainfall_data = [rainfall_df['Country'].dropna(), rainfall_df['Baku'].dropna(), rainfall_df['Ganja'].dropna()]
    plt.boxplot(rainfall_data, labels=['Country', 'Baku', 'Ganja'])
    plt.title('Rainfall Variability Distribution', fontsize=14, fontweight='bold')
    plt.ylabel('Rainfall (mm)')
    
    # Chart 4: Drought/Wet Years Analysis
    plt.subplot(2, 2, 4)
    country_mean = rainfall_df['Country'].mean()
    rainfall_anomaly = rainfall_df['Country'] - country_mean
    colors = ['red' if x < 0 else 'blue' for x in rainfall_anomaly]
    plt.bar(years_int, rainfall_anomaly, color=colors, alpha=0.7)
    plt.title('Rainfall Anomaly (Deviation from Mean)', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Anomaly (mm)')
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('charts/rainfall_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_temperature_charts(temp_df):
    """Create temperature analysis charts"""
    plt.figure(figsize=(12, 8))
    
    years_int = [int(y) for y in temp_df['Year']]
    
    # Chart 1: Temperature Trends
    plt.subplot(2, 2, 1)
    plt.plot(years_int, temp_df['Country'], marker='o', linewidth=2, label='Country Average')
    plt.plot(years_int, temp_df['Baku'], marker='s', linewidth=2, label='Baku')
    plt.plot(years_int, temp_df['Ganja'], marker='^', linewidth=2, label='Ganja')
    plt.title('Annual Temperature Trends (2002-2023)', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Chart 2: Temperature Comparison
    plt.subplot(2, 2, 2)
    avg_temp = [
        temp_df['Country'].mean(),
        temp_df['Baku'].mean(),
        temp_df['Ganja'].mean()
    ]
    locations = ['Country', 'Baku', 'Ganja']
    bars = plt.bar(locations, avg_temp, color=['#d62728', '#ff7f0e', '#2ca02c'])
    plt.title('Average Annual Temperature (2002-2023)', fontsize=14, fontweight='bold')
    plt.ylabel('Temperature (°C)')
    
    # Add value labels
    for bar, value in zip(bars, avg_temp):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{value:.1f}°C', ha='center', va='bottom')
    
    # Chart 3: Temperature Warming Trend
    plt.subplot(2, 2, 3)
    z = np.polyfit(years_int, temp_df['Country'], 1)
    p = np.poly1d(z)
    plt.plot(years_int, temp_df['Country'], 'o-', alpha=0.7, label='Annual Temperature')
    plt.plot(years_int, p(years_int), "r--", alpha=0.8, linewidth=2, label=f'Trend: +{z[0]:.3f}°C/year')
    plt.title('Climate Change Trend - Country Average', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Chart 4: Temperature Anomaly
    plt.subplot(2, 2, 4)
    baseline_temp = temp_df['Country'][:10].mean()  # 2002-2011 baseline
    temp_anomaly = temp_df['Country'] - baseline_temp
    colors = ['blue' if x < 0 else 'red' for x in temp_anomaly]
    plt.bar(years_int, temp_anomaly, color=colors, alpha=0.7)
    plt.title(f'Temperature Anomaly (vs 2002-2011 baseline: {baseline_temp:.1f}°C)', fontsize=12, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Anomaly (°C)')
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('charts/temperature_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_current_weather_charts(current_df):
    """Create current weather analysis charts"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Chart 1: Temperature Distribution
    axes[0, 0].hist(current_df['temp'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Current Temperature Distribution Across Cities', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Temperature (°C)')
    axes[0, 0].set_ylabel('Number of Cities')
    axes[0, 0].axvline(current_df['temp'].mean(), color='red', linestyle='--', 
                      label=f'Mean: {current_df["temp"].mean():.1f}°C')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Chart 2: Geographic Temperature Map
    scatter = axes[0, 1].scatter(current_df['lon'], current_df['lat'], c=current_df['temp'], 
                               s=50, cmap='coolwarm', alpha=0.8)
    axes[0, 1].set_title('Temperature by Geographic Location', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Longitude')
    axes[0, 1].set_ylabel('Latitude')
    plt.colorbar(scatter, ax=axes[0, 1], label='Temperature (°C)')
    
    # Chart 3: Day/Night Temperature Comparison
    day_temps = current_df['temp_day'].dropna()
    night_temps = current_df['temp_night'].dropna()
    
    x = np.arange(len(['Day', 'Night']))
    temps = [day_temps.mean(), night_temps.mean()]
    bars = axes[1, 0].bar(x, temps, color=['orange', 'navy'], alpha=0.7)
    axes[1, 0].set_title('Average Day vs Night Temperature', fontsize=14, fontweight='bold')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(['Day', 'Night'])
    axes[1, 0].set_ylabel('Temperature (°C)')
    
    # Add value labels
    for bar, temp in zip(bars, temps):
        axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                       f'{temp:.1f}°C', ha='center', va='bottom')
    
    # Chart 4: Weather Conditions Distribution
    weather_counts = current_df['icon'].value_counts()
    weather_labels = [label.replace('_', ' ').title() for label in weather_counts.index[:6]]
    
    axes[1, 1].pie(weather_counts.values[:6], labels=weather_labels, autopct='%1.1f%%', 
                  startangle=90)
    axes[1, 1].set_title('Current Weather Conditions Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('charts/current_weather_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_statistics():
    """Generate comprehensive weather statistics"""
    rainfall_df = load_rainfall_data()
    temp_df = load_temperature_data()
    current_df = load_current_weather_data()
    
    stats = {
        'rainfall': {
            'country_avg': rainfall_df['Country'].mean(),
            'country_std': rainfall_df['Country'].std(),
            'baku_avg': rainfall_df['Baku'].mean(),
            'ganja_avg': rainfall_df['Ganja'].mean(),
            'wettest_year': rainfall_df.loc[rainfall_df['Country'].idxmax(), 'Year'],
            'driest_year': rainfall_df.loc[rainfall_df['Country'].idxmin(), 'Year'],
            'max_rainfall': rainfall_df['Country'].max(),
            'min_rainfall': rainfall_df['Country'].min()
        },
        'temperature': {
            'country_avg': temp_df['Country'].mean(),
            'country_std': temp_df['Country'].std(),
            'baku_avg': temp_df['Baku'].mean(),
            'ganja_avg': temp_df['Ganja'].mean(),
            'warmest_year': temp_df.loc[temp_df['Country'].idxmax(), 'Year'],
            'coolest_year': temp_df.loc[temp_df['Country'].idxmin(), 'Year'],
            'warming_trend': np.polyfit([int(y) for y in temp_df['Year']], temp_df['Country'], 1)[0]
        },
        'current': {
            'cities_count': len(current_df),
            'temp_avg': current_df['temp'].mean(),
            'temp_std': current_df['temp'].std(),
            'temp_max': current_df['temp'].max(),
            'temp_min': current_df['temp'].min(),
            'day_temp_avg': current_df['temp_day'].mean(),
            'night_temp_avg': current_df['temp_night'].mean()
        }
    }
    
    return stats

if __name__ == "__main__":
    print("🌦️  Starting Weather Data Analysis...")
    
    # Load data
    print("📊 Loading data...")
    rainfall_df = load_rainfall_data()
    temp_df = load_temperature_data()
    current_df = load_current_weather_data()
    
    # Create charts
    print("📈 Creating rainfall charts...")
    create_rainfall_charts(rainfall_df)
    
    print("🌡️  Creating temperature charts...")
    create_temperature_charts(temp_df)
    
    print("🌤️  Creating current weather charts...")
    create_current_weather_charts(current_df)
    
    # Generate statistics
    print("📋 Generating statistics...")
    stats = generate_statistics()
    
    print("\n✅ Analysis complete! Charts saved to 'charts/' directory")
    print("\n🔍 Key Findings:")
    print(f"• Average annual rainfall: {stats['rainfall']['country_avg']:.1f}mm")
    print(f"• Average annual temperature: {stats['temperature']['country_avg']:.1f}°C")
    print(f"• Climate warming trend: +{stats['temperature']['warming_trend']:.3f}°C per year")
    print(f"• Current temperature range: {stats['current']['temp_min']:.1f}°C to {stats['current']['temp_max']:.1f}°C")
    print(f"• Weather data from {stats['current']['cities_count']} cities")