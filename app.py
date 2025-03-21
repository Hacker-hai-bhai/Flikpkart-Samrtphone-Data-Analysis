import streamlit as st
import pandas as pd
import plotly.express as px

# Set dark theme
st.set_page_config(page_title="Flipkart Smartphone Analysis", layout="wide")

st.markdown(
    """
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        @keyframes glow {
            0% { box-shadow: 0 0 10px rgba(0, 255, 255, 0.2); }
            50% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
            100% { box-shadow: 0 0 10px rgba(0, 255, 255, 0.2); }
        }

        body {
            color: #E0E0E0;
            background-color: #121212;
            font-family: 'Arial', sans-serif;
        }

        header { visibility: hidden; }

        .stApp {
            background-color: #121212;
            color: #E0E0E0;
            animation: fadeIn 0.5s ease;
        }

        .stTitle {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #00FFF7;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 255, 255, 0.4);
            animation: fadeIn 0.8s ease;
        }

        .section-header {
            font-size: 24px;
            font-weight: bold;
            color: #00FFF7;
            margin-top: 20px;
            text-shadow: 1px 1px 3px rgba(0, 255, 255, 0.5);
            border-bottom: 2px solid #00ADB5;
            padding-bottom: 5px;
            animation: fadeIn 0.8s ease;
        }

        /* Sidebar Slide-in Animation */
        [data-testid="stSidebar"] {
            background-color: #1E1E1E;
            padding: 20px;
            color: #E0E0E0;
            border-right: 2px solid #00ADB5;
            animation: slideIn 0.5s ease;
        }

        /* Hover Effect on Sidebar Inputs */
        [data-testid="stSidebar"] select,
        [data-testid="stSidebar"] input {
            background-color: #292929;
            color: #E0E0E0;
            border: 1px solid #00ADB5;
            border-radius: 4px;
            padding: 6px;
            transition: all 0.3s ease;
        }

        [data-testid="stSidebar"] select:focus,
        [data-testid="stSidebar"] input:focus {
            outline: none;
            border-color: #00FFF7;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
            transform: scale(1.05);
        }
        

        /* Hover Effect on Compare Table */
        .compare-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }

        .compare-table th,
        .compare-table td {
            border: 1px solid #00ADB5;
            padding: 8px;
            text-align: center;
            color: #E0E0E0;
            transition: background-color 0.3s ease;
        }

        .compare-table th {
            background-color: #00ADB5;
            color: #121212;
            font-weight: bold;
            animation: fadeIn 0.8s ease;
        }

        .compare-table tr:nth-child(even) {
            background-color: #1E1E1E;
        }

        .compare-table tr:nth-child(odd) {
            background-color: #121212;
        }

        .compare-table tr:hover {
            background-color: #00ADB5;
            color: #121212;
            transform: scale(1.02);
            transition: all 0.3s ease;
        }

        /* Glow effect for plots */
        .plot-container {
            animation: glow 2s infinite;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)
# CSS and JS for sidebar animation
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            transition: transform 0.4s ease;
            z-index: 999;
        }
        .collapsed [data-testid="stSidebar"] {
            transform: translateX(-100%);
        }
    </style>
    
    <script>
        function toggleSidebar() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                const isCollapsed = document.body.classList.contains('collapsed');
                if (isCollapsed) {
                    document.body.classList.remove('collapsed');
                } else {
                    document.body.classList.add('collapsed');
                }
            }
        }
    </script>
    """,
    unsafe_allow_html=True
)

# Sidebar Styling
st.markdown(
    """
    <style>
       /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        padding: 20px;
        color: #E0E0E0;
        border-right: 2px solid #00ADB5;
    }
    
    /* Input Fields */
    [data-testid="stSidebar"] select, 
    [data-testid="stSidebar"] input {
        background-color: #292929;
        color: #E0E0E0;
        border: 1px solid #00ADB5;
        border-radius: 4px;
        padding: 8px;
        width: 100%;
    }
    
    
    [data-testid="stSidebar"] select:focus, 
    [data-testid="stSidebar"] input:focus {
        outline: none;
        border-color: #00FFF7;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
    }

    /* Sidebar Expander */
    .st-expander {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
    }
        }
        
    </style>
    """,
    unsafe_allow_html=True
)

# Apply custom CSS to make the sidebar compact and fixed
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 350px !important;
            min-width: 350px !important;
            position: fixed !important;
            height: 100vh !important;
            overflow-y: auto !important;
        }
        [data-testid="stSidebarContent"] {
            padding: 15px;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)




# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('updated_data.csv')
    data.columns = data.columns.str.lower().str.replace(' ', '_')
    data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')
    data['original_price'] = pd.to_numeric(data['original_price'], errors='coerce')
    data['discounted_price'] = pd.to_numeric(data['discounted_price'], errors='coerce')
    data['battery_capacity'] = pd.to_numeric(data['battery_capacity'], errors='coerce')
    data['memory'] = data['memory'].astype(str)
    data['storage'] = data['storage'].astype(str)
    data['rear_camera'] = data['rear_camera'].astype(str)
    data['front_camera'] = data['front_camera'].astype(str)
    data['processor'] = data['processor'].astype(str)
    return data

data = load_data()
# ---- SIDEBAR FILTERS ----
with st.sidebar:
    st.markdown("<h3 style='color: cyan;'>🛠️ Filters</h3>", unsafe_allow_html=True)

    # Brand Filter
    with st.expander("🔎 Brand"):
        brands = st.multiselect(
            "Select Brand(s):",
            options=data['brand'].unique(),
            default=data['brand'].unique()
        )

    # Price Range Filter
    with st.expander("💲 Price Range"):
        min_price = int(data['original_price'].min())
        max_price = int(data['original_price'].max())
        price_range = st.slider("₹:", min_price, max_price, (min_price, max_price))

    # Ratings Filter
    with st.expander("⭐ Ratings"):
        min_rating = float(data['ratings'].min())
        max_rating = float(data['ratings'].max())
        rating_range = st.slider("Range:", min_rating, max_rating, (min_rating, max_rating))

    # Battery Filter
    with st.expander("🔋 Battery Capacity"):
        min_battery = int(data['battery_capacity'].min())
        max_battery = int(data['battery_capacity'].max())
        battery_range = st.slider("mAh:", min_battery, max_battery, (min_battery, max_battery))

    # Memory Filter
    with st.expander("💾 Memory"):
        memory_options = data['memory'].unique()
        selected_memory = st.multiselect(
            "Select Memory (RAM):",
            options=memory_options,
            default=memory_options
        )

    # Storage Filter
    with st.expander("💽 Storage"):
        storage_options = data['storage'].unique()
        selected_storage = st.multiselect(
            "Select Storage:",
            options=storage_options,
            default=storage_options
        )

    # Processor Filter
    with st.expander("🖥️ Processor"):
        processor_options = data['processor'].unique()
        selected_processor = st.multiselect(
            "Select Processor:",
            options=processor_options,
            default=processor_options
        )

# ---- APPLY FILTERS ----
filtered_data = data[
    (data['brand'].isin(brands)) &
    (data['original_price'] >= price_range[0]) &
    (data['original_price'] <= price_range[1]) &
    (data['ratings'] >= rating_range[0]) &
    (data['ratings'] <= rating_range[1]) &
    (data['battery_capacity'] >= battery_range[0]) &
    (data['battery_capacity'] <= battery_range[1]) &
    (data['memory'].isin(selected_memory)) &
    (data['storage'].isin(selected_storage)) &
    (data['processor'].isin(selected_processor))
]
# ---- Title ----
st.markdown("<div class='stTitle'>📱 Flipkart Smartphone Data Analysis</div>", unsafe_allow_html=True)

# ---- Brand Market Share ----
st.markdown("<div class='section-header'>🏆 Brand Market Share</div>", unsafe_allow_html=True)
brand_counts = filtered_data['brand'].value_counts().reset_index()
brand_counts.columns = ['brand', 'count']

fig_brand_share = px.pie(
    brand_counts,
    names='brand',
    values='count',
    title='Brand Market Share',
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Bold  # Keeps color consistent
)


fig_brand_share.update_layout(
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font=dict(color='#E0E0E0'),
    legend=dict(
        font=dict(color='#FFFFFF'),
        bgcolor='#1E1E1E',
        bordercolor='#00ADB5',
        borderwidth=1
    )
)
st.plotly_chart(fig_brand_share)

# ---- Price vs Ratings ----
st.markdown("<div class='section-header'>💲 Price vs Ratings</div>", unsafe_allow_html=True)

fig_price_vs_rating = px.scatter(
    filtered_data,  # Apply filtered data
    x='original_price',
    y='ratings',
    color='brand',
    title='Price vs Ratings',
    hover_data=['model'],
    color_discrete_sequence=px.colors.qualitative.Set1  # Keeps color consistent
)


fig_price_vs_rating.update_layout(
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font=dict(color='#E0E0E0'),
    legend=dict(
        font=dict(color='#FFFFFF'),
        bgcolor='#1E1E1E',
        bordercolor='#00ADB5',
        borderwidth=1
    )
)
st.plotly_chart(fig_price_vs_rating)

# ---- Battery vs Price ----
st.markdown("<div class='section-header'>🔋 Battery Capacity vs Price</div>", unsafe_allow_html=True)

fig_battery_vs_price = px.scatter(
    filtered_data,  # Apply filtered data
    x='battery_capacity',
    y='original_price',
    color='brand',
    title='Battery Capacity vs Price',
    hover_data=['model'],
    color_discrete_sequence=px.colors.qualitative.Dark24  # Keeps color consistent
)


fig_battery_vs_price.update_layout(
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font=dict(color='#E0E0E0'),
    legend=dict(
        font=dict(color='#FFFFFF'),
        bgcolor='#1E1E1E',
        bordercolor='#00ADB5',
        borderwidth=1
    )
)
st.plotly_chart(fig_battery_vs_price)

# ---- Ratings Distribution ----
st.markdown("<div class='section-header'>⭐ Ratings Distribution</div>", unsafe_allow_html=True)

fig_ratings = px.histogram(
    filtered_data,  # Apply filtered data
    x='ratings',
    color='brand',
    title='Ratings Distribution',
    nbins=30,
    color_discrete_sequence=px.colors.qualitative.Vivid  # Keeps color consistent
)

fig_ratings.update_layout(
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font=dict(color='#E0E0E0'),
    legend=dict(
        font=dict(color='#FFFFFF'),
        bgcolor='#1E1E1E',
        bordercolor='#00ADB5',
        borderwidth=1
    )
)
st.plotly_chart(fig_ratings)


# ✅ Load Data
df = data

# ✅ Maintain Dark Theme
plotly_template = "plotly_dark"


# ✅ Function to Apply Dark Theme and CSS Glow to Graphs
def dark_style(fig):
    fig.update_layout(
        plot_bgcolor="black",  # Dark graph background
        paper_bgcolor="black",  # Dark surrounding background
        font=dict(color="#00FFFF"),  # Neon text color
        xaxis=dict(showgrid=True, gridcolor="gray"),
        yaxis=dict(showgrid=True, gridcolor="gray"),
        title=dict(font=dict(size=16, color="#00FFFF")),
         legend=dict(
        font=dict(color='#FFFFFF'),
        bgcolor='#1E1E1E',
        bordercolor='#00ADB5',
        borderwidth=1
         )
    )
    return fig

# ✅ Function to Create Colored Headers
def section_header(text, color):
    st.markdown(f"<h2 style='color:{color}; text-align:left;'>{text}</h2>", unsafe_allow_html=True)

# ✅ Function to Create Section Headers (Outside Graph)
def section_header(text, color="#00FFFF"):
    st.markdown(f"<h2 style='color:{color}; text-align:left;'>{text}</h2>", unsafe_allow_html=True)

# ✅ Top 10 Most Reviewed Smartphones (Filtered)
section_header("📢 Top 10 Most Reviewed Smartphones")
if "reviews" in filtered_data.columns and "model" in filtered_data.columns:
    top_reviewed = filtered_data.nlargest(10, "reviews")  # Apply filtering

    fig = px.bar(top_reviewed, 
                 x="reviews", 
                 y="model", 
                 title="",  # Remove title inside the graph
                 labels={"reviews": "Number of Reviews", "model": "Smartphone Model"},
                 color="reviews",
                 color_continuous_scale="viridis",
                 template=plotly_template,
                 text_auto=True)

    fig = dark_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ✅ Average Ratings by Brand (Filtered)
section_header("⭐ Average Ratings by Brand")
if "brand" in filtered_data.columns and "ratings" in filtered_data.columns:
    avg_ratings = filtered_data.groupby("brand")["ratings"].mean().sort_values(ascending=False).reset_index()

    fig = px.bar(avg_ratings, 
                 x="ratings", 
                 y="brand", 
                 title="",  # Remove title inside the graph
                 labels={"ratings": "Average Rating", "brand": "Brand"},
                 template=plotly_template,
                 text_auto=True,
                 color="ratings",
                 color_continuous_scale="viridis")

    fig = dark_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ✅ Price Distribution by Brand (Filtered)
section_header("💰 Price Distribution by Brand")
if "brand" in filtered_data.columns and "original_price" in filtered_data.columns:
    fig = px.box(filtered_data, 
                 x="brand", 
                 y="original_price",
                 title="",  # Remove title inside the graph
                 labels={"original_price": "Price", "brand": "Brand"},
                 template=plotly_template,
                 color="brand")

    fig.update_xaxes(tickangle=-45)
    fig = dark_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ✅ Battery Capacity vs. Ratings (Filtered)
section_header("🔋 Battery Capacity vs. Ratings")
if "battery_capacity" in filtered_data.columns and "ratings" in filtered_data.columns and "brand" in filtered_data.columns:
    fig = px.scatter(filtered_data, 
                     x="battery_capacity", 
                     y="ratings",
                     color="brand",
                     title="",  # Remove title inside the graph
                     labels={"battery_capacity": "Battery Capacity (mAh)", "ratings": "Ratings"},
                     template=plotly_template,
                     color_continuous_scale="viridis")

    fig = dark_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ✅ Processor Performance Analysis (Filtered)
section_header("⚡ Processor Performance Analysis")
if "processor" in filtered_data.columns:
    processor_counts = filtered_data["processor"].value_counts().head(10).reset_index()
    processor_counts.columns = ["processor", "count"]

    fig = px.bar(processor_counts, 
                 x="count", 
                 y="processor", 
                 title="",  # Remove title inside the graph
                 labels={"count": "Number of Smartphones", "processor": "Processor"},
                 template=plotly_template,
                 text_auto=True,
                 color="count",
                 color_continuous_scale="viridis")

    fig = dark_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ---- Compare Smartphones ----
st.markdown("<div class='section-header'>🆚 Compare Smartphones</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    model1 = st.selectbox("Select First Smartphone:", data['model'].unique())

with col2:
    model2 = st.selectbox("Select Second Smartphone:", data['model'].unique())

if model1 and model2:
    phone1 = data[data['model'] == model1].iloc[0]
    phone2 = data[data['model'] == model2].iloc[0]

    st.markdown(f"""
    <table class='compare-table'>
        <tr>
            <th>Feature</th>
            <th>{model1}</th>
            <th>{model2}</th>
        </tr>
        <tr>
            <td>Original Price</td>
            <td>{phone1['original_price']}</td>
            <td>{phone2['original_price']}</td>
        </tr>
        <tr>
            <td>Discounted Price</td>
            <td>{phone1['discounted_price']}</td>
            <td>{phone2['discounted_price']}</td>
        </tr>
        <tr>
            <td>Ratings</td>
            <td>{phone1['ratings']}</td>
            <td>{phone2['ratings']}</td>
        </tr>
        <tr>
            <td>Battery Capacity</td>
            <td>{phone1['battery_capacity']}</td>
            <td>{phone2['battery_capacity']}</td>
        </tr>
        <tr>
            <td>Memory</td>
            <td>{phone1['memory']}</td>
            <td>{phone2['memory']}</td>
        </tr>
        <tr>
            <td>Rear Camera</td>
            <td>{phone1['rear_camera']}</td>
            <td>{phone2['rear_camera']}</td>
        </tr>
        <tr>
            <td>Front Camera</td>
            <td>{phone1['front_camera']}</td>
            <td>{phone2['front_camera']}</td>
        </tr>
        <tr>
            <td>Processor</td>
            <td>{phone1['processor']}</td>
            <td>{phone2['processor']}</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

