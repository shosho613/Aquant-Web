import React from 'react';
import './App.css';
import Home from './Home';
import Parser from './Parser';
import Builder from './Builder';
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";






class App extends React.Component{

  render(){
    return (
      <Router>
        <Switch>
          <Route exact path='/' component={Home}/>
          <Route path='/parser/' component={Parser}/>
          <Route path='/builder/' component={Builder}/>
        </Switch>

      </Router>

    );
    }
}

export default App;