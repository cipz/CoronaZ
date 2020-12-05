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

  let total_nodes = 0;
  let zombies = 0;
  let deaths = 0;
  let inf_deaths = 0;

  if(props.node) {
    total_nodes = Object.entries(props.node).length - 1;
    zombies = Object.entries(props.node).filter(([key, value]) => key !== "_id" && value.alive && value.infected).length;
    deaths = Object.entries(props.node).filter(([key, value]) => key !== "_id" && !value.alive).length;
    inf_deaths = Object.entries(props.node).filter(([key, value]) => key !== "_id" && !value.alive && value.infected).length;
  }

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
          <Grid item xs={6}>
            <Toolbar>
              <Typography variant="p" className={classes.title}>
              Total nodes: {total_nodes}
              </Typography>
              <Typography variant="p" className={classes.title}>
                Zombies: {zombies}
              </Typography>
              <Typography variant="p" className={classes.title}>
                Deaths: {deaths}
              </Typography>
              <Typography variant="p" className={classes.title}>
                Dead zombies: {inf_deaths}
              </Typography>
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
