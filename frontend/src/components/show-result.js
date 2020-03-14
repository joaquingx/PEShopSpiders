import React, { Component } from 'react';
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.min"
import './showresult.css'
import axios from 'axios';

export default class ShowResult extends Component{
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            card_prices: [],
            online_prices: [],
            descriptions: [],
            stocks: [],
            urls: [],
            starss: [],
            img_urls: [{"img_url": ""}],
            sorted_prices: [],
        }
    }

    componentDidMount() {
        axios.get('http://localhost:5000/results/' + this.props.match.params.id)
            .then(response => {
                this.setState({
                    card_prices: response.data.card_prices,
                    regular_prices: response.data.regular_prices,
                    online_prices: response.data.online_prices,
                    descriptions: response.data.descriptions,
                    name: response.data.name,
                    stocks: response.data.stocks,
                    urls: response.data.urls,
                    starss: response.data.starss,
                    img_urls: response.data.img_urls,
                    sorted_prices: response.data.sorted_prices,
                });
            })
            .catch(error => console.log(error));
    }

    render(){

        const item = [];
        const prices = this.state.sorted_prices;
        for (const value of prices) {
            item.push([value[0], value[1]]);
        }
        const img_url = this.state.img_urls.wong;

        return (
            <div className="container">
                <div className="row">
                    <div className='col-sm-4 item-photo'>
                        <img style={{maxWidth: "100%"}}
                             src={img_url}/>
                    </div>
                    <div className="col-sm-8" style={{border:"0px solid gray"}}>
                        <h3 style={{textTransform: 'capitalize'}}>{this.state.name}</h3>
                        <h6 className="title-price"><small>PRECIO</small></h6>
                        {item.map(price => <p><span style={{textTransform: 'capitalize'}}>{price[0]}</span>: {price[1]}</p>)}
                        <div className="section">
                            <h6 className="title-attr" style={{marginTop: "15px"}}><small>COLOR</small></h6>
                            <div>
                                <div className="attr" style={{width:"25px", background:"#5a5a5a"}}></div>
                                <div className="attr" style={{width:"25px", background: "white"}}></div>
                            </div>
                        </div>
                        <div className="section" style={{paddingBottom:"5px"}}>
                            <h6 className="title-attr"><small>CAPACIDAD</small></h6>
                            <div>
                                <div className="attr2">16 GB</div>
                                <div className="attr2">32 GB</div>
                            </div>
                        </div>
                        <div className="section" style={{paddingBottom: "20px"}}>
                            <h6 className="title-attr"><small>CANTIDAD</small></h6>
                            <div>
                                <div className="btn-minus"><span className="glyphicon glyphicon-minus"></span></div>
                                <input value="1"/>
                                <div className="btn-plus"><span className="glyphicon glyphicon-plus"></span></div>
                            </div>
                        </div>

                        <div className="section" style={{paddingBottom: "20px"}}>
                            <button className="btn btn-success"><span style={{marginRight:"20px"}}
                                                                      className="glyphicon glyphicon-shopping-cart"
                                                                      aria-hidden="true"></span> Agregar al carro
                            </button>
                            <h6><a href="#"><span className="glyphicon glyphicon-heart-empty"
                                                  style={{cursor: "pointer"}}></span> Agregar a lista de deseos</a></h6>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
