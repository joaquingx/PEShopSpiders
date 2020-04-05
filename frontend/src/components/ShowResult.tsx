import { Product } from './ProductAggregator';
import {useEffect, useState} from 'react'
import  * as React from 'react'
import './ShowResult.css'
import * as d3 from 'd3'

interface graphData {
    date: Date,
    value: number,
}

async function scatterPlot() {
    let margin = {top: 10, right: 100, bottom: 30, left: 30};
    let width = 460 - margin.left - margin.right;
    let height = 400 - margin.top - margin.bottom;
    let svg = d3.select("#data_viz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
    let csv = await d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/connectedscatter.csv");
    let format_date = (d: any): graphData => {
        return {date: d3.timeParse("%Y-%m-%d")(d.date) as Date, value: d.value}
    };
    let ff = csv.map(format_date);

    let graphic_data = function (data: {date: Date, value: number}[]) {
        console.log(data);
        const domainX = d3.extent(data, (e) => e.date) as [Date, Date];
        const domainY = d3.extent(data, (e) => e.value) as [number, number];
        let x = d3.scaleTime()
            .domain(domainX)
            .range([0, width]);
        let y = d3.scaleLinear()
            .domain(domainY)
            .range([height, 0]);

        svg.append("g")
            .attr("transform", "translate(0,"+ height + ")")
            .call(d3.axisBottom(x));

        svg.append("g")
            .call(d3.axisRight(y));

        const line = d3.line<graphData>().curve(d3.curveBasis).x(d => x(d.date)).y(d => y(d.value));
        svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "#69b3a2")
            .attr("stroke-width", 1.5)
            .attr("d", line)

        let Tooltip = d3.select("#data_viz")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px")

        let mouseover = (d: any) => {
            Tooltip.style("opacity", 1)
        };

        let mousemove = function (d: graphData) {
            Tooltip
                .html("Exact value:" + d.value)
                //@ts-ignore
                .style("left", (d3.mouse(this)[0] + 100) + "px")
                //@ts-ignore
                .style("top", (d3.mouse(this)[1]) + "px")
        };

        let mouseLeave = (d: any) => {
            Tooltip
                .style("opacity", 0.2)
        };

        svg.append("g")
            .selectAll("dot")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", d => x(d.date))
            .attr("cy", d => y(d.value))
            .attr("r", 8)
            .attr("fill", "white")
            .attr("stroke", "#69b3a2")
            .attr("stroke-width", 3)
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseLeave)
    };
    graphic_data(ff)
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
                    date: Date.now(),
                }],
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
                    date: Date.now(),
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
        scatterPlot();
    });
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
                <div className="price-graph" id="data_viz">
                    {/*Probablemetne aca agregare d3 things*/}
                </div>
            </div>
        </div>
    )
};
