// TODO: add stars, stock

export interface ProductExpand {
    id: number;
    name: string;
    providers: Provider[]; // in order
}

export interface Product {
    id: number;
    name : string;
    imgUrl: string;
    description: string;
    providersSimple: ProviderSimple[]; // in order
}

interface Price {
    price: number;
    date:  number; // TODO: need to change
}

interface Provider {
    provider: string;
    description: string;
    url: string;
    imgUrl: string;
    prices: Price[];
}

interface ProviderSimple {
    provider: string;
    url: string;
    location: {
        lng: number;
        lat: number;
    };
    prices: Price[];  // intended to be sort.
}
