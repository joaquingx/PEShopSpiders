import { graphData, Product, ScaleD3 } from './InterfacesTypes'
import * as d3 from 'd3'

export const graphConfig = {
    width: 800,
    height: 400,
    margin: {
        left: 50,
        top: 50,
        bottom: 50,
        right: 50,
    }
};


export const providerToColor = {
    wong: '#c2185b',
    metro: '#4a0072',
    Seminare: '#283593',
    'Seru Giran': '#2e7d32'
};

export const sanitizeGraphData = (d: any): graphData => {
    return {date: d3.timeParse("%Y-%m-%d")(d.date) as Date, price: d.price}
};

export const getGraphData = (product: Product): graphData[][] => {
    const prices = product.providersSimple.map(ps => ps.prices);
    return prices;
};

export const expandGraphData = (graphData: graphData[][]): graphData[] => {
    let plainGraphData: graphData[] = [];
    graphData.map(p => {
        plainGraphData = plainGraphData.concat(p); // is this efficient?
    });
    return plainGraphData;
};

export const getScales = (graphData: graphData[]): [ScaleD3, ScaleD3] => {
    let xScale = d3.scaleTime().range([graphConfig.margin.left, graphConfig.width - graphConfig.margin.right]);
    let yScale = d3.scaleLinear().range([graphConfig.height - graphConfig.margin.top, graphConfig.margin.bottom]);
    xScale.domain(d3.extent(graphData, d => d.date) as [Date, Date]);
    yScale.domain(d3.extent(graphData, d => d.price) as [number, number]);
    return [xScale, yScale];
};
