import express from "express";
import axios from "axios";
// import URL from "URL";

let flask_api = "http://localhost:5002"

export const registerRoutes = (app: express.Application) => {
    app.get("/clusterized/", async (req, res) => {
        const  getUrl = (flask_url: string, name: string, sim: string) => {
            const url = new URL(flask_api);
            url.searchParams.append("input", name);
            url.searchParams.append("threshold", sim);
            return url;
        }
        const url = getUrl(flask_api, req.query.search as string, req.query.sim as string);
        try {
            let response = await axios.get(url.href);
            if (response.status == 200) {
                res.send(response.data);
            } else {
                res.send({"error": "Server error"});
            }
        } catch(error) {
            res.send({"error": "Unexpected error, probably in upstream"})
        }
    });
}
