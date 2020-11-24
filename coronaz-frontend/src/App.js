import React, { useEffect, useState } from 'react'
import MenuBar from "./ui/MenuBar";
import Map from "./ui/Map";

const axios = require('axios').default;

function App() {

  const [data, setData] = useState([]);

  const handleTick = () => {
    axios.get("http://host.docker.internal:10000/data")
      .then(response => {
        console.log(response);
        setData(response.data.result);
      })
  };

  useEffect(() => {
    handleTick();
    const interval = setInterval(() => handleTick(), 5000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div>
      <MenuBar min={0} max={data.length} />
      <Map height="500" width="500" radius="10" node={data[0]}/>
    </div>
  );
}

export default App;
