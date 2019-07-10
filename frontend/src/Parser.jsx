import React from 'react';
import DiagFlow from './DiagFlow';
import PdfViewer  from './PdfViewer';
import PDFJSBackend from './pdfjs';
import WebviewerBackend from './webviewer';
import { withRouter, Route } from "react-router-dom";




class Parser extends React.Component {
  
  constructor(props){
    super(props);
    //this.filename = props.location.state.filename
    //this.pagenum = props.location.state.pagenum
    this.file = props.location.state.file
    this.data = props.location.state.data
    this.myViewer = React.createRef();
    this.state ={
      pagenum: props.location.state.pagenum
    }



    window.console.log(this.pagenum)
    window.console.log(this.file)
    window.console.log(this.data)
  }


  

  

  componentDidMount(){

  }
  

 


 
  render(){
    const NextPage = withRouter(({history}) => (
      <button type="submit" className="btn btn-primary p-3" onClick={()=>{
        var newPage = parseInt(this.state.pagenum) + 1
        this.setState({pagenum : newPage})
        console.log(this.state.pagenum)
        const queryString = require('query-string');
        const parsed = queryString.parse(history.location.search)
        parsed.pagenum = newPage
        var stringified = queryString.stringify(parsed)
        history.push({
        pathname: '/parser/',
        search: stringified,
        state: {pagenum: newPage, file: this.file,}
        })
        window.location.reload();
          }}>
       Parse Next Page 
       </button>

    ))

    const BackHome = withRouter(({history}) => (
      <img src="https://pbs.twimg.com/media/Dn88s1aWsAAF4fH.png" width="200" height="150"alt="" onClick={() =>{
        history.push({
        pathname: '/',
        })
        window.location.reload();
          }}>
       </img>

    ))

    
   
      return (
        // initialize Uploader component
  
    <div className="container-fluid">
      
      <div className="row">
        <div className="container">
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <BackHome/>
                <h3 className="navbar-brand">Aquant-Fault Tree Parser</h3>
                <h6>Please Label Events. Red = Observation, Blue = Solution.</h6>
                <NextPage/> 
                           
                </nav>
                </div>
        </div>
      <div className="row"> 
        <div className="col-lg-7">
          <DiagFlow file={this.file} pagenum={this.state.pagenum} hasPdf ={true}/>
        </div>
        <div className="col-lg-5">
        <PdfViewer file={this.file} pagenum={this.state.pagenum}/>
        </div>
      </div>

        
  
    </div>

  );
  }
 
  }

  export default Parser;