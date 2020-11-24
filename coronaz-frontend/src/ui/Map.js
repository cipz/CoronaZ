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

export default function Map(props) {
    const classes = useStyles();
    
    const ref = React.createRef()

    const height = props.height;
    const width = props.width;
    const radius = props.radius;
    const node = props.node;

    const scaleFactor = 5;

    useEffect(() => {
        // Clear old content, duh...
        d3.select(ref.current)
          .select("svg")
          .remove();

        var svg = d3.select(ref.current)
        .append("svg")
        .attr("width", width)
        .attr("height", height);
        
        if(node) {
          Object.entries(node).forEach(([key, value]) => {
            if(key != "_id") {
              console.log(value)
              svg.append("circle")
                .attr("cx", value[0][0])
                .attr("cy", value[0][1])
                .attr("r", radius)
                .attr("fill", (value[1])? "red": "blue");
            }
          });
        }
    });

    return(
        <div ref={ref} className={classes.root}>
        </div>
    );
};