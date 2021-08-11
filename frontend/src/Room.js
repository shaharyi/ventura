import React, { useState, useEffect } from 'react';

import Item from './Item.js';

import './App.css';

function Room() {
  const [room, setRoom] = useState({img:"", items:[]});

  useEffect(() => {
    fetch('/api/v1.0/rooms/1').then(res => res.json()).then(data => {
      setRoom(data);
    });
  }, []);

  const items = room.items.map((d) => <Item item={d} />);

  return (
    <div className="App">
      <header className="App-header">
        <img src={room.img} alt="logo" />
        <div>
          {items}
        </div>
        <div>Room: {JSON.stringify(room)}</div>
      </header>
    </div>
  );
}

export default Room;
