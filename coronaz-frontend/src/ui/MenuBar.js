import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { AppBar, Toolbar, Typography, Slider } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  title: {
    flexGrow: 1,
  },
  slider: {
    color: "red",
    width: "96%",
    top: 0,
    bottom: 0,
    left: "2%",
    right: "2%"
  }
}));

function valuetext(value) {
  return `Day ${value}`;
}

export default function MenuBar() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            CoronaZ: Timeline from Day Zero
          </Typography>
        </Toolbar>
        <Slider
          className={classes.slider}
          defaultValue={0}
          getAriaValueText={valuetext}
          aria-labelledby="discrete-slider"
          valueLabelDisplay="auto"
          step={1}
          marks
          min={0}
          max={10}
        />
      </AppBar>
    </div>
  );
}
