import express from "express";
import {result} from "../models/results_model"

export const registerRoutes = (app: express.Application) => {
    app.get("/product/id=:id", async (req, res) => {
        return res.send(await result.findById(req.params.id));
    });

    app.get("/product/search=:query", async (req, res) =>{
        return res.json(await result.find({name: req.params.query}).exec())
    });
}
