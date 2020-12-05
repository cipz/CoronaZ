import React, { useEffect, useState } from 'react'
import MenuBar from "./ui/MenuBar";
import Map from "./ui/Map";

import * as config from "./config.json";

const axios = require('axios').default;

function App() {

  const [data, setData] = useState([]);
  const [currentSelection, setCurrentSelection] = useState(0);

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

  const handleChange = (event, newValue) => {
    setCurrentSelection(newValue);
  }

  useEffect(() => {
    handleTick();
    const interval = setInterval(() => handleTick(), 5000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  var menubar = (data.length != 0)? (<MenuBar min={0} max={data.length - 1} handleChange={handleChange}/>): <MenuBar min={0} max={0} handleChange={(event, newValue) => {}}/>

  return (
    <div>
      {menubar}
      <Map height={config.field_height} width={config.field_width} radius={config.infection_radius} scale={config.scale_factor} node={data[currentSelection]}/>
    </div>
  );
}

export default App;
