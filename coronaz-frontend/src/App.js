import React, { useEffect, useState } from 'react'
import MenuBar from "./ui/MenuBar";
import Map from "./ui/Map";

import * as config from "./config.json";

const axios = require('axios').default;

function App() {

  const [data, setData] = useState([]);
  const [currentSelection, setCurrentSelection] = useState(0);

  const handleTick = () => {
    // Windows
    // axios.get("http://host.docker.internal:9000/data")
    //Linux
    axios.get("http://localhost:9000/data")
      .then(response => {
        console.log(response);
        setData(response.data.result);
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
