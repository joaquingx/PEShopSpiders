import * as d3 from 'd3'
import * as React from 'react'
import { Fragment } from 'react'
import {useEffect, useState} from 'react'
import { Price, ScaleD3 } from './InterfacesTypes'

const config = {
    circle: {
        borderCircleColor: "#000000",
        radius: 5,
    }
};


interface Props {
    items: Price[]
    xScale: ScaleD3,
    yScale: ScaleD3,
    mainColor: string,
}

function getLine(graphData: Price[], xScale: ScaleD3, yScale: ScaleD3) {
    return d3.line<Price>()
        .x(d => xScale(d.date))
        .y(d => yScale(d.price))
}

const drawLine = (graphData: Price[], xScale: ScaleD3, yScale: ScaleD3): string =>{
    let lineGenerator = getLine(graphData, xScale, yScale);
    return lineGenerator(graphData) as string;
};


const CircleInfo: React.FC<{x: number, y: number, price: number, date: Date, mainColor: string, mouseMove: any, mouseLeave: any}> =
    ({x, y, price, date, mainColor, mouseMove, mouseLeave}) => {
    return (
        <circle
            cx={x}
            cy={y}
            r={config.circle.radius}
            fill="white"
            strokeWidth='2.2'
            style={{ fill: mainColor, stroke: config.circle.borderCircleColor}}
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

export const Graph: React.FC<Props> = ({items, xScale, yScale, mainColor}) => {
    const [graphData, setGraphData] = useState([{date: new Date(), price: 10}]);
    const pointInfo = useShowPointInfo(0, new Date(), 0, 0);
    useEffect( () => {
        function getGraphData () {
            setGraphData(items)
        }
        getGraphData();
    });

    const handleMouseMove = (e: MouseEvent, price: number, date: Date) => {
        pointInfo.setShowPoint(true);
        pointInfo.setPointCoords({x: e.clientX, y: e.clientY});
        pointInfo.setPointDate(date);
        pointInfo.setPointPrice(price);
    };

    const handleMouseLeave = () => {
      pointInfo.setShowPoint(false);
    };

    return (
            <Fragment>
                <path d={drawLine(graphData, xScale, yScale)} fill='none' stroke={mainColor} strokeWidth="3"/>
                <g>
                    <g>
                        {
                            graphData.map((d, index) => {
                                return <CircleInfo key={index} x={xScale(d.date)} y={yScale(d.price)}
                                                   price={d.price} date={d.date} mainColor={mainColor}
                                                   mouseLeave={handleMouseLeave} mouseMove={handleMouseMove}/>
                            })
                        }
                    </g>
                </g>
            </Fragment>
)};
