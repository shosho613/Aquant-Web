import React,{Component} from 'react';
import Parser from './Parser';
import Builder from './Builder';
import { BrowserRouter as  Route,Link,  } from "react-router-dom";
import Upload from './Upload';


class Home extends Component{
    constructor(props){
        super(props);
        this.filename = null
        this.pagenum = null
        this.fileToBeSent = null

    }
    
    

    routeChangeToParser() {
        return(
        <Route path="/parser" component={Parser} />
        );

      }
    

    render(){
        //document.body.appendChild(<Upload/>);

        return(
            
            <div className="jumbotron">
                <div className="row">
                <div className="col-m-7">
                    <h1 className="display-4">Aquant Fault Tree Evaluator</h1>
                    <p className="lead">To run: Upload Troubleshooting Manual or Start from scratch!</p>
                </div>
                <img src="https://pbs.twimg.com/media/Dn88s1aWsAAF4fH.png" width="200" height="150"alt=""/>
                </div>
                <hr className="my-4"></hr>
                <div className = "row">
                    <div className="col-m-6">
                        <Upload/>
                    </div>
                    <div className="col-m-6">
                        <Link to="/builder/">Start from Scratch</Link>
                        <Route path="/builder/"  component={Builder} />
                    </div>
                </div>
            
        </div>
            
        );

    }
 
}

export default Home;