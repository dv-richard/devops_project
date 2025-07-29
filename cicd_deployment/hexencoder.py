#!/usr/bin/python3
import codecs
from fastapi import FastAPI

# FastAPI app instance
app = FastAPI()

# hexencoder API
@app.get("/encode/{text}")
def hex_encode_text(text: str):
    return codecs.getencoder('hex')(text.encode())[0].decode('ascii')

@app.get("/decode/{text}")
def hex_decode_text(text: str):
    return codecs.getdecoder('hex')(text.encode())[0].decode('utf-8')
