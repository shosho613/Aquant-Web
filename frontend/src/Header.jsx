import React from 'react'
import './Header.css'



class Header extends React.Component {

    render() {
      return (
        <div className="row">
        
        <div className="container">
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <img src="https://pbs.twimg.com/media/Dn88s1aWsAAF4fH.png" width="200" height="150"alt=""/>
                <h3 className="navbar-brand">Aquant-Fault Tree Parser</h3>
                <button type="submit" className="btn btn-primary">Get Results</button>
                
                </nav>
                </div>
        </div>

      );
    }

  }

  export default Header;