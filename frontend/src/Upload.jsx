import React from 'react';
import { withRouter } from "react-router-dom";



class Upload extends React.Component{

    constructor(props) {
        super(props);
        this.pagenum = null
        this.file = null
        this.handleUpload = this.handleUpload.bind(this)

    }

    handleUpload(){
      this.file = this.uploadInput.files[0];
      this.pagenum = document.getElementById("pagenum").value
      var data = new FormData()
      data.append('file', this.file);
      data.append('pagenum', this.pagenum)
      console.log(data)
      fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: data,
        headers:{
          "Access-Control-Allow-Origin" : "*", 
          "Access-Control-Allow-Credentials" : true,
        }
      }).then(response => response.json())
      .then(response => {
        this.setState({data: response});


      }
      )
    }


    
    render() {
        const ParserSubmit = withRouter(({history}) => (
            <button type="submit" className="btn btn-primary p-3" onClick={()=>{
                this.file = this.uploadInput.files[0];
                const queryString = require('query-string');
                const parsed = queryString.parse(history.location.search)
                this.pagenum = document.getElementById("pagenum").value
                parsed.pagenum = this.pagenum
                var stringified = queryString.stringify(parsed)
                history.push({
                pathname: '/parser/',
                search: stringified,
                state: {pagenum: this.pagenum, file: this.file,}
                })}}>
             Submit 
             </button>

          ))
        return (
            <form autoComplete="off">
            <div>
              <input ref={(ref) => { this.uploadInput = ref; }} type="file"/>
            </div>
            <input id="pagenum" className="form-control form-control-lg" type="text" placeholder="Enter starting PDF page."/>
            <button type="button" className="btn btn-success p-3" onClick={()=>{
              this.handleUpload()
            }}>Apply</button>
            <ParserSubmit/>
          </form>
        );
      }
    
}

export default Upload;