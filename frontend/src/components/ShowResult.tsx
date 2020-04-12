import { Product } from './InterfacesTypes';
import {useEffect, useState} from 'react'
import  * as React from 'react'
import './ShowResult.css'
import {Graph} from './Graph'
import { graphConfig, getScales, expandGraphData, providerToColor } from './graphsUtils'
import { Axis } from "./Axis";


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
                    price: 130,
                    date: new Date('04/08/2020'),
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
        document.title = product.name;
    });
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
                                                {provider_info.provider}: </span><span className="provider-price">{provider_info.prices[0].price}
                                            </span>
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
