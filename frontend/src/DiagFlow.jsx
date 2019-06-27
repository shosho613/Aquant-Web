import * as React from "react";
import { ComplexHierarchicalTree, DataBinding, DiagramComponent, Inject, SelectorConstraints, } from "@syncfusion/ej2-react-diagrams";
import { DataManager } from "@syncfusion/ej2-data";
import { multiParentData } from './diagram-data';
import SolutionTool from './SolutionTool';
import ObservationTool from './ObservationTool';
export class DiagFlow extends React.Component {

    constructor(props){
        super(props);
        this.state ={
            data: multiParentData,
        }
        this.downloadCSV = this.downloadCSV.bind(this);
        this.saveAsFile = this.saveAsFile.bind(this);
    
    }

    componentDidMount(){
        fetch('http://localhost:5000/GetNodes', {
        method: 'GET',
        headers:{
          "Access-Control-Allow-Origin" : "*", 
          "Access-Control-Allow-Credentials" : true,
        }
      }).then(response => response.json())
      .then(response => {
        console.log(this.state.data)
        let exports = Object();
        Object.defineProperty(exports, "__esModule", { value: true });
        console.log(response)
        exports.data = response['nodes']
        console.log(exports.data)
        this.setState({data : exports.data})
  
      }
      )
    }

    downloadCSV(){
        var data = new FormData()
        data.append('data', JSON.stringify(this.state.data))
        fetch('http://localhost:5000/downloadcsv', {
            method: 'POST',
            body: data,
            headers:{
              "Access-Control-Allow-Origin" : "*", 
              "Access-Control-Allow-Credentials" : true,
            }
        }).then((response) => {
            var a = response.body.getReader();
            a.read().then(({ done, value }) => {
                // console.log(new TextDecoder("utf-8").decode(value));
                this.saveAsFile(new TextDecoder("utf-8").decode(value), 'result.csv');
              }
            );
        });
    }
        
        
        saveAsFile(text, filename) {
          // Step 1: Create the blob object with the text you received
          const type = 'text/csv'; // modify or get it from response
          const blob = new Blob([text], {type});
        
          // Step 2: Create Blob Object URL for that blob
          const url = URL.createObjectURL(blob);
        
          // Step 3: Trigger downloading the object using that URL
          const a = document.createElement('a');
          a.href = url;
          a.download = filename;
          a.click(); // triggering it manually
        }

    render() {
        let handles = [{
            name: 'solution',
            pathData: 'M60.3,18H27.5c-3,0-5.5,2.4-5.5,5.5v38.2h5.5V23.5h32.7V18z M68.5,28.9h-30c-3, 0-5.5,2.4-5.5,5.5v38.2c0,3,2.4,5.5,5.5,5.5h30c3,0,5.5-2.4,5.5-5.5V34.4C73.9,31.4,71.5,28.9,68.5,28.9z M68.5,72.5h-30V34.4h30V72.5z',
            visible: true,
            offset: 1,
            side: 'Right',
            pathColor: "white",
            margin: {
                top: 0,
                bottom: 0,
                left: 0,
                right: 0
            },
            backgroundColor: 'blue'
        },
        {
            name: 'observation',
            pathData: 'M60.3,18H27.5c-3,0-5.5,2.4-5.5,5.5v38.2h5.5V23.5h32.7V18z M68.5,28.9h-30c-3, 0-5.5,2.4-5.5,5.5v38.2c0,3,2.4,5.5,5.5,5.5h30c3,0,5.5-2.4,5.5-5.5V34.4C73.9,31.4,71.5,28.9,68.5,28.9z M68.5,72.5h-30V34.4h30V72.5z',
            visible: true,
            offset: 1,
            side: 'Left',
            pathColor: "white",
            margin: {
                top: 0,
                bottom: 0,
                left: 0,
                right: 0
            },
            backgroundColor: 'red'
        }
        ]
    
        let diagramInstance;
        return (<div className="control-pane">
        <div className="control-section">
            <button className="btn btn-success" onClick={()=>{
                var nodeData = {nodes: []}
                for(var key in diagramInstance.nodes){
                    var array = nodeData.nodes 
                    array.push(diagramInstance.nodes[key]["data"])
                    nodeData.nodes = array
                }
                console.log(nodeData)
                let exports = Object();
                Object.defineProperty(exports, "__esModule", { value: true });
                exports.data = nodeData['nodes']
                this.setState({data: exports.data})
                console.log(this.state.data)                
            }}>Apply Changes</button>
            <button type="submit" className="btn btn-primary" onClick={this.downloadCSV}>Get Results</button>

          <div className="content-wrapper" style={{ width: "100%" }}>
          <DiagramComponent id="diagram" ref={diagram => (diagramInstance = diagram)} width={"100%"} height={580} selectedItems ={{constraints: SelectorConstraints.UserHandle,
        userHandles: handles}}
        getCustomTool={(action) => {
            let tool;
            if (action === 'solution') {
                tool = new SolutionTool().mouseDown(diagramInstance.commandHandler, diagramInstance)
            }
            else if(action === 'observation'){
                tool = new ObservationTool().mouseDown(diagramInstance.commandHandler, diagramInstance)
        
            }
            return tool;
        }}
        
        layout={{
            type: "ComplexHierarchicalTree",
            horizontalSpacing: 40,
            verticalSpacing: 40,
            orientation: "TopToBottom",
            margin: { left: 10, right: 0, top: 50, bottom: 0 }
        } //Configrues hierarchical tree layout
        } getNodeDefaults={(obj) => {
            //Sets the default values of nodes
            obj.width =60;
            obj.height = 60;
            //Initialize shape
            obj.shape = {
                type: "Basic",
                shape: "Rectangle",
                cornerRadius: 7
            };
   
        }} getConnectorDefaults={(connector) => {
            //Sets the default values of connector
            connector.type = "Orthogonal";
            connector.cornerRadius = 7;
            connector.targetDecorator.height = 7;
            connector.targetDecorator.width = 7;
            connector.style.strokeColor = "#6d6d6d";
        }} dataSourceSettings={{
            id: "Name",
            parentId: "ReportingPerson",
           
            dataManager: new DataManager(this.state.data),
            
        
            
            doBinding: (nodeModel, data, diagram) => {
                //Configures data source
                //binds the external data with node
                /* tslint:disable:no-string-literal */
                console.log(data)
                nodeModel.annotations = [{
                    content: String(data['content']),
                    style: { color: "black" }
                }];
                
                nodeModel.style = {
                    
                    fill: data['eventtype'] === 'Solution' ? "#3583ba" : data['eventtype'] === 'Observation' ? "#F45342" : '#ffeec7',
                    strokeColor: "#f5d897",
                    strokeWidth: 1
                    
                };
            },
          
             
        }} snapSettings={{ constraints: 0 }}>
              <Inject services={[DataBinding, ComplexHierarchicalTree]}/>
            </DiagramComponent>
          </div>
        </div>
      </div>);
    }
}
export default DiagFlow