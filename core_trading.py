
# # For now hardcoded (later move to vault/env)

# # core_trading.py
# from kiteconnect import KiteConnect
# import re
# from datetime import datetime, time
# import os

# # Use environment variables for security
# API_KEY = "p04e63vptv9shd2m"
# ACCESS_TOKEN = "MrwiUoPhgqes0E4qIE43awvQSLr236eu"
# if not API_KEY or not ACCESS_TOKEN:
#     raise ValueError("Missing KITE_API_KEY or KITE_ACCESS_TOKEN environment variables")

# kite = KiteConnect(api_key=API_KEY)
# kite.set_access_token(ACCESS_TOKEN)

# STOCK_SYMBOLS = {
#     "hdfc": "HDFCBANK",
#     "icici": "ICICIBANK",
#     "reliance": "RELIANCE",
#     "tcs": "TCS",
#     "infosys": "INFY",
#     "sbin": "SBIN",
#     "bharti": "BHARTIARTL",
#     "itc": "ITC",
#     "axis": "AXISBANK",
#     "kotak": "KOTAKBANK",
#     "yesbank":"YESBANK",

# }

# def market_open():
#     """Check if market is currently open"""
#     now = datetime.now()
    
#     # Check if weekend
#     if now.weekday() >= 5:  # Saturday=5, Sunday=6
#         return False
    
#     current_time = now.time()
#     # NSE trading hours: 9:15 AM to 3:30 PM IST
#     return time(9, 15) <= current_time <= time(15, 30)

# def extract_qty(text):
#     """Extract quantity from command text"""
#     m = re.search(r"\d+", text)
#     return int(m.group()) if m else 1

# def extract_symbol(text):
#     """Extract stock symbol from command text"""
#     text = text.lower()
#     for k, v in STOCK_SYMBOLS.items():
#         if k in text:
#             return v
#     return None

# def place_trade(command: str):
#     """
#     Place a trade using natural language command
#     Example: "buy 10 hdfc" or "sell 5 reliance"
#     """
#     try:
#         if not market_open():
#             return {
#                 "error": "Market is closed",
#                 "message": "NSE trading hours: Mon-Fri 9:15 AM - 3:30 PM IST"
#             }

#         text = command.lower()

#         # Determine transaction type
#         if "buy" in text:
#             txn = kite.TRANSACTION_TYPE_BUY
#             txn_type = "BUY"
#         elif "sell" in text:
#             txn = kite.TRANSACTION_TYPE_SELL
#             txn_type = "SELL"
#         else:
#             return {"error": "Specify BUY or SELL in your command"}

#         # Extract stock symbol
#         symbol = extract_symbol(text)
#         if not symbol:
#             return {
#                 "error": "Stock not recognized",
#                 "available_stocks": list(STOCK_SYMBOLS.keys())
#             }

#         # Extract quantity
#         qty = extract_qty(text)

#         # Place order
#         order_id = kite.place_order(
#             variety=kite.VARIETY_REGULAR,
#             exchange=kite.EXCHANGE_NSE,
#             tradingsymbol=symbol,
#             transaction_type=txn,
#             quantity=qty,
#             order_type=kite.ORDER_TYPE_MARKET,
#             product=kite.PRODUCT_CNC,
#         )

#         return {
#             "status": "success",
#             "order_id": order_id,
#             "symbol": symbol,
#             "quantity": qty,
#             "transaction_type": txn_type,
#             "order_type": "MARKET",
#             "product": "CNC"
#         }
    
#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e),
#             "message": "Trade placement failed"
#         }

# def get_quote(symbol: str):
#     """
#     Get live quote for a stock symbol
#     Example: get_quote("HDFCBANK")
#     """
#     try:
#         # Ensure symbol is uppercase for NSE
#         symbol = symbol.upper()
        
#         # Fetch quote from Kite API
#         quote_data = kite.quote(f"NSE:{symbol}")
#         q = quote_data[f"NSE:{symbol}"]
        
#         return {
#             "status": "success",
#             "symbol": symbol,
#             "last_price": q["last_price"],
#             "open": q["ohlc"]["open"],
#             "high": q["ohlc"]["high"],
#             "low": q["ohlc"]["low"],
#             "close": q["ohlc"]["close"],
#             "volume": q.get("volume", 0),
#             "last_trade_time": q.get("last_trade_time", "")
#         }
    
#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e),
#             "message": f"Failed to fetch quote for {symbol}"
#         }

# def get_positions():
#     """Get current positions"""
#     try:
#         positions = kite.positions()
#         return {
#             "status": "success",
#             "net_positions": positions.get("net", []),
#             "day_positions": positions.get("day", [])
#         }
#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e),
#             "message": "Failed to fetch positions"
#         }

# def get_orders():
#     """Get order history"""
#     try:
#         orders = kite.orders()
#         return {
#             "status": "success",
#             "orders": orders
#         }
#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e),
#             "message": "Failed to fetch orders"
#         }
# core_trading.py

from kiteconnect import KiteConnect
import re
from datetime import datetime, time
import os

# Use environment variables for security
API_KEY = "p04e63vptv9shd2m"
ACCESS_TOKEN = "MrwiUoPhgqes0E4qIE43awvQSLr236eu"

if not API_KEY or not ACCESS_TOKEN:
    raise ValueError("Missing KITE_API_KEY or KITE_ACCESS_TOKEN environment variables")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

STOCK_SYMBOLS = {
    "hdfc": "HDFCBANK",
    "icici": "ICICIBANK",
    "reliance": "RELIANCE",
    "tcs": "TCS",
    "infosys": "INFY",
    "sbin": "SBIN",
    "bharti": "BHARTIARTL",
    "itc": "ITC",
    "axis": "AXISBANK",
    "kotak": "KOTAKBANK",
}

# Indian Stock Market Indices
INDICES = {
    "NIFTY 50": "NSE:NIFTY 50",
    "NIFTY BANK": "NSE:NIFTY BANK",
    "SENSEX": "BSE:SENSEX",
    "NIFTY IT": "NSE:NIFTY IT",
    "NIFTY FIN SERVICE": "NSE:NIFTY FIN SERVICE",
    "NIFTY MIDCAP 50": "NSE:NIFTY MIDCAP 50",
    "NIFTY NEXT 50": "NSE:NIFTY NEXT 50",
    "INDIA VIX": "NSE:INDIA VIX",
}

def market_open():
    """Check if market is currently open"""
    now = datetime.now()
    
    # Check if weekend
    if now.weekday() >= 5:  # Saturday=5, Sunday=6
        return False
    
    current_time = now.time()
    # NSE trading hours: 9:15 AM to 3:30 PM IST
    return time(9, 15) <= current_time <= time(15, 30)

def extract_qty(text):
    """Extract quantity from command text"""
    m = re.search(r"\d+", text)
    return int(m.group()) if m else 1

def extract_symbol(text):
    """Extract stock symbol from command text"""
    text = text.lower()
    for k, v in STOCK_SYMBOLS.items():
        if k in text:
            return v
    return None

def place_trade(command: str):
    """
    Place a trade using natural language command
    Example: "buy 10 hdfc" or "sell 5 reliance"
    """
    try:
        if not market_open():
            return {
                "error": "Market is closed",
                "message": "NSE trading hours: Mon-Fri 9:15 AM - 3:30 PM IST"
            }

        text = command.lower()

        # Determine transaction type
        if "buy" in text:
            txn = kite.TRANSACTION_TYPE_BUY
            txn_type = "BUY"
        elif "sell" in text:
            txn = kite.TRANSACTION_TYPE_SELL
            txn_type = "SELL"
        else:
            return {"error": "Specify BUY or SELL in your command"}

        # Extract stock symbol
        symbol = extract_symbol(text)
        if not symbol:
            return {
                "error": "Stock not recognized",
                "available_stocks": list(STOCK_SYMBOLS.keys())
            }

        # Extract quantity
        qty = extract_qty(text)

        # Place order
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=txn,
            quantity=qty,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_CNC,
        )

        return {
            "status": "success",
            "order_id": order_id,
            "symbol": symbol,
            "quantity": qty,
            "transaction_type": txn_type,
            "order_type": "MARKET",
            "product": "CNC"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Trade placement failed"
        }

def get_quote(symbol: str):
    """
    Get live quote for a stock symbol
    Example: get_quote("HDFCBANK")
    """
    try:
        # Ensure symbol is uppercase for NSE
        symbol = symbol.upper()
        
        # Fetch quote from Kite API
        quote_data = kite.quote(f"NSE:{symbol}")
        q = quote_data[f"NSE:{symbol}"]
        
        return {
            "status": "success",
            "symbol": symbol,
            "last_price": q["last_price"],
            "open": q["ohlc"]["open"],
            "high": q["ohlc"]["high"],
            "low": q["ohlc"]["low"],
            "close": q["ohlc"]["close"],
            "volume": q.get("volume", 0),
            "last_trade_time": q.get("last_trade_time", "")
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to fetch quote for {symbol}"
        }

def get_positions():
    """Get current positions"""
    try:
        positions = kite.positions()
        return {
            "status": "success",
            "net_positions": positions.get("net", []),
            "day_positions": positions.get("day", [])
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to fetch positions"
        }

def get_orders():
    """Get order history"""
    try:
        orders = kite.orders()
        return {
            "status": "success",
            "orders": orders
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to fetch orders"
        }

def get_all_indices():
    """Get live data for all major Indian indices"""
    try:
        # Get quotes for all indices
        index_symbols = list(INDICES.values())
        quotes = kite.quote(index_symbols)
        
        indices_data = []
        for name, symbol in INDICES.items():
            if symbol in quotes:
                q = quotes[symbol]
                
                # Calculate change and percentage
                last_price = q.get("last_price", 0)
                prev_close = q["ohlc"].get("close", 0)
                
                if prev_close > 0:
                    change = last_price - prev_close
                    change_percent = (change / prev_close) * 100
                else:
                    change = 0
                    change_percent = 0
                
                indices_data.append({
                    "name": name,
                    "symbol": symbol,
                    "last_price": last_price,
                    "open": q["ohlc"].get("open", 0),
                    "high": q["ohlc"].get("high", 0),
                    "low": q["ohlc"].get("low", 0),
                    "close": prev_close,
                    "change": round(change, 2),
                    "change_percent": round(change_percent, 2),
                    "timestamp": q.get("last_trade_time", "")
                })
        
        return {
            "status": "success",
            "indices": indices_data,
            "market_open": market_open(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to fetch indices data"
        }