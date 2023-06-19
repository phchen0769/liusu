# when we import hydralit, we automatically get all of Streamlit
import hydralit as hy
from index import main

app = hy.HydraApp(title="Simple Multi-Page App")


@app.addapp()
def my_home():
    hy.info("Hello from app1")
    hy.button("btn")


@app.addapp()
def app2():
    main()


@app.addapp()
def app3():
    hy.info("Hello from app3")


@app.addapp()
def app4():
    hy.info("Hello from app 4")


app.run()
