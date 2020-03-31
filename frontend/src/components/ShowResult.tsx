import { Product } from './ProductAggregator';
import { useState } from 'react'
import  * as React from 'react'
// import "bootstrap/dist/css/bootstrap.min.css"
// import "bootstrap/dist/js/bootstrap.min"
import './showresult.css'
import * as ReactDom from 'react-dom'

function useProduct() {
    const initialState: Product = {
        name: 'Charly',
        description: 'Cosmigonon Narcisolon',
        url: 'https://es.wikipedia.org/wiki/Charly_Garc%C3%ADa',
        imgUrl: 'https://www.larata.cl/wp-content/uploads/2014/08/fito-paez-rockandrollrevolution.jpg',
        providersSimple: [
            {
                provider: 'Seminare',
                bestPrice : {
                    price: 1000000,
                    date: Date.now(),
                    location : {
                        lat: 344.62264,
                        lng: -58.44104,
                    }
                }
            }
        ]
    };
    const [product , setProduct] = useState<Product>(initialState);
    return product;
}


export default function ShowResult(): JSX.Element {
    const product = useProduct();

    return (
        <div className="container">
            <div className="row">
                <div className='col-sm-4 item-photo'>
                    <img style={{maxWidth: "100%"}}
                         src={product.imgUrl}/>
                </div>
                <div className="col-sm-8" style={{border:"0px solid gray"}}>
                    <h3 style={{textTransform: 'capitalize'}}>{product.name}</h3>
                    <h6 className="title-price"><small>PRECIO</small></h6>
                    {
                        product.providersSimple.map(provider => {
                            return (<p>
                                <span style={{textTransform: 'capitalize'}}>
                                    {provider.provider}
                                </span>: {provider.bestPrice.price}
                            </p>)
                        })
                    }
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
                        <button className="btn btn-success" onClick={() => {console.log('button doing nothing!')}} ><span style={{marginRight:"20px"}}
                                                                                                className="glyphicon glyphicon-shopping-cart"
                                                                                                aria-hidden="true"></span> Regresar
                        </button>
                        <h6><a href="#"><span className="glyphicon glyphicon-heart-empty"
                                              style={{cursor: "pointer"}}></span> Agregar a lista de deseos</a></h6>
                    </div>
                </div>
            </div>
        </div>
    )
};
