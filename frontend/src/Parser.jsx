import React from 'react';
import DiagFlow from './DiagFlow';
import Header from './Header';
import PdfViewer  from './PdfViewer';

class Parser extends React.Component {
  
  constructor(props){
    super(props);
    //this.filename = props.location.state.filename
    this.pagenum = props.location.state.pagenum
    this.file = props.location.state.file
    this.data = props.location.state.data

    window.console.log(this.pagenum)
    window.console.log(this.file)
    window.console.log(this.data)
  }

  
  



 
  render(){
      return (
        // initialize Uploader component
  
    <div className="container-fluid">
      <Header/> 
      <div className="row"> 
        <div className="col-lg-7">
          <DiagFlow/>
        </div>
        <div className="col-lg-5">
        <PdfViewer/>
        </div>
      </div>

        
  
    </div>

  );
  }
 
  }

  export default Parser;