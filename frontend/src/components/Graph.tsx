import * as d3 from 'd3'
import {ScaleLinear, ScaleTime} from 'd3-scale'
import * as React from 'react'
import {useEffect, useRef, useState} from 'react'
import {graphData} from './ProductAggregator'

const width = 450;
const height = 400;
const margin = {top: 20, right: 20, bottom: 20, left: 35};
const lineColor = "#000000";
const circleColor = "#69b3a2";
type ScaleD3 = ScaleTime<number, number> | ScaleLinear<number, number>

interface Props {
    items: graphData[]
}

let getScales = (graphData: graphData[]): [ScaleD3, ScaleD3] => {
    let xScale = d3.scaleTime().range([margin.left, width - margin.right]);
    let yScale = d3.scaleLinear().range([height-margin.top, margin.bottom]);
    xScale.domain(d3.extent(graphData, d => d.date) as [Date, Date]);
    yScale.domain(d3.extent(graphData, d => d.price) as [number, number]);
    return [xScale, yScale];
};

function getLine(graphData: graphData[], xScale: ScaleD3, yScale: ScaleD3) {
    return d3.line<graphData>()
        .x(d => xScale(d.date))
        .y(d => yScale(d.price))
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

const drawGraphWithD3 = (graphData: graphData[], references: {refXAxis: any, refYAxis: any}): void => {
    let [xScale, yScale] = getScales(graphData);
    let {refXAxis, refYAxis} = references;
    drawAxis(graphData, refXAxis, refYAxis, xScale, yScale);
};

const CircleInfo: React.FC<{x: number, y: number, price: number, date: Date, mouseMove: any, mouseLeave: any}> =
    ({x, y, price, date, mouseMove, mouseLeave}) => {
    return (
        <circle
            cx={x}
            cy={y}
            r="10"
            fill="white"
            strokeWidth='2'
            style={{ fill: circleColor, stroke: "black"}}
            onMouseMove={(e) => mouseMove(e, price, date)}
            onMouseLeave={mouseLeave}
        >
        </circle>
    )
};

const useShowPointInfo = (price: number, date: Date, x: number, y: number) => {
    const [showPoint, setShowPoint] = useState(false);
    const x1 = useState(price);
    const [pointDate, setPointDate] = useState(date);
    const [pointCoords, setPointCoords] = useState({x,y});

    return {
        showPoint,
        pointPrice: x1[0],
        pointDate,
        pointCoords,
        setShowPoint,
        setPointPrice: x1[1],
        setPointDate,
        setPointCoords,
    }
};


export const Graph: React.FC<Props> = ({items}) => {
    const [graphData, setGraphData] = useState([{date: new Date(), price: 10}]);
    const pointInfo = useShowPointInfo(0, new Date(), 0, 0);
    const [xScale, yScale] = getScales(graphData);
    const refXAxis = useRef<SVGGElement>(null);
    const refYAxis = useRef<SVGGElement>(null);
    useEffect( () => {
        function getGraphData () {
            setGraphData(items)
        }
        getGraphData();
        drawGraphWithD3(graphData, {
            refXAxis: refXAxis.current,
            refYAxis: refYAxis.current,
        })
    });

    const handleMouseMove = (e: MouseEvent, price: number, date: Date) => {
        pointInfo.setShowPoint(true);
        pointInfo.setPointCoords({x: e.clientX, y: e.clientY});
        pointInfo.setPointDate(date);
        pointInfo.setPointPrice(price);
    };

    const handleMouseLeave = (e: MouseEvent) => {
      pointInfo.setShowPoint(false);
    };

    return (
        <div className="graph-container">
            <svg width={width} height={height}>
                <path d={drawLine(graphData)} fill='none' stroke={lineColor}/>
                <g>
                    <g ref={refXAxis} transform={`translate(0, ${height-margin.bottom})`}/>
                    <g ref={refYAxis} transform={`translate(${margin.left}, 0)`}/>
                    <g>
                        {
                            graphData.map(d => {
                                return <CircleInfo x={xScale(d.date)} y={yScale(d.price)}
                                                   price={d.price} date={d.date}
                                                   mouseLeave={handleMouseLeave} mouseMove={handleMouseMove}/>
                            })
                        }
                    </g>
                </g>
            </svg>
            <div className="tooltip">
                {
                    pointInfo.showPoint ?
                        <div style={{position: "absolute", left: pointInfo.pointCoords.x - 50,
                            top: pointInfo.pointCoords.y - 50, fontSize: '25px', color: "red"}}>{pointInfo.pointPrice}</div> :
                        <div></div>
                }
            </div>
        </div>

    )
}
