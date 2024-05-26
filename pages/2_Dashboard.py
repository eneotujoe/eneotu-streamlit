import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title='Eneotu',
    page_icon=':material/thumb_up:',
    layout='wide',
    initial_sidebar_state='auto',
    menu_items={}
)

code = """
        <style>
            .st-emotion-cache-1xarl3l {
                font-weight: bold;
                padding: 5px;
            }
            .st-emotion-cache-17c4ue {
                font-weight: bold;
                color: #ffffff !important;
            }
            div[data-testid="stMetric"], div[data-testid="metric-container"] {
            background-color: #0000ff !important; 
            color: #ffffff !important;
            padding-left: 10px;
            border-radius: 5px;
            }
        </style>
    """
st.html(code)
tab1, tab2 = st.tabs(['Stock Analysis Dashboard', 'Credit Card Fraud Analysis Dashboard'])

with tab1:
    # st.subheader('Stock Analysis', divider='rainbow')
    # stock_tickers = ['GOOGL', 'AAPL', 'TSLA', 'MSFT']
    # start = pd.to_datetime('2010-01-01')
    # end = pd.to_datetime('today')

    try:
        # stock_df = yf.download('AAPL', start=start, end=end, interval='1mo')
        stock_df = pd.read_csv('data/stock.csv', index_col='Date')
    except Exception as e:
        st.write(e)

    # stock_df = yf.download('AAPL', start=start, end=end, interval='1mo')
    # stock_df.index = stock_df.index.date

    stock_df1 = stock_df.drop(['Adj Close', 'Volume'], axis=1)

    stock_df_desc = stock_df1.describe()

    mean_stock_df2 = pd.DataFrame(stock_df_desc.mean()).T
    mean_stock_values = mean_stock_df2.values.squeeze().tolist()
    mean_stock_labels = mean_stock_df2.columns.tolist()
    mean_stock= round(stock_df_desc.loc['mean'], 3)

    stock_pct_change = stock_df1.pct_change()
    stock_pct_change_desc_df = stock_pct_change.describe()
    stock_pct_change_desc = round(stock_pct_change_desc_df.loc['mean'], 3)

    open_col, high_col, low_col, close_col = st.columns(4)
    with open_col:
        st.metric(label="Open", value=mean_stock.Open.item(), delta=stock_pct_change_desc.High.item())
    with high_col:
        st.metric(label="High", value=mean_stock.High.item(), delta=stock_pct_change_desc.High.item())
    with low_col:
        st.metric(label="Low", value=mean_stock.Low.item(), delta=stock_pct_change_desc.Low.item())
    with close_col:
        st.metric(label="Close", value=mean_stock.Close.item(), delta=stock_pct_change_desc.Close.item())

    scatter_fig = go.Figure()
    scatter_fig.add_trace(go.Scatter(
                x=stock_df.index,
                y=stock_df.Close,
                fill="tonexty",
                mode="lines",
                line_color="darkblue",
                fillgradient=dict(
                    type="vertical",
                    colorscale=[(0.0, "darkblue"), (0.5, "royalblue"), (1.0, "cyan")],
                ),
            ),)


    scatter_fig.update_layout(
        # title="Stock",
        xaxis_title="Date",
        yaxis_title="Stock",
    )

    bar_fig = px.bar(stock_df_desc.loc['mean'], x=['Open', 'High', 'Low', 'Close'], y="mean")

    bar_fig.update_layout(
        # title="Stock",
        xaxis_title="OHCL",
        yaxis_title="Mean Price",
    )

    pair_fig = px.scatter_matrix(stock_df_desc,
        dimensions=['Open', 'High', 'Low', 'Close'],
        )

    pie_fig = go.Figure(data=[go.Pie(labels=mean_stock_labels, values=mean_stock_values, hole=0.8)])

    chart1_col1, chart_col2 = st.columns(2)
    with chart1_col1:
        st.plotly_chart(scatter_fig, theme=None, use_container_width=True)

    with chart_col2:
        st.plotly_chart(bar_fig, theme=None, use_container_width=True)


    chart2_col, df1_col = st.columns(2)
    with chart2_col:
        st.plotly_chart(pie_fig, theme=None, use_container_width=True)

    with df1_col:
        st.dataframe(stock_df)


    chart3_col, df2_col = st.columns([3,1])
    with chart3_col:
        st.line_chart(stock_df, y=['Open', 'High', 'Low', 'Close'], color=["#FF0000", "#00ff00", "#0000FF", "#F06056"], use_container_width=True)

    with df2_col:
        st.dataframe(stock_df_desc)


    st.plotly_chart(pair_fig, theme=None, use_container_width=True)

with tab2:
# ======Credit Card Fraud=====
    credit_card_df = pd.read_csv('data/credit_card_fraud.csv')
    credit_card_df.drop(['Cardholder Name', 'Card Number (Hashed or Encrypted)', 'CVV Code (Hashed or Encrypted)', 'Transaction ID', 'User Account Information', 'Transaction Notes'], inplace=True, axis='columns')
    credit_card_df.columns = ['date', 'amount', 'merchant', 'MCC', 'location', 'currency', 'card_type', 'card_expiration_date', 'response_code', 'fraud_flag', 'previous_transactions', 'transaction_source', 'IP_address', 'device_information']
    credit_card_df.dropna(inplace=True)
    mean_trans_amount = credit_card_df.amount.mean()
    total_trans_amount = credit_card_df.amount.sum()

    fraud_flag_count_df = credit_card_df['fraud_flag'].value_counts()
    fraud_flag_count_df.to_frame()
    fraud_flag_count_df = fraud_flag_count_df.reset_index()
    fraud_flag_count_df.columns = ['fraud_flag', 'fraud_flag_count']

    total_col, mean_col, min_col, max_col = st.columns(4)
    with total_col:
        st.metric(label="Total transaction amount", value=round(total_trans_amount, 2))
    with mean_col:
        st.metric(label="Mean transaction", value=round(mean_trans_amount, 2))
    with min_col:
        st.metric(label="Total non-fraud transaction", value=round(fraud_flag_count_df.fraud_flag_count[0], 2))
    with max_col:
        st.metric(label="Total fraud transaction", value=round(fraud_flag_count_df.fraud_flag_count[1], 2))

    credit_card_df['month'] = pd.to_datetime(credit_card_df['date']).dt.month_name().str[:3]
    monthly_fraud_flag = pd.crosstab(credit_card_df['month'], credit_card_df['fraud_flag'])
    monthly_fraud_flag.reset_index(inplace=True)
    monthly_fraud_flag.columns = [ 'Month', 'Non fraud count', 'Fraud count']

    monthly_fraud_flag_grouped_barplot = px.bar(
        monthly_fraud_flag,
        x = "Month",
        y = ['Non fraud count', 'Fraud count'],
        barmode = 'group',
        title='Fraud flag by monthly transaction',
        color_discrete_map={
            'Non fraud count': 'blue',
            'Fraud count': 'green'
        }
    )

    monthly_fraud_flag_stacked_barplot = go.Figure(data=[
        go.Bar(name='Non fraud', x=monthly_fraud_flag.Month, y=monthly_fraud_flag['Non fraud count']),
        go.Bar(name='Fraud', x=monthly_fraud_flag.Month, y=monthly_fraud_flag['Fraud count'])
    ])
    monthly_fraud_flag_stacked_barplot.update_layout(barmode='stack', title='Fraud flag by monthly transaction')

    credit_card_df['year'] = pd.to_datetime(credit_card_df['date']).dt.year
    yearly_fraud_flag = pd.crosstab(credit_card_df['year'], credit_card_df['fraud_flag'])
    yearly_fraud_flag.reset_index(inplace=True)
    yearly_fraud_flag.columns = [ 'Year', 'Non fraud count', 'Fraud count']

    yearly_fraud_flag_grouped_barplot = go.Figure(data=[
        go.Bar(name='Non fraud', x=yearly_fraud_flag.Year, y=monthly_fraud_flag['Non fraud count']),
        go.Bar(name='Fraud', x=yearly_fraud_flag.Year, y=monthly_fraud_flag['Fraud count'])
    ])
    yearly_fraud_flag_grouped_barplot.update_layout(title='Fraud flag by yearly transaction')

    currency_fraud_flag_count = pd.crosstab(credit_card_df['currency'], credit_card_df['fraud_flag'])
    currency_fraud_flag_count.reset_index(inplace=True)
    currency_fraud_flag_count.columns = [ 'Currency', 'Non fraud count', 'Fraud count']

    currency_fraud_flag_pieplot = go.Figure(data=[go.Pie(labels=currency_fraud_flag_count.Currency, values=currency_fraud_flag_count['Fraud count'], hole=0.6)])

    device_fraud_flag = pd.crosstab(credit_card_df['device_information'], credit_card_df['fraud_flag'])
    device_fraud_flag.reset_index(inplace=True)
    device_fraud_flag.columns = [ 'Device', 'Non fraud count', 'Fraud count']

    device_fraud_flag_grouped_barplot = px.bar(
        device_fraud_flag,
        x = "Device",
        y = ['Non fraud count', 'Fraud count'],
        barmode = 'group',
        title='Fraud flag by user\'s device',
    )

    trans_source_fraud_flag = pd.crosstab(credit_card_df['transaction_source'], credit_card_df['fraud_flag'])
    trans_source_fraud_flag.reset_index(inplace=True)
    trans_source_fraud_flag.columns = [ 'Transaction source', 'Non fraud count', 'Fraud count']
    trans_source_fraud_flag_grouped_barplot = px.bar(
        trans_source_fraud_flag,
        x = "Transaction source",
        y = ['Non fraud count', 'Fraud count'],
        barmode = 'group',
        title='Fraud flag by source of transaction'
    )

    card_type_fraud_flag = pd.crosstab(credit_card_df['card_type'], credit_card_df['fraud_flag'])
    card_type_fraud_flag.reset_index(inplace=True)
    card_type_fraud_flag.columns = [ 'Card type', 'Non fraud count', 'Fraud count']
    card_type_fraud_flag_grouped_barplot = px.bar(
        card_type_fraud_flag,
        x = "Card type",
        y = ['Non fraud count', 'Fraud count'],
        barmode = 'group',
        # variable='',
        title='Fraud flag by Card type'
    )

    monthly_fraud_flag_barplot_col1, chart_col2 = st.columns([2, 1])
    with monthly_fraud_flag_barplot_col1:
        st.plotly_chart(monthly_fraud_flag_grouped_barplot, theme=None, use_container_width=True)
        st.plotly_chart(monthly_fraud_flag_stacked_barplot, theme=None, use_container_width=True)

    with chart_col2:
        st.plotly_chart(currency_fraud_flag_pieplot, theme=None, use_container_width=True)
        st.plotly_chart(yearly_fraud_flag_grouped_barplot, theme=None, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(device_fraud_flag_grouped_barplot, theme=None, use_container_width=True)

    with col2:
        st.plotly_chart(trans_source_fraud_flag_grouped_barplot, theme=None, use_container_width=True)

    with col3:
        st.plotly_chart(card_type_fraud_flag_grouped_barplot, theme=None, use_container_width=True)

    st.dataframe(credit_card_df)

