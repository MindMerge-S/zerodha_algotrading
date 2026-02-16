# api_server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from core_trading import place_trade, get_quote, get_positions, get_orders,get_all_indices

app = FastAPI(title="Zerodha Trading API", version="1.0.0")

# CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#changes
# Request models
class TradeCommand(BaseModel):
    command: str

class QuoteRequest(BaseModel):
    symbol: str

# Root endpoint
@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Zerodha Trading API is running",
        "version": "1.0.0",
        "endpoints": {
            "POST /trade": "Place a trade using natural language",
            "POST /quote": "Get live stock quote",
            "GET /positions": "Get current positions",
            "GET /orders": "Get order history"
        }
    }

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Zerodha Trading API"
    }

# Place trade endpoint
@app.post("/trade")
def trade(cmd: TradeCommand):
    """
    Place a trade using natural language command
    Example: {"command": "buy 10 hdfc"}
    """
    if not cmd.command or not cmd.command.strip():
        raise HTTPException(status_code=400, detail="Command cannot be empty")
    
    result = place_trade(cmd.command)
    
    # If there's an error in the result, return appropriate HTTP status
    if result.get("status") == "error" or "error" in result:
        return result  # Return error as JSON, don't raise HTTP exception
    
    return result

# Get quote endpoint
@app.post("/quote")
def quote(req: QuoteRequest):
    """
    Get live quote for a stock
    Example: {"symbol": "HDFCBANK"}
    """
    if not req.symbol or not req.symbol.strip():
        raise HTTPException(status_code=400, detail="Symbol cannot be empty")
    
    result = get_quote(req.symbol)
    
    if result.get("status") == "error":
        return result
    
    return result

# Get positions endpoint
@app.get("/positions")
def positions():
    """Get current trading positions"""
    result = get_positions()
    return result

# Get orders endpoint
@app.get("/orders")
def orders():
    """Get order history"""
    result = get_orders()
    return result

# Get all indices endpoint
@app.get("/indices")
def indices():
    """Get live data for all major Indian indices"""
    result = get_all_indices()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)