import React from 'react'
import DiagFlow from './DiagFlow'
import { withRouter } from "react-router-dom";
import TextRep from './TextRep';

/** Build from scratch component */
class Builder extends React.Component{

    render(){
        const BackHome = withRouter(({history}) => (
            <img src="https://pbs.twimg.com/media/Dn88s1aWsAAF4fH.png" width="200" height="150"alt="" onClick={() =>{
              history.push({
              pathname: '/',
              })
              window.location.reload();
                }}>
             </img>
      
          ))
      
          
        return(
            <div className="container-fluid">
                <div className="row">
            <div className="container">
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <BackHome/>
                <h3 className="navbar-brand">Aquant-Fault Tree Parser</h3>
                <h6>Please Label Events. Red = Observation, Blue = Solution.</h6>
                 
                           
                </nav>
                </div>
        </div>
                <DiagFlow hasPdf={false}/>
            <TextRep file={null} pagenum={null}/>
            </div>
        );
    }
}

export default Builder;