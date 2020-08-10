import express from "express";
import mongoose from "mongoose"
import cors from "cors";
import dotenv from "dotenv";
import * as productRoutes from "./routes/productRoutes";
import * as clusterizedRoutes from "./routes/clusterizedRoutes";

dotenv.config();

const app = express();
const port = process.env.PORT || 5000;

app.use(express.json());
app.use(cors())

mongoose.connect(process.env.ATLAS_URI, {useNewUrlParser: true, useCreateIndex: true});
const connection = mongoose.connection;
connection.once('open', () => {
    console.log('MONGODB database connection established correctly')
});


app.get('/', (req: express.Request, res: express.Response) =>{
    res.send('Welcome to PESHOP Backend');
});

productRoutes.registerRoutes(app);
clusterizedRoutes.registerRoutes(app);

app.listen(port, () =>{
    // tslint:disable-next-line:no-console
    console.log(`Server is running on port: ${port}`)
});
