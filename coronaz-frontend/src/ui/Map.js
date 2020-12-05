import React, { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import * as d3 from "d3";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    padding: 2
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

        // Initialize svg container
        var svg = d3.select(ref.current)
        .append("svg")
        .attr("width", width * scaleFactor)
        .attr("height", height * scaleFactor);
        
        // Add border
        svg.append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", width * scaleFactor)
                .attr("height", height * scaleFactor)
                .attr("fill", "none")
                .attr("stroke-width", 2)
                .attr("stroke", "rgb(0,0,0)");
        
        if(node) {
          Object.entries(node).forEach(([key, value]) => {
            if(key != "_id") {
              console.log(value);

              let fill = "gray";
              if(value.alive) {
                fill = (value.infected)? "red": "blue";
              }
              
              if(props.realism) {
                let icon = "icons/grave.svg";
                if(value.alive) {
                  icon = (value.infected)? "icons/zombie.svg": "icons/human.svg";
                }

                svg.append("svg:image")
                .attr('x', value.position[0] * scaleFactor - radius * scaleFactor)
                .attr('y', value.position[1] * scaleFactor - radius * scaleFactor)
                .attr("preserveAspectRatio", "none")
                .attr('width', 2 * radius * scaleFactor)
                .attr('height', 2 * radius * scaleFactor)
                .attr("xlink:href", icon)
              } else {
                svg.append("circle")
                .attr("cx", value.position[0] * scaleFactor)
                .attr("cy", value.position[1] * scaleFactor)
                .attr("r", radius * scaleFactor)
                .attr("fill", fill)
              }
            }
              
          }) 
        }
    });

    return(
        <div ref={ref} className={classes.root}>
        </div>
    );
};