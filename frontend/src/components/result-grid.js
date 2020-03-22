import React, { Component } from 'react';
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.min.js"
import "jquery/dist/jquery.min"
import "./result_grid.css"

export default class ResultGrid extends Component{
    constructor(props) {
        super(props);
    };

    addManta(st){
        let index = st.lastIndexOf('.');
        if (index === -1) {
            st += '.00';
        }
        else {
            console.log(st + " " + st.length + " " + index);
            let toadd = Math.max(3 - (st.length-index), 0);
            st += '0'.repeat(toadd)
        }
        return st
    }

    render(){
        const results = this.props.results;
        return(
            <div className="container">
                <div className="row">
                {results.map(result => {
                        // console.log("result en result_grid" + result);
                        let html_gen = '';
                        html_gen = <div className="col-md-3">
                                    <figure className="card card-product">
                                        <div className="img-wrap" ><img src={result.img_urls.wong}/></div>
                                    <figcaption className="info-wrap">
                                        <h6 className="title" style={{textTransform: 'capitalize'}}>{result.name}</h6>
                                        <div className="rating-wrap">
                                            <div className="label-rating"></div>
                                        </div>
                                    </figcaption>
                                    <div className="bottom-wrap">
                                        <button type="button" value={JSON.stringify(result)} className="btn btn-sm btn-primary float-right" onClick={this.props.changer}>Detalles</button>
                                        <div className="price-wrap h5">
                                            <span className="price-new">s/ {this.addManta(result.sorted_prices[0][1].toString())} </span>
                                        </div>
                                    </div>
                            </figure>
                            </div> ;
                        return html_gen
                    })}
                </div>
            </div>
        )
    }
}

