import * as d3 from 'd3'
import {ScaleLinear, ScaleTime} from 'd3-scale'
import * as React from 'react'
import {useEffect, useRef, useState} from 'react'

interface Props {
    items: Promise<graphData[]>
}

interface graphData {
    date: Date,
    value: number,
}

const width = 450;
const height = 400;
const margin = {top: 20, right: 20, bottom: 20, left: 35};
const lineColor = "#000000";
const circleColor = "#69b3a2";
type ScaleD3 = ScaleTime<number, number> | ScaleLinear<number, number>

 let getScales = (graphData: graphData[]): [ScaleD3, ScaleD3] => {
    let xScale = d3.scaleTime().range([margin.left, width - margin.right]);
    let yScale = d3.scaleLinear().range([height-margin.top, margin.bottom]);
    xScale.domain(d3.extent(graphData, d => d.date) as [Date, Date]);
    yScale.domain(d3.extent(graphData, d => d.value) as [number, number]);
    return [xScale, yScale];
};

function getLine(graphData: graphData[], xScale: ScaleD3, yScale: ScaleD3) {
    return d3.line<graphData>()
        .x(d => xScale(d.date))
        .y(d => yScale(d.value))
}

const drawLine = (graphData: graphData[]): string =>{
    let [xScale, yScale] = getScales(graphData);
    let lineGenerator = getLine(graphData, xScale, yScale);
    return lineGenerator(graphData) as string;
};

const drawAxis = (graphData: graphData[], refXAxis: any, refYAxis: any, xScale: ScaleD3, yScale: ScaleD3): void => {
    let xAxis = d3.axisBottom(xScale);
    let yAxis = d3.axisLeft(yScale);
    d3.select(refXAxis).call(xAxis);
    d3.select(refYAxis).call(yAxis);
};

const drawCircles = (graphData: graphData[], refCircles: any, xScale: ScaleD3, yScale: ScaleD3): void  => {
    d3.select(refCircles)
        .selectAll("dot")
        .data(graphData)
        .enter()
        .append("circle")
        .attr("cx", d => xScale(d.date))
        .attr("cy", d => yScale(d.value))
        .attr("r", 2)
        .attr("fill", "white")
        .attr("stroke", circleColor)
        .attr("stroke-width", 8);
};

const drawToolTip = (graphData: graphData[], refToolTip: any, refCircles: any): void =>  {
    const [xScale, yScale] = getScales(graphData);
    const toolTip = d3.select(refToolTip)
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px");
    const mousemove = (d: graphData) => {
        toolTip.html("Exact value: " + d.value)
            //@ts-ignore
            .style("left", (d3.mouse(this)[0] + 100) + "px")
    };
    const mouseover = () => {
        toolTip.style("opacity", 1);
    };
    const mouseLeave = () => {
        toolTip.style("opacity", 0.2);
    };
    d3.select(refCircles)
        .selectAll("dot")
        .data(graphData)
        .enter()
        .append("circle")
        .attr("cx", d => xScale(d.date))
        .attr("cy", d => yScale(d.value))
        .attr("r", 2)
        .attr("fill", "white")
        .attr("stroke", circleColor)
        .attr("stroke-width", 8)
        .on('mouseover', mouseover)
        .on('mousemove', mousemove)
        .on('mouseleave', mouseLeave)
};

const drawGraphWithD3 = (graphData: graphData[], references: {refCircles: any, refXAxis: any, refYAxis: any, refToolTip: any}): void => {
    let [xScale, yScale] = getScales(graphData);
    let {refCircles, refXAxis, refYAxis, refToolTip} = references;
    drawCircles(graphData, refCircles, xScale, yScale);
    drawAxis(graphData, refXAxis, refYAxis, xScale, yScale);
    drawToolTip(graphData, refToolTip, refCircles);
};

export const Graph: React.FC<Props> = ({items}) => {
    const [graphData, setGraphData] = useState([{date: new Date(), value: 10}]);
    const refXAxis = useRef<SVGGElement>(null);
    const refYAxis = useRef<SVGGElement>(null);
    const refCircles = useRef<SVGGElement>(null);
    const refToolTip = useRef<HTMLDivElement>(null);
    useEffect( () => {
        async function getGraphData () {
            let itemsDownloaded = await items;
            setGraphData(itemsDownloaded)
        }
        getGraphData();
        drawGraphWithD3(graphData, {
            refCircles: refCircles.current,
            refXAxis: refXAxis.current,
            refYAxis: refYAxis.current,
            refToolTip: refToolTip.current,
        })
    });

    return (
        <div className="graph-container">
            <svg width={width} height={height}>
                <path d={drawLine(graphData)} fill='none' stroke={lineColor}/>
                <g>
                    <div ref={refToolTip}/>
                    <g ref={refXAxis} transform={`translate(0, ${height-margin.bottom})`}/>
                    <g ref={refYAxis} transform={`translate(${margin.left}, 0)`}/>
                    <g ref={refCircles}/>
                </g>
            </svg>
        </div>

    )
}
