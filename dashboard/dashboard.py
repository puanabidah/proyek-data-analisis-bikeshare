import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.header('Bikeshare Dashboard 2011-2012')

# load data
day_df = pd.read_csv("..\data\day.csv")

year_labels = ["2011", "2012"]

# Pastikan kolom 'dteday' bertipe datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Filter untuk tahun 2011 dan 2012
filtered_df = day_df[(day_df['dteday'].dt.year >= 2011) & (day_df['dteday'].dt.year <= 2012)]

# Tambahkan kolom 'year' untuk mempermudah pengelompokan
filtered_df['yr'] = filtered_df['dteday'].dt.year

# Lakukan agregasi berdasarkan 'weekday' dan 'year'
result_weekday = (
    filtered_df.groupby(by=['weekday', 'yr'])
    .agg({
        "cnt": ["sum", "mean"]
    })
    .reset_index()
    .sort_values(by=('cnt', 'sum'), ascending=False)
)

result_weekday.columns = ['weekday', 'year', 'cnt_sum', 'cnt_mean']

# Visualisasi Line Plot
st.subheader("Rata-Rata Penggunaan Sepeda per Hari dalam Seminggu (2011-2012)")

# Menyiapkan plot
plt.figure(figsize=(10, 6))
sns.lineplot(
    data=result_weekday,
    x='weekday',
    y='cnt_mean',
    hue='year',
    marker='o',
    palette='Set2'
)
plt.xticks(ticks=range(7), labels=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], rotation=45, fontsize=10)
plt.xlabel(None)
plt.ylabel(None)
plt.legend(title=None, fontsize=10)
plt.grid(True)

# Menampilkan plot di Streamlit
st.pyplot(plt)


# agregasi berdasarkan 'weekworkday' dan 'year'
result_workday = (
    day_df.groupby(by=['workingday', 'yr'])
    .agg({
        "cnt": ["sum", "mean"]
    })
    .reset_index()
    .sort_values(by=('cnt', 'sum'), ascending=False)
)

result_workday.columns = ['workingday', 'year', 'cnt_sum', 'cnt_mean']

st.subheader('Perbedaan Rata-Rata Penyewaan Sepeda pada Workingday')
workday_label = ["Hari Libur", "Hari Kerja"]

plt.figure(figsize=(8, 6))
sns.barplot(x='workingday',
            y='cnt_mean',
            data=result_workday,
            hue='year',
            palette='Set2',
            errorbar=None)
plt.xticks(ticks=range(2), labels=workday_label, fontsize=12)
plt.legend(labels=year_labels, fontsize=10)
plt.xlabel(None)
plt.ylabel(None)
plt.show()
st.pyplot(plt)

result_user = filtered_df.groupby(by=['workingday', 'yr']).agg({
    'casual': ['sum', 'mean'],
    'registered': ['sum', 'mean'],
    'cnt': ['sum', 'mean']
}).reset_index().sort_values(by=('cnt', 'sum'), ascending=False)

result_user.columns = ['workingday', 'year', 'casual_sum', 'casual_mean', 'registered_sum', 'registered_mean', 'cnt_sum', 'cnt_mean']

# Menambah kolom 'workingday_label' ke dalam DataFrame
result_user['workingday_label'] = result_user['workingday'].map({0: "Hari Libur", 1: "Hari Kerja"})

# Set gaya visualisasi
sns.set(style="whitegrid")

# Persiapkan figure
fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

# Plot pengguna casual
sns.barplot(
    x='workingday_label',
    y='casual_mean',
    hue='year',
    data=result_user,
    errorbar=None,
    ax=axes[0]  # Arahkan plot ke subplot pertama
)
axes[0].set_title('Pengguna Casual: Hari Kerja vs Hari Libur')
axes[0].set_xlabel(None)
axes[0].set_ylabel(None)

# Plot pengguna registered
sns.barplot(
    x='workingday_label',
    y='registered_mean',
    hue='year',
    data=result_user,
    errorbar=None,
    ax=axes[1]  # Arahkan plot ke subplot kedua
)
axes[1].set_title('Pengguna Registered: Hari Kerja vs Hari Libur')
axes[1].set_xlabel(None)
axes[1].set_ylabel('')  # Kosongkan karena sharey=True

axes[0].legend_.remove()
axes[1].legend_.remove()

# legend untuk figure secara keseluruhan
handles, labels = axes[1].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', title='Tahun', bbox_to_anchor=(0.512, 1.05), ncol=2)

plt.tight_layout()
plt.show()
st.subheader('Perbandingan Pengguna Casual & Registered pada Hari Kerja dan Hari Libur')
st.pyplot(plt)


result_season = filtered_df.groupby(by=['season', 'yr']).agg({
    'cnt': ['sum', 'mean']
}).reset_index().sort_values(by=('cnt', 'sum'), ascending=False)

result_season.columns = ['season', 'year', 'cnt_sum', 'cnt_mean']

plt.figure(figsize=(12, 6))
sns.barplot(x='season',
            y='cnt_mean',
            data=result_season,
            hue="year",
            errorbar=None,
            palette='Set2')
plt.legend(labels=year_labels, fontsize=10)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks([0, 1, 2, 3], ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
plt.show()
st.subheader('Perbandingan Rata-Rata Penyewaan Sepeda pada Setiap Musim (2011-2012)')
st.pyplot(plt)


# Agregasi data berdasarkan 'month' dan 'year'
monthly_trend = (
    day_df.groupby(by=['yr', 'mnth'])
    .agg({
        'cnt': ['sum', 'mean']
    })
    .reset_index()
)

monthly_trend.columns = ['year', 'month', 'cnt_sum', 'cnt_mean']  # Flatten multi-index kolom agar mudah digunakan

monthly_trend['year'] = monthly_trend['year'].replace({0: 2011, 1: 2012})  # Ganti nilai 0 dan 1 dengan 2011 dan 2012

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=monthly_trend,
    x='month',
    y='cnt_mean',
    hue='year',
    marker='o',
    palette='Set2'
)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Year')
plt.grid(True)
plt.show()
st.subheader('Tren Penyewaan Sepeda per Bulan (2011-2012)')
st.pyplot(plt)