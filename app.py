import streamlit as st

def main():
    st.set_page_config(
        page_title='US Risk Dashboard',
        page_icon='✅',
        layout='wide'
    )

    st.sidebar.title("Navigation")
    pages = {
        "Dashboard": dashboard,
        "Customer Sales Trend": customer_sales_trend,
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()

def dashboard():
    from dashboard import render_dashboard
    render_dashboard()

def customer_sales_trend():
    st.title("Customer Sales Trend")
    # Add customer sales trend content here

if __name__ == "__main__":
    main()
