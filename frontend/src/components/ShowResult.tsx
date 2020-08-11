import { Product } from './InterfacesTypes';
import {useEffect, useState} from 'react'
import  * as React from 'react'
import { useLocation } from "react-router-dom";
import './ShowResult.css'
import {Graph} from './Graph'
import { graphConfig, getScales, expandGraphData, providerToColor } from './graphsUtils'
import { Axis } from "./Axis";
import axios from "axios";

export interface ClusterParams {
    name: string,
    threshold: string,
}

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
                    date: new Date('04/10/2020'),
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
                    date: new Date('04/10/2020'),
                }, {
                    price: 300,
                    date: new Date('04/08/2020'),
                }],
            },
            {
                provider: 'wong',
                url: 'https://www.youtube.com/watch?v=2P3YX2i782I',
                location : {
                    lat: 344.62264,
                    lng: -58.44104,
                },
                prices : [{
                    price: 120,
                    date: new Date('04/10/2020'),
                }, {
                    price: 200,
                    date: new Date('04/08/2020'),
                }],
            }
        ]
    };
    const [product , setProduct] = useState<Product>(initialState);
    return {
        product,
        setProduct
    };
}
function useQuery() {
    return new URLSearchParams(useLocation().search);
}

export const ShowResult = () => {
    const ss = useProduct()
    const product = ss["product"];
    const query = useQuery();
    useEffect(() => {
        document.title = product.name;
    });
    useEffect(() => {
        const fetchData = async () => {
            const url = new URL(`http://localhost:8080/clusterized/?search=${query.get("name")}&sim=${query.get("threshold")}`)
            const result = await axios.get(url.href);
            let cleanResult = result.data;
            ss["setProduct"](cleanResult);
        }
        fetchData();
    })
    let expandedGraphData = expandGraphData(product.providersSimple.map(p => p.prices));
    const [xScale, yScale] = getScales(expandedGraphData);
    return (
        <div className="result-container">
            <div className="name-img-container">
                <a className="try"><img alt="product image" className="img-product" src={product.imgUrl}/></a>
                <div className="name-prices-container">
                    <p className="name-product">{product.name}</p>
                    <div className="prices-container">
                        {
                            product.providersSimple.map((provider_info, index) => {
                                return(
                                    <div key={index}><a href={provider_info.url}>
                                            <span >
                                                <span style={{color: providerToColor[provider_info.provider], fontSize: '27px'}}>■ </span>
                                                {provider_info.provider}: </span>
                                                <span className="provider-price">{provider_info.prices[provider_info.prices.length-1].price}</span>
                                        </a>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
            <div className="insight-container">
                <svg width={graphConfig.width} height={graphConfig.height}>
                    <Axis xScale={xScale} yScale={yScale}/>
                {
                    product.providersSimple.map((provider, index) => {
                        return <Graph
                            key={index}
                            items={provider.prices} xScale={xScale} yScale={yScale} mainColor={providerToColor[provider.provider]}
                        />
                    })
                }
                </svg>
            </div>
        </div>
    )
};
