import React from 'react';

import './App.css';

function Item(props) {
  const item = props.item;
  return (
    <img src={item.img} alt={item.name} style={{position: 'absolute', left:item.x, top:item.y}} />
  );
}

export default Item;
