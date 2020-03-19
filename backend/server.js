const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');

require('dotenv').config();

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

const uri = process.env.ATLAS_URI;

mongoose.connect(uri, {useNewUrlParser: true, useCreateIndex: true});

const connection = mongoose.connection;
connection.once('open', () => {
    console.log('MONGODB database connection established correctly')
});

const resultsRouter = require('./routes/results');
const healthRouter = require('./routes/health');

app.use('/results', resultsRouter);
app.use('/health', healthRouter);
app.get('/', (req, res) =>{
    res.send('Welcome to PESHOPSPIDERS Backend')
});

app.listen(port, () =>{
   console.log(`Server is running on port: ${port}`)
});
