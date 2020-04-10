import { graphData, Product } from './ProductAggregator';
import {useEffect, useState} from 'react'
import  * as React from 'react'
import './ShowResult.css'
import * as d3 from 'd3'
import {Graph} from './Graph'

let sanitizeGraphData = (d: any): graphData => {
    return {date: d3.timeParse("%Y-%m-%d")(d.date) as Date, price: d.price}
};

let getGraphData = (product: Product): graphData[][] => {
    const prices = product.providersSimple.map(ps => ps.prices);
    return prices;
};

function useProduct() {
    const initialState: Product = {
        id: 1,
        name: 'Charly',
        description: 'Cosmigonon Narcisolon',
        imgUrl: 'https://www.larata.cl/wp-content/uploads/2014/08/fito-paez-rockandrollrevolution.jpg',
        providersSimple: [
            {
                provider: 'Seminare',
                url: 'https://www.youtube.com/watch?v=xVdtGR_zgdA',
                location : {
                    lat: 344.62264,
                    lng: -58.44104,
                },
                prices : [{
                    price: 100,
                    date: new Date(),
                }, {
                        price: 150,
                        date: new Date("04/08/2020"),
                },{
                        price: 90,
                        date: new Date("04/07/2020"),
                    }
                ],
            },
            {
                provider: 'Seru Giran',
                url: 'https://www.youtube.com/watch?v=2P3YX2i782I',
                location : {
                    lat: 344.62264,
                    lng: -58.44104,
                },
                prices : [{
                    price: 200,
                    date: new Date(),
                }],
            }

        ]
    };
    const [product , setProduct] = useState<Product>(initialState);
    return product;
}


export default function ShowResult(): JSX.Element {
    const product = useProduct();
    useEffect(() => {
        document.title = `Hola!`;
    });
    console.log(getGraphData(product));
    return (
        <div className="result-container">
            <div className="name-img-container">
                <a className="try"><img  className="img-product" src={product.imgUrl}/></a>
                <div className="name-prices-container">
                    <p className="name-product">{product.name}</p>
                    <div className="prices-container">
                        {
                            product.providersSimple.map((provider_info, index) => {
                                return(
                                    <div key={index}><a href={provider_info.url}>
                                        <span >{provider_info.provider}: </span><span className="provider-price">{provider_info.prices[0].price}</span>
                                        </a>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
            <div className="insight-container">
                {
                    getGraphData(product).map((graphData: graphData[], index) => <Graph items={graphData}/>)
                }
                {/*<Graph items={getGraphData()}/>*/}
            </div>
        </div>
    )
};
