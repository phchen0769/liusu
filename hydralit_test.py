#when we import hydralit, we automatically get all of Streamlit
import hydralit as hy
from streamlit_test import show_tables

app = hy.HydraApp(title='Simple Multi-Page App')

@app.addapp()
def my_home():
    hy.info('Hello from app1')
    show_tables()

@app.addapp()
def app2():
    hy.info('Hello from app 2')

@app.addapp()
def app3():
    hy.info('Hello from app 2')

@app.addapp()
def app4():
    hy.info('Hello from app 2')
    
#Run the whole lot, we get navbar, state management and app isolation, all with this tiny amount of work.
app.run()