import { Schema, model } from "mongoose";

const resultSchema = new Schema({
    "name": String,
    "price": String,
    "url": String,
    "img_url": String,
    "stars": String,
    "stock": String,
    "currency": String,
    "spider": String,
});

export const result = model("result", resultSchema);
