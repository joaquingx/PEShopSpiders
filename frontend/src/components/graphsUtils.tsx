import { Price, ScaleD3 } from './InterfacesTypes'
import * as d3 from 'd3'

export const graphConfig = {
    width: 600,
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
    adidas: '#000',
    ripley: "#33F6FF",
    oechsle: "#FF8A33",
    'Seru Giran': '#2e7d32'
};

export const expandGraphData = (graphData: Price[][]): Price[] => {
    let plainGraphData: Price[] = [];
    graphData.map(p => {
        plainGraphData = plainGraphData.concat(p);
    });
    return plainGraphData;
};

export const getScales = (graphData: Price[]): [ScaleD3, ScaleD3] => {
    let xScale = d3.scaleTime().range([graphConfig.margin.left, graphConfig.width - graphConfig.margin.right]);
    let yScale = d3.scaleLinear().range([graphConfig.height - graphConfig.margin.top, graphConfig.margin.bottom]);
    const tt = [
        {date: new Date('04/20/2020')},
        {date: new Date('04/30/2020')},
    ];
    // graphData.map()
    // console.log(graphData);
    graphData.map( (value, index) => {
        value["date"] = new Date(value["date"]);
    })
    // console.log(d3.extent(graphData, d => d.date) as [Date, Date]);
    // console.log(d3.extent(tt, d => d.date) as [Date, Date]);
    xScale.domain(d3.extent(graphData, d => d.date) as [Date, Date]);
    yScale.domain(d3.extent(graphData, d => d.price) as [number, number]);
    return [xScale, yScale];
};
