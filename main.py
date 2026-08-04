#API 
from fastapi import FastAPI, Path, HTTPException, BackgroundTasks
from fastapi.concurrency import run_in_threadpool
import uvicorn
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import psycopg2
import os
import pipeline
from sqlalchemy.pool import NullPool
import multiprocessing 

app = FastAPI()

#connect to the database
load_dotenv()
db_password = os.getenv("POSTGRES_PASSWORD")
db_url = f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/steam"
engine = create_engine(db_url, poolclass = NullPool)

@app.get("/")
def root():
    return {"status": 200}

#get specific game information
@app.get("/api/games/search/{game_name}")
def get_game(game_name : str = Path(description = "Name of the game you would like to see the information of: ")):
    query = text("""
        SELECT g.developer, gp.price, gp.discount_pct, gp.discount, gp.total_reviews, gp.positive_reviews FROM
        steam_games g JOIN steam_price_history gp ON g.game_id = gp.game_id WHERE g.game_name = :game_name 
        ORDER BY gp.snapshot_id DESC LIMIT 1;
    """)
    with engine.begin() as conn:
        result = conn.execute(query, {"game_name":game_name}).mappings().all()

    if not result:
        raise HTTPException(status_code = 404, detail = "Game Not Found")

    return {"game_name": game_name, "data": list(result)}

@app.get("/api/games/top_discounts")
def get_discounts():
    query = text("""SELECT DISTINCT g.game_name, g.developer, gp.price, gp.discount, gp.discount_pct FROM
                    steam_games g JOIN steam_price_history gp ON g.game_id = gp.game_id WHERE 
                    gp.total_reviews > 5000 AND gp.discount_pct > 0 ORDER BY gp.discount_pct DESC LIMIT 100;
    """)

    with engine.begin() as conn:
        result = conn.execute(query).mappings().all()

    if not result:
        raise HTTPException(status_code = 404, detail = "Unable to retrieve")
    return {"top_discounts": [dict(row) for row in result]}

@app.get("/api/games/top_reviews/")
def get_reviews():
    query = text("""SELECT DISTINCT g.game_name, g.developer, gp.total_reviews, gp.positive_reviews_pct FROM steam_games g JOIN 
    steam_price_history gp ON g.game_id = gp.game_id WHERE 
                    gp.total_reviews > 5000 ORDER BY gp.positive_reviews_pct DESC LIMIT 100;
    """)

    with engine.begin() as conn:
            result = conn.execute(query).mappings().all()
    
    if not result:
        raise HTTPException(status_code = 404, detail = "Unable to retrieve")
    return {"top_reviews" : [dict(row) for row in result]}


@app.get("/api/games/price_history/{game_name}")
def get_game_price_history(game_name : str = Path(description = "Name of the game you would like to see the information of: ", gt = 0)):
    query = text("""
        SELECT g.name, gp.price, gp.discount_pct, gp.discount FROM
        steam_games g JOIN steam_price_history gp ON g.game_id = gp.game_id WHERE g.name = :game_name 
        ORDER BY gp.snapshot_id DESC LIMIT 5;
    """)
    with engine.begin() as conn:
        result = conn.execute(query, {"game_name":game_name}).mappings().all()

    if not result:
        raise HTTPException(status_code = 404, detail = "Game Not Found")

    return {"game_name": game_name, "data": list(result)}


#endpoint to refresh web scraping
@app.post("/api/admin/run_etl_pipeline")
async def run_etl_pipeline(background_tasks: BackgroundTasks):
    p = multiprocessing.Process(target = pipeline.main)
    p.start()
    return {"status": "running in the background"}
    
@app.get("/health")
def health_check():
    return {"status":"up and running"}