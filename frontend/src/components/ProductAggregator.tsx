// TODO: add stars, stock

export interface ProductExpand {
    name: string;
    providers: Provider[];
}

export interface Product {
    name : string;
    url: string;
    imgUrl: string;
    description: string;
    providersSimple: ProviderSimple[];
}

interface Price {
    price: number;
    date:  number; // TODO: need to change
    location: {
        lng: number;
        lat: number;
    };
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
    bestPrice: Price;
}
