import React, { Component } from 'react';
import {BrowserRouter as Router, Route} from "react-router-dom"
import "bootstrap/dist/css/bootstrap.min.css"

import ShowResult from "./components/show-result"
import ResultGrid from "./components/result-grid";
import Header from "./components/header"
import axios from 'axios'

export default class App extends  Component{
    constructor(props) {
        super(props);
        this.state = {
            initialLower:  0,
            initialUpper: 20,
            results: [
                {
                    name: 'Dummy Value',
                    img_urls:{
                        wong: 'Dummy Value',
                    },
                    sorted_prices:[[0, 1 ], [0, 1]],

                }
            ],
            result: {
                name: '',
                card_prices: [],
                online_prices: [],
                descriptions: [],
                stocks: [],
                urls: [],
                starss: [],
                img_urls: [{"img_url": ""}],
                sorted_prices: [],
            },
            detail: false,
        };
        this.searchHandler = this.searchHandler.bind(this);
        this.changeDetailState = this.changeDetailState.bind(this);
        this.changeGridState = this.changeGridState.bind(this);
    }

    componentDidMount() {
        console.log('url es' + 'http://localhost:5000/results/lower=' + this.state.initialLower + "&upper=" + this.state.initialUpper);
        axios.get('http://localhost:5000/results/lower=' + this.state.initialLower + "&upper=" + this.state.initialUpper)
            .then(response =>{
                this.setState({
                    results: response.data,
                })
            });
    }

    searchHandler(event){
        console.log('Usando search handler!' + event.target.value);
        axios.get('http://localhost:5000/results/search=' + event.target.value)
            .then(response =>{
                this.setState({
                    results: response.data,
                })
            })
    }

    changeDetailState(event){
        console.log("result %s", JSON.parse(event.target.value));
        this.setState({
                detail: true,
                result: JSON.parse(event.target.value),
            }
        )
    }

    changeGridState(){
        this.setState({
            detail: false,
        })
    }


    render() {
        return (
            <div className="container">
                <Header handler={this.searchHandler}></Header>
                <div className="row">
                    <div className="col-sm-12">
                        {
                            this.state.detail ? <ShowResult changer={this.changeGridState} result={this.state.result}></ShowResult> : <ResultGrid results={this.state.results} changer={this.changeDetailState}></ResultGrid>
                        }
                    </div>
                </div>
            </div>
        );
    }
}

// export default App;
