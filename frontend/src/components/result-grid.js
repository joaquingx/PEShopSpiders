import React, { Component } from 'react';
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.min"
import './showresult.css'
import axios from 'axios';

export default class ResultGrid extends Component{
    constructor(props) {
        super(props);
        this.state = {
            results: [
                {
                    name: 'Nada',
                    img_urls:{
                        wong: 'Nada',
                    }
                }
            ],
        }
    };

    componentDidMount() {
        console.log('url es' + 'http://localhost:5000/results/lower=' + this.props.lower + "&upper=" + this.props.upper);
        axios.get('http://localhost:5000/results/lower=' + this.props.lower + "&upper=" + this.props.upper)
            .then(response =>{
                this.setState({
                    results: response.data,
                    // img_urls: response.data,
                    // name: response.data.name,
                })
            })
    }


    render(){
        const results = this.state.results;
        return(
            <div className="container">
                {results.map(result => <img alt={result.name} className="col-sm-4" src={result.img_urls.wong} width="150px" height="150px"/>)}
            </div>
        )
    }
}

