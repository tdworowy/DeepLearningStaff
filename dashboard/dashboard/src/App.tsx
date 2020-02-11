import React from 'react';
import logo from './logo.svg';
import './App.css';
import { NewNetwork } from './NewNetworkForm';
import { NetworksList } from './NetworksList';

const App = () => {
  return (
    <div className="App">
        <NewNetwork />
        <br/>
        <NetworksList />
    </div>
    
  );
}

export default App;
