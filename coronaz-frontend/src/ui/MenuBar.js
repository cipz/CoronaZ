import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { AppBar, Toolbar, Typography, Slider, FormControlLabel, Switch, Grid } from '@material-ui/core';

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

export default function MenuBar(props) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Grid container spacing={1}>
          <Grid item xs={4}>
            <Toolbar>
              <Typography variant="h6" className={classes.title}>
                CoronaZ: Timeline from Day Zero
              </Typography>
            </Toolbar>
          </Grid>
          <Grid item xs={2}>
            <Toolbar>
              <FormControlLabel
                control={
                  <Switch
                    checked={props.realism}
                    onChange={props.onRealismChange}
                    name="checkedIcons"
                    color="secondary"
                  />
                }
                label="Realism"
              />
            </Toolbar>
          </Grid>
          <Grid item xs={12}>
            <Slider
              className={classes.slider}
              defaultValue={0}
              getAriaValueText={valuetext}
              aria-labelledby="discrete-slider"
              valueLabelDisplay="auto"
              step={1}
              marks
              min={props.min}
              max={props.max}
              onChange={props.handleChange}
            />
          </Grid>
        </Grid>
      </AppBar>
    </div>
  );
}
