import * as React from 'react'
import { ScaleD3 } from "./InterfacesTypes";
import { Fragment } from 'react'
import * as d3 from 'd3'

interface Props {
    xScale: ScaleD3,
    yScale: ScaleD3,
}

const config = {
    axisColor: "#a00037",
    tickColor: "#d81b60",
    textColor: "#616161",
    colorDashedLine: '#d81b60',
};


export const Axis: React.FC<Props> = ({xScale, yScale}) => {
    const [xStart, xEnd] = xScale.range();
    const [yStart, yEnd] = yScale.range();
    const xTicks = xScale.ticks(3);
    const xFormatter = xScale.tickFormat(xTicks.length, '%B %d');
    const yTicks = yScale.ticks();

    // console.log(xScale.tickFormat(4, '%Y-%M'));
    console.log("ticks " + xTicks);
    console.log("tickeanos" + d3.axisBottom(xScale).tickArguments());
    return (
        <Fragment>
            <line x1={xStart} x2={xEnd} y1={yStart} y2={yStart} stroke={config.axisColor}/>
            <line x1={xStart} x2={xStart} y1={yEnd} y2={yStart} stroke={config.axisColor}/>
            <g>
                {
                    //@ts-ignore
                    xTicks.map((t, i) => {
                        const x = xScale(t);
                        const tFormatted = xFormatter(t);
                        return (
                            <Fragment key={i}>
                                <line x1={x} x2={x} y1={yStart} y2={yStart + 5} stroke={config.tickColor}/>
                                <text
                                    x={x}
                                    y={yStart + 20}
                                    fill={config.textColor}
                                    textAnchor="middle"
                                    fontSize={15}
                                    >
                                    {tFormatted}
                                </text>
                            </Fragment>
                        )
                    })
                }
            </g>
            <g>
                {
                    //@ts-ignore
                    yTicks.map((t, i) => {
                        const y = yScale(t);
                        return (
                            <Fragment key={i}>
                                <line x1={xStart} x2={xStart-10} y1={y} y2={y} stroke={config.tickColor}/>
                                <line x1={xStart} x2={xEnd} y1={y} y2={y} stroke={config.colorDashedLine} strokeOpacity={0.5} strokeDasharray="10"/>
                                <text
                                    x={xStart - 20}
                                    y={y}
                                    fill={config.textColor}
                                    fontFamily={`Inconsolata`}
                                    textAnchor="middle"
                                    fontSize={13.5}
                                >
                                    {t}
                                </text>
                            </Fragment>
                        )
                    })
                }
            </g>
        </Fragment>
    )
};
