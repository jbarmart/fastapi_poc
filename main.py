from typing import Optional

from fastapi import FastAPI, HTTPException, status, Depends, Header

development_db = ["DB for Development"]


# Dependency function to get the database engine
def get_engine():
    engine = "!! sqliteActual !!"
    return engine


def get_db_session(engine=Depends(get_engine, use_cache=False)):
    print(engine)
    return development_db


# Dependency function to check for 'token' in headers
def verify_token(token: Optional[str] = Header(None)):
    #if token != "your-expected-token":
        #raise HTTPException(status_code=403, detail="Invalid token or token missing")
    return token


app = FastAPI(dependencies=[Depends(verify_token)])


@app.get("/add-item/", )
def add_item(item: str, db=Depends(get_db_session)):
    db.append(item)
    print(db)
    return {"message": f"added item {item}"}
