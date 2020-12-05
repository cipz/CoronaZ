import React, { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import * as d3 from "d3";
import { gray } from 'd3';

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
        .attr("width", width * scaleFactor)
        .attr("height", height * scaleFactor);
        
        if(node) {
          Object.entries(node).forEach(([key, value]) => {
            if(key != "_id") {
              console.log(value);

              let fill = "gray";
              if(value.alive) {
                fill = (value.infected)? "red": "blue";
              }

              svg.append("circle")
                .attr("cx", value.position[0] * scaleFactor)
                .attr("cy", value.position[1] * scaleFactor)
                .attr("r", radius)
                .attr("fill", fill);
            }
          }) 
        }
    });

    return(
        <div ref={ref} className={classes.root}>
        </div>
    );
};