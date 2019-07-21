import React from 'react';
class PdfViewer extends React.Component {
  constructor(props) {
    super(props);
    this.file = props.file
    this.viewer = React.createRef();
    this.docViewer = null;
    this.annotManager = null;
    this.instance = null;
    this.initialPage = props.pagenum
    console.log(this.initialPage)
  }

  componentDidMount() {
    window.WebViewer({
      path: '/lib',
      initialDoc: ''
    }, this.viewer.current).then(instance => {
      // at this point, the viewer is 'ready'
      // call methods from instance, docViewer and annotManager as needed
      this.instance = instance;
      this.docViewer = instance.docViewer;
      this.annotManager = instance.annotManager;
      instance.loadDocument(this.file)

      instance.enableFilePicker();
     // instance.disableNotesPanel()

      // you can also access major namespaces from the instance as follows:
      // var Tools = instance.Tools;
      // var Annotations = instance.Annotations;

      // now you can access APIs through `this.instance`
      //this.instance.openElement('notesPanel')

      // or listen to events from the viewer element
      this.viewer.current.addEventListener('pageChanged', (e) => {
        const [ pageNumber ] = e.detail;
        console.log(`Current page is ${pageNumber}`);
      });

      

      

      
      

      // or from the docViewer instance
      this.docViewer.on('annotationsLoaded', () => {
        console.log('annotations loaded');
        var annotList = this.annotManager.getAnnotationsList()
        this.annotManager.deleteAnnotations(this.annotManager.getAnnotationsList())
      for(var a in annotList){
        console.log(annotList[a])
      }
      });

      this.annotManager.on('annotationChanged',  (event, annotations, action) => {
        if (action === 'add') {
          console.log(annotations[0].getContents())
          var data = new FormData()
          data.append('event', annotations[0].getContents())
          fetch('http://localhost:5000/addEventFromPDF', {
              method: 'POST',
              body: data,
              headers:{
                "Access-Control-Allow-Origin" : "*", 
                "Access-Control-Allow-Credentials" : true,
              }
          }).then(response => response.json()).then(
            //response => alert("added [responses]. Click Apply Changes to See.")
          )
        } else if (action === 'modify') {
         
          console.log('this change modified annotations');
        } else if (action === 'delete') {
          var data = new FormData()
          data.append('event', annotations[0].getContents())
          fetch('http://localhost:5000/removeEventFromPDF', {
              method: 'POST',
              body: data,
              headers:{
                "Access-Control-Allow-Origin" : "*", 
                "Access-Control-Allow-Credentials" : true,
              }
          })
          console.log('there were annotations deleted');
        }
      })
      this.docViewer.on('documentLoaded', () =>{
        for(var i = 1; i < this.initialPage; i++){
          console.log("got here")
          this.instance.goToNextPage()
      }
      })

      
    })
  }



  

  render(){
    return (
      <div>
      <div className="webviewer" style={{height: "750px"}} ref={this.viewer}></div>
      </div>

    );
  }
}

export default PdfViewer;