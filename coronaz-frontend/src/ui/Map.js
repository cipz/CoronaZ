import React, { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import * as d3 from "d3";
import test_data from "./test_data.json";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    border: "1px solid black",
  },
  title: {
    flexGrow: 1,
  },
}));

export default function Map() {
    const classes = useStyles();
    
    const ref = React.createRef()

    var height = test_data.height;
    var width = test_data.width;
    var radius = test_data.radius;

    useEffect(() => {
        var svg = d3.select(ref.current)
        .append("svg")
        .attr("width", width)
        .attr("height", height);
        
        test_data.nodes.forEach((node) => {
            svg.append("circle")
            .attr("cx", node.x)
            .attr("cy", node.y)
            .attr("r", radius)
            .attr("fill", (node.inf)? "red": "blue");
        })
    });

    return(
        <div ref={ref} className={classes.root}>
        </div>
    );
};