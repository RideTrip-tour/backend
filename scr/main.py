from fastapi import FastAPI

from scr.v1 import router_v1

app = FastAPI(title='RideTrip_tour')


app.include_router(
    router_v1,
    prefix='/v1',
)