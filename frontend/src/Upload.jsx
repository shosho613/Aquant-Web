import React from 'react';
import { withRouter } from "react-router-dom";
import bsCustomFileInput from 'bs-custom-file-input';


/** component that deals with uploading and loading fault trees from pdf */
class Upload extends React.Component{

    constructor(props) {
        super(props);
        this.pagenum = null
        this.file = null
        this.handleUpload = this.handleUpload.bind(this)

    }

    componentDidMount() {
      bsCustomFileInput.init()
    }

    /** takes the file uploaded by the user and the page number
     * sends to server to retrieve corresponding fault tree
     * 
     */
    handleUpload(){
      this.file = this.uploadInput.files[0];
      this.pagenum = document.getElementById("pagenum").value
      var data = new FormData()
      data.append('file', this.file);
      data.append('pagenum', this.pagenum)
      console.log(data)
      fetch('/upload', {
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
        const ParserSubmit = withRouter(({history}) => (// the submit button that loads the url to the parser component
            <button type="submit" className="btn btn-primary p-3" onClick={()=>{
                this.file = this.uploadInput.files[0];
                this.pagenum = document.getElementById("pagenum").value
                history.push({
                pathname: '/parser/',
                state: {pagenum: this.pagenum, file: this.file,}
                })}}>
             Submit 
             </button>

          ))
        return (
            <form autoComplete="off">
           
            <div class="custom-file">
              <input ref={(ref) => { this.uploadInput = ref; }} type="file" class="custom-file-input file-name" id="customFile"/>
              <label class="custom-file-label" for="customFile">Choose file</label>
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