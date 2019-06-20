import React from 'react';
import './PdfViewer.css';
import { PdfViewerComponent, Toolbar, Magnification, Navigation, Inject } from '@syncfusion/ej2-react-pdfviewer';

class PdfViewer extends React.Component{

    render(){
        return(
            <PdfViewerComponent id="container" documentPath="" serviceUrl="https://ej2services.syncfusion.com/production/web-services/api/pdfviewer" style={{ 'height': '640px' }}>
            <Inject services={[Toolbar, Magnification, Navigation]}/>
            </PdfViewerComponent>
        );
    }
}

export default PdfViewer;