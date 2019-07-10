export default class PDFTron {
    init = (source, element) => {
      this.viewer = new window.PDFTron.WebViewer({
        path: '/WebViewer/lib',
        initialDoc: source
      }, element,
      );
      //this.viewer.loadDocument(source, { filename: source['name'] })
    }

    

    load = (File, pagenum) => {
          this.viewer.loadDocument(File, {filename: File['name']});
          console.log(this.viewer)
          var instance = this.viewer.getInstance()
          var docViewer = instance.docViewer
          console.log(docViewer)
          
          

        }

    goToPage = (pagenum) => {
        var instance = this.viewer.getInstance()
        
        for(var i = 0; i < pagenum; i++){
            console.log("got here")
            instance.goToNextPage()
        }
    }
      

    
  }