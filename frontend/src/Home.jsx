import React,{Component} from 'react';
import Parser from './Parser';
import Builder from './Builder';
import { BrowserRouter as  Route,Link, withRouter } from "react-router-dom";
//import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import { FilePond } from 'react-filepond';
import 'filepond/dist/filepond.min.css';

class Home extends Component{
    constructor(props){
        super(props);
        this.filename = null
        this.pagenum = null

    }
    
    

    routeChangeToParser() {
        return(
        <Route path="/parser" component={Parser} />
        );

      }
    onUploadSuccess(args){
        if (args.operation === 'upload') {
            this.filename = args['file']['name']
            window.console.log(args)
        }
      }
    
    uploadFile(){
        this.state.uploadObj.upload(this.uploadObj.getFilesData());
      }


    render(){

        const ParserSubmit = withRouter(({history}) => (
            <button type="submit" className="btn btn-primary mb-10" 
            onClick={()=>{
                const queryString = require('query-string');
                const parsed = queryString.parse(history.location.search)
                this.pagenum = document.getElementById("pagenum").value
                parsed.filename = this.filename
                parsed.pagenum = this.pagenum
                var stringified = queryString.stringify(parsed)
                window.console.log(stringified)
                history.push({
                    pathname: '/parser/',
                    search: stringified,
                    state: {filename: this.filename, pagenum: this.pagenum}})            
            }}>
            
            Submit</button>

          ))
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
                        <FilePond server="/"/>
                        <input id="pagenum" className="form-control form-control-lg" type="text" placeholder="Enter starting PDF page."/>
                        <ParserSubmit/>
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