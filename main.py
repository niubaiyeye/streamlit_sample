import streamlit as st
import pandas as pd
import io
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from WindPy import w
import time
class excel_update(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
    def on_modified(self, event):
        if event.src_path.endswith('.xlsx'):
            self.callback()

def app():

    xlsx_path = 'C:\\Users\\h\\Desktop\\FuturesData.xlsx'

    # 更新应用程序
    def load_xlsx_data():
        df = pd.read_excel(xlsx_path)
        return df

    def update_app():
        df = load_xlsx_data()
        if df is not None:
            st.dataframe(df)


    event_handler = excel_update(update_app)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(xlsx_path), recursive=False)
    observer.start()




    update_app()

    def stop_observer():
        observer.stop()
        observer.join()



def stock_data(trade_data):
    global stock_1, stock_2
    sec_code = trade_data.Codes
    time = trade_data.Times
    price = trade_data.Data
    stock_1 = price[0][0]
    print(time)

def process_wsq_data(data):
    table_data = pd.DataFrame({'time': data.Times, 'stock_code': data.Codes, 'price': data.Data[0]})
    return table_data

def run():
    table_container = st.container()
    while True:
        # w.wsq("000002.SZ,00001.SZ", 'rt_close', func=stock_data)
        data = w.wsq("000002.SZ", 'rt_last')
        print(data)
        table_data = process_wsq_data(data)

        with table_container:
            st.dataframe(table_data)
        time.sleep(0.2)
        st.rerun()


if __name__ == "__main__":
    #app()
    w.start()
    w.isconnected()
    run()


