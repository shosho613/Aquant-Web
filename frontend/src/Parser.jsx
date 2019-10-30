import React from 'react';
import DiagFlow from './DiagFlow';
import PdfViewer  from './PdfViewer';
import { withRouter, Link } from "react-router-dom";




/**Parent Component of Parser Page, houses the diagram flowcharting component and the pdf viewer component */
class Parser extends React.Component {
  
  constructor(props){
    super(props);
    //this.filename = props.location.state.filename
    //this.pagenum = props.location.state.pagenum
    //this.file = props.location.state.file
    //this.data = props.location.state.data
    this.myViewer = React.createRef();
    this.state ={
      pagenum: props.location.state.pagenum,
      file: props.location.state.file
    }
    window.console.log(this.state)



  }


  

  
  componentWillMount(){

  }
  componentDidMount(){

  }
  

 


 
  render(){
    /** loads same parser component with the next page in the pdf file as input to parse. */
    
    
    /** sends user back to the home page */
    const BackHome = withRouter(({history}) => (
      <img src="https://pbs.twimg.com/media/Dn88s1aWsAAF4fH.png" width="200" height="150"alt="" onClick={() =>{
        history.push({
        pathname: '/',
        })
        window.location.reload();
          }}>
       </img>

    ))

    const NextPage = withRouter(({history}) => (
      <button className="btn btn-primary" onClick={() =>{
        var newPage = parseInt(this.state.pagenum) + 1;
        console.log(newPage)
        console.log(this.file)
        history.push({
          pathname: '/parser',
          state: {pagenum: newPage, file:this.state.file}
        })
        window.location.reload()
      }}>Parse Next Page</button>
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
          <DiagFlow file={this.state.file} pagenum={this.state.pagenum} hasPdf ={true}/>
          
        </div>
        <div className="col-lg-5">
        <PdfViewer file={this.state.file} pagenum={this.state.pagenum}/>
        </div>
      </div>
      
        
  
    </div>

  );
  }
 
  }

  export default Parser;