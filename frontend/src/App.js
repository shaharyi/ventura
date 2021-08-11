import React, { useState, useEffect } from 'react';

import logo from './logo.svg';
import './App.css';

function App() {
  const [room, setRoom] = useState(null);

  useEffect(() => {
    fetch('/api/v1.0/rooms/1').then(res => res.json()).then(data => {
      setRoom(JSON.stringify(data));
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Room: {room}.</p>
      </header>
    </div>
  );
}

export default App;
