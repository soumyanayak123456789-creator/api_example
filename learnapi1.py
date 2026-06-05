from fastapi import FastAPI
import model_database
from database import engine
from config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
from routers import posts, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware
model_database.Base.metadata.create_all(bind=engine)



# while True:
#     try:
#         conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='123456789', cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connection successful")
#         break

#     except Exception as error:
#         print("Database connection failed", error)
#         cursor.close()
#         conn.close()
#         time.sleep(2)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello and Welcome to this universe!!!"}

