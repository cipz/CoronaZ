import React, { useEffect, useState } from 'react'
import { makeStyles } from '@material-ui/core/styles';

import MenuBar from "./ui/MenuBar";
import Map from "./ui/Map";
import {CircularProgress} from '@material-ui/core';
import * as config from "./config.json";

const axios = require('axios').default;

const useStyles = makeStyles((theme) => ({
  loading: {
    padding: 2
  }
}));

function App() {
  const classes = useStyles();

  const [data, setData] = useState([]);
  const [currentSelection, setCurrentSelection] = useState(0);
  const [realismMode, setRealismMode] = useState(false);

  const handleTick = () => {
    // This has to be localhost as it is run from broser
    axios.get("http://localhost:9000/data")
      .then(response => {
        console.log(response);
        setData(response.data.result);
      })
      .catch(err => {
        console.log(console.error(err));
      })
  };

  useEffect(() => {
    handleTick();
    const interval = setInterval(() => handleTick(), 5000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  const handleChange = (event, newValue) => {
    setCurrentSelection(newValue);
  }

  const onRealismChange = (event) => {
    setRealismMode(event.target.checked);
  }

  var menubar = (data.length !== 0)? (<MenuBar realism={realismMode} onRealismChange={onRealismChange} min={0} max={data.length - 1} handleChange={handleChange} node={data[currentSelection]}/>): 
    (<MenuBar realism={realismMode} onRealismChange={onRealismChange} min={0} max={0} handleChange={(event, newValue) => {}} node={data[currentSelection]}/>);

  var map = (data.length !== 0)? (<Map height={config.field_height} width={config.field_width} radius={config.infection_radius} scale={config.scale_factor} node={data[currentSelection]} realism={realismMode}/>):
    (<CircularProgress className={classes.loading}/>);
  return (
    <div>
      {menubar}
      {map}  
    </div>
  );
}

export default App;
