import express from "express";

export const registerRoutes = (app: express.Application) => {
    app.get("/clusterized/:name", async (req, res) => {
        res.send({})
    });
}
