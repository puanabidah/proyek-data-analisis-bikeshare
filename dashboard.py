import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Helper Functions
def load_and_prepare_data(filepath):
    day_df = pd.read_csv(filepath)
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df

def filter_data_by_year(df, start_year, end_year):
    return df[(df['dteday'].dt.year >= start_year) & (df['dteday'].dt.year <= end_year)]

def filter_data_by_date(df, start_date, end_date):
    return df[(df['dteday'] >= start_date) & (df['dteday'] <= end_date)]

def add_year_column(df):
    df['yr'] = df['dteday'].dt.year
    return df

def plot_line(data, x, y, hue, title, labels, figsize=(10, 6)):
    plt.figure(figsize=figsize)
    sns.lineplot(data=data, x=x, y=y, hue=hue, marker='o', palette='Set2')
    plt.xticks(ticks=range(len(labels)), labels=labels, rotation=45, fontsize=10)
    plt.title(title)
    plt.xlabel(None)
    plt.ylabel(None)
    plt.legend(title=None, fontsize=10)
    plt.grid(True)
    st.pyplot(plt)

def plot_total_rentals(data):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='dteday', y='cnt', marker='o', color='blue')
    plt.title('Total Penyewaan Sepeda Harian')
    plt.xlabel(None)
    plt.ylabel(None)
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

def plot_bar(data, x, y, hue, title, labels, figsize=(8, 6)):
    plt.figure(figsize=figsize)
    sns.barplot(x=x, y=y, data=data, hue=hue, palette='Set2', errorbar=None)
    plt.xticks(ticks=range(len(labels)), labels=labels, fontsize=12)
    plt.legend(title=None, labels=year_labels, fontsize=10)
    plt.title(title)
    plt.xlabel(None)
    plt.ylabel(None)
    st.pyplot(plt)

def plot_comparison_bar(data, x, y, hue, title, labels, figsize=(14, 5)):
    fig, axes = plt.subplots(1, 2, figsize=figsize, sharey=True)
    
    # Plot untuk casual users
    sns.barplot(x=x, y='casual_mean', hue=hue, data=data, errorbar=None, ax=axes[0])
    axes[0].set_title('Pengguna Casual: Hari Kerja vs Hari Libur')  # Title untuk casual
    axes[0].set_xlabel(None)
    axes[0].set_ylabel(None)

    # Plot untuk registered users
    sns.barplot(x=x, y='registered_mean', hue=hue, data=data, errorbar=None, ax=axes[1])
    axes[1].set_title('Pengguna Registered: Hari Kerja vs Hari Libur')  # Title untuk registered
    axes[1].set_xlabel(None)
    axes[1].set_ylabel(None)
    
    # Menghilangkan legend dari masing-masing plot
    axes[0].legend_.remove()
    axes[1].legend_.remove()

    # Menambahkan legend untuk figure secara keseluruhan
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', title='Tahun', bbox_to_anchor=(0.512, 1.05), ncol=2)

    plt.tight_layout()
    st.pyplot(fig)

# Main code
st.title(":blue[Bikeshare Dashboard] 📊")

# List of years
year_labels = ["2011", "2012"]

# Load and prepare data
day_df = load_and_prepare_data( "day.csv")

# Sidebar: Filter by Date
with st.sidebar:
    st.header("Filter Bikeshare Data 📆")
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    start_date, end_date = st.date_input(
        "Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date
    )

# Filter data based on selected dates
filtered_df = filter_data_by_date(day_df, pd.Timestamp(start_date), pd.Timestamp(end_date))

# Display total rentals for the selected range
st.subheader(f"Penyewaan Sepeda dari {start_date} hingga {end_date}", divider="gray")
total_rentals = filtered_df['cnt'].sum()

# Display total casual and registered users in the selected date range
total_casual = filtered_df['casual'].sum()
total_registered = filtered_df['registered'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=total_rentals)
with col2:
    st.metric('Total Pengguna Casual', value=total_casual)
with col3:
    st.metric('Total Pengguna Registered', value=total_registered)

# Plot total rentals over the selected date range
plot_total_rentals(filtered_df)

# Filter and prepare data for analysis
filtered_df = filter_data_by_year(day_df, 2011, 2012)
filtered_df = add_year_column(filtered_df)

# Agregasi berdasarkan 'weekday' dan 'year'
result_weekday = (
    filtered_df.groupby(by=['weekday', 'yr'])
    .agg({"cnt": ["sum", "mean"]})
    .reset_index()
    .sort_values(by=('cnt', 'sum'), ascending=False)
)
result_weekday.columns = ['weekday', 'year', 'cnt_sum', 'cnt_mean']

# Visualisasi Line Plot: Penggunaan Sepeda per Hari dalam Seminggu
st.subheader("Rata-Rata Penggunaan Sepeda per Hari dalam Seminggu (2011-2012)")
plot_line(result_weekday, 'weekday', 'cnt_mean', 'year', 
          '', 
          ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])

# Agregasi berdasarkan 'workingday' dan 'year'
result_workday = (
    day_df.groupby(by=['workingday', 'yr'])
    .agg({"cnt": ["sum", "mean"]})
    .reset_index()
    .sort_values(by=('cnt', 'sum'), ascending=False)
)
result_workday.columns = ['workingday', 'year', 'cnt_sum', 'cnt_mean']

# Visualisasi Bar Plot: Penyewaan Sepeda pada Workingday
st.subheader('Perbedaan Rata-Rata Penyewaan Sepeda pada Workingday')
plot_bar(result_workday, 'workingday', 'cnt_mean', 'year', 
         '', 
         ["Hari Libur", "Hari Kerja"])

# Agregasi berdasarkan 'workingday' dan 'year' untuk casual dan registered
result_user = filtered_df.groupby(by=['workingday', 'yr']).agg({
    'casual': ['sum', 'mean'],
    'registered': ['sum', 'mean'],
    'cnt': ['sum', 'mean']
}).reset_index().sort_values(by=('cnt', 'sum'), ascending=False)

result_user.columns = ['workingday', 'year', 'casual_sum', 'casual_mean', 'registered_sum', 'registered_mean', 'cnt_sum', 'cnt_mean']
result_user['workingday_label'] = result_user['workingday'].map({0: "Hari Libur", 1: "Hari Kerja"})

# Visualisasi perbandingan pengguna casual dan registered
st.subheader('Perbandingan Pengguna Casual & Registered pada Hari Kerja dan Hari Libur')
plot_comparison_bar(result_user, 'workingday_label', 'casual_mean', 'year', 
                    '', 
                    ["Hari Libur", "Hari Kerja"])

# Agregasi berdasarkan 'season' dan 'year'
result_season = filtered_df.groupby(by=['season', 'yr']).agg({
    'cnt': ['sum', 'mean']
}).reset_index().sort_values(by=('cnt', 'sum'), ascending=False)

result_season.columns = ['season', 'year', 'cnt_sum', 'cnt_mean']

# Visualisasi perbandingan Penyewaan Sepeda pada Setiap Musim
st.subheader('Perbandingan Rata-Rata Penyewaan Sepeda pada Setiap Musim (2011-2012)')
plt.figure(figsize=(12, 6))
sns.barplot(x='season', y='cnt_mean', data=result_season, hue="year", errorbar=None, palette='Set2')
plt.legend(title=None, labels=year_labels, fontsize=10)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks([0, 1, 2, 3], ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
st.pyplot(plt)

# Agregasi berdasarkan 'month' dan 'year'
monthly_trend = (
    day_df.groupby(by=['yr', 'mnth'])
    .agg({'cnt': ['sum', 'mean']})
    .reset_index()
)
monthly_trend.columns = ['year', 'month', 'cnt_sum', 'cnt_mean']
monthly_trend['year'] = monthly_trend['year'].replace({0: 2011, 1: 2012})

# Visualisasi Tren Penyewaan Sepeda per Bulan
st.subheader('Tren Penyewaan Sepeda per Bulan (2011-2012)')
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_trend, x='month', y='cnt_mean', hue='year', marker='o', palette='Set2')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Tahun', fontsize=10)
plt.xlabel(None)
plt.ylabel(None)
plt.grid(True)
st.pyplot(plt)
