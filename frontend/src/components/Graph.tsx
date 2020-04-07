import * as d3 from 'd3'
import * as React from 'react'
import {useEffect, useState} from "react";

const width = 650;
const height = 400;
const margin = {top: 20, right: 5, bottom: 20, left: 35};
const red = "#eb6a5b";

interface graphData {
    date: Date,
    value: number,
}

async function scatterPlot () {
    let xScale = d3.scaleTime().range([margin.left, width - margin.right]);
    let yScale = d3.scaleLinear().range([margin.bottom, height - margin.top]);
    let lineGenerator = d3.line();
}

export function Graph (props: {items: Promise<graphData[]>}) {

    const [graphData, setGraphData] = useState([{date: new Date(), value: 10}]);

    useEffect( () => {
        // props.items.then(items => setGraphData(items));
        async function getGraphData () {
            let items= await props.items;
            setGraphData(items)
        }
        getGraphData()
    });

    console.log(graphData);

    return (
        <div className="graph-container">
            <p>Graph Data:</p>
            <p>{graphData[0].date.toString()}{graphData[0].value}</p>
            <svg width={width} height={height}>
            </svg>
        </div>

    )
}
