import * as React from "react";
import './DiagFlow.css'
import { ToolbarComponent } from '@syncfusion/ej2-react-navigations';
import { HierarchicalTree, DataBinding, DiagramComponent, Inject, SymbolPaletteComponent, Connector, SnapConstraints } from "@syncfusion/ej2-react-diagrams";
import SolutionTool from './SolutionTool';
import ObservationTool from './ObservationTool';

/** class compenent dealing with interactive diagram flowchart */
export class DiagFlow extends React.Component {

    constructor(props){
        super(props);
        this.pagenum = props.pagenum
        this.file = props.file
        console.log(this.file)
        this.hasPdf = props.hasPdf // if diagflow is used as a representation for pdf parsing, its True
        /**state handles the existing nodes and connectors */
        this.state ={
             nodes : [
                {
                    id: "n1",
                    offsetX: 280,
                    offsetY: 250,
                    annotations: [{ content: "" }],
                    addInfo : [{'eventtype' : ''}]
                },
                {
                    id: "n2",
                    offsetX: 280,
                    offsetY: 110,
                    annotations: [{ content: "" }],
                    addInfo : [{'eventtype' : ''}]

                },
               
                
            ],
            //Initializes the connector for the diagram
             connectors : [
                {
                    id: "connector1",
                    sourceID: "n1",
                    targetID: "n2",
                },
            ]
                
        }
        this.addedEvents = null
        this.nodes = null
        this.connectors = []
        this.new_annots = false
        this.downloadCSV = this.downloadCSV.bind(this);
        this.saveAsFile = this.saveAsFile.bind(this);
        this.getGraphRep = this.getGraphRep.bind(this);
        this.convertNodes = this.convertNodes.bind(this);
		this.convertConnectors = this.convertConnectors.bind(this);
        this.getPorts = this.getPorts.bind(this);
        
    }

    componentDidMount(){
        if(this.file !== undefined){
            this.getGraphRep()
        }
	}
    
    /** returns the ports to enable connecting and disconecting connectors */
	getPorts(node){
		let ports = [
			{ id: "port1", shape: "Circle", offset: { x: 0, y: 0.5 } },
			{ id: "port2", shape: "Circle", offset: { x: 0.5, y: 1 } },
			{ id: "port3", shape: "Circle", offset: { x: 1, y: 0.5 } },
			{ id: "port4", shape: "Circle", offset: { x: 0.5, y: 0 } }
		];
		return ports;

	}

    /** @return an array that is compliant with diagram API, from what JSON format returns as. */
    convertNodes(array){
        var result = []
        for (var i in array){
            result.push({
                id : String(array[i]['Name']),
                annotations : [{content : String(array[i]['Content'])}],
                addInfo : [{eventtype : String(array[i]['eventtype'])}]
            })
        }
        return result
    }


    /** @return an array that is compliant with diagram API, from what JSON format returns as. */

    convertConnectors(array){
        var result = []
        for (var c in array){
			if(array[c] !== null){
				result.push({
					id : String(array[c]['id']),
					sourceID : String(array[c]['sourceID']),
					targetID : String(array[c]['targetID']),
					annotations : [{content : String(array[c]['content'])}]
				})
			}
        }
        return result
    }

    /** retrieves and sets state of PDF tree representation  */
    getGraphRep(){
        var data = new FormData()
        data.append('pagenum', this.pagenum)
        data.append('file', this.file)
        fetch('/GetGraph', {
        method: 'POST',
        body: data,
        headers:{
          "Access-Control-Allow-Origin" : "*", 
          "Access-Control-Allow-Credentials" : true,
        }
      }).then(response => response.json())
      .then(response => {
        console.log(this.state.data)
        console.log(response['nodes'][0]['Name'])
        console.log(response['connectors'])
        //exports.nodes = response['nodes']
        //exports.connectors = response['connectors']
        var nodeArr = this.convertNodes(response['nodes'])
        var connectorArr = this.convertConnectors(response['connectors'])
        console.log(nodeArr)
        this.setState({nodes : nodeArr, connectors: connectorArr})
  
      }
      )
    }

    /** gets all annotations from server, adds them to addedEvents array and sets has_annotations to True */
    getAnnotationsAsEvents = () =>{
        var data = new FormData()
        console.log(this.state.nodes.length)
        data.append("size", String(this.state.nodes.length))
        fetch('/GetAnnots', {
        method: 'POST',
        body: data,
        headers:{
          "Access-Control-Allow-Origin" : "*", 
          "Access-Control-Allow-Credentials" : true,
        }
      }).then(response => response.json())
      .then(response => {
          /*this.addedEvents = response
          console.log(this.addedEvents)
          this.new_annots = true*/
          var addedNodes = this.convertNodes(response)
          this.addedEvents = addedNodes
          this.new_annots = true
      })

    }

    /**fetches csv created in server, downloads to client */
    downloadCSV(){
        var data = new FormData()
        data.append('nodes', JSON.stringify(this.state.nodes))
        data.append('connectors', JSON.stringify(this.state.connectors))
        fetch('/downloadcsv', {
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
        let diagramInstance;
        
        let handles = [{ //sets user buttons on each diagram element
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
                right: 100
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
                top: 10,
                bottom: 10,
                left: 100,
                right: 10
            },
            backgroundColor: 'red'
        }
        ]

        //sets template icons for draggable pallettes
        let flowshapes = [
            {id : 'Process', shape: { type: "Flow", shape: "Process"}}
        ]

        let connectorSymbols = [
            {
                id: "Link1",
                type: "Orthogonal",
                sourcePoint: { x: 0, y: 0 },
                targetPoint: { x: 60, y: 60 },
                targetDecorator: { shape: "Arrow" },
                style: { strokeWidth: 1 }
            },
        ]

        //only show the add PDF Annotations if used in the parse from PDF option
        const AddPDFButton = () => {
            if(this.hasPdf){
                return(
                    <button className="btn btn-secondary" onClick={() => {this.getAnnotationsAsEvents()}}>Add PDF Annotations</button>
                );
            }
            else{
                return(
                    <div></div>
                );
            }
        }

        return (
			<div className="control-pane font-size:larger">
				<div className="control-section">
                <AddPDFButton/>
				<button className="btn btn-success" onClick={ ()=>{ //Applying changes done on clientside to diagram API
						var nodeArr = []
						var connectorArr = []
						for(var i in diagramInstance.nodes){
							nodeArr.push({
								id : String(diagramInstance.nodes[i].id),
								annotations : [{content : String(diagramInstance.nodes[i].annotations[0].content)}],
								addInfo : [{eventtype : String(diagramInstance.nodes[i].addInfo[0].eventtype)}]    
							})

                        }

                        //now add the pdf highlights as nodes, if present.
                        if(this.new_annots){
                            for(var a in this.addedEvents){
                                nodeArr.push(this.addedEvents[a])
                            }
                        }
                            
                        console.log(nodeArr)
						for(var c in diagramInstance.connectors){
							connectorArr.push({
								id : String(diagramInstance.connectors[c].id),
								sourceID : String(diagramInstance.connectors[c].sourceID),
								targetID : String(diagramInstance.connectors[c].targetID),
								annotations : [{content : String(diagramInstance.connectors[c].annotations[0].content)}] 
							})

                        }
						this.setState({nodes : nodeArr, connectors : connectorArr})
						console.log(this.state.nodes)
                        console.log(this.state.connectors)
                        this.new_annots = false
                    
					}}>Apply Edits (Refresh Diagram)</button>
					<button type="submit" className="btn btn-primary" onClick={this.downloadCSV}>Get Results</button> 

                    <ToolbarComponent id='toolbar'  items={[ // handles the deletion of client side elements. 
                                                                                                    //Only gets updated server-side when apply edits button is triggered
                    {
                        tooltipText: 'Delete',
                        prefixIcon: 'e-ddb-crudicons e-delete',
                        id: 'Delete',
                        text: 'Delete'
                    }
        ]} clicked={(args) => {
            let selectedItem;
            if (diagramInstance.selectedItems.nodes.length > 0) {
                selectedItem = diagramInstance.selectedItems.nodes[0];
            }
            if (diagramInstance.selectedItems.connectors.length > 0) {
                selectedItem = diagramInstance.selectedItems.connectors[0];
            }
            if (selectedItem) {
                switch (args.item.tooltipText) {
                    case 'Delete':
                        diagramInstance.remove(selectedItem);
                        diagramInstance.doLayout();
                        let element = { id: selectedItem.id, annotations: selectedItem.annotations, addInfo: selectedItem.addInfo };
                        let index = this.state.nodes.indexOf(element);
                        console.log(index)
                        this.state.nodes.splice(index, 1);
                        break;
                    default:
                        break;
                }
            }
        }} />
					<div className="sb-mobile-palette-bar">
						<div id="palette-icon" style={{ float: "right", role: "button" }} className="e-ddb-icons1 e-toggle-palette"></div>
					</div>
					<div id="palette-space" className="sb-mobile-palette">
						<SymbolPaletteComponent id="symbolpalette" expandMode="Multiple" palettes={[
								{
									id: "flow",
									expanded: true,
									symbols: flowshapes,
									iconCss: "e-diagram-icons1 e-diagram-flow",
									title: "Add Events"
								},
								{
									id: "connectors",
									expanded: true,
									symbols: connectorSymbols,
									iconCss: "e-diagram-icons1 e-diagram-connector",
									title: "Add Connectors"
								}
							]} width={"20%%"} height={"700px"} symbolHeight={60} symbolWidth={60} getNodeDefaults={(symbol) => {
								if (symbol.id === "Process") {
									symbol.width = 80;
									symbol.height = 40;
								}
							}} symbolMargin={{ left: 0, right: 0, top: 0, bottom: 0 }} getSymbolInfo={(symbol) => {
								return { fit: true };
							}}/>
                           

					</div>
					<div id="diagram-space" className="sb-mobile-diagram">
					<DiagramComponent id="diagram" ref={diagram => (diagramInstance = diagram)}  nodes={this.state.nodes} connectors ={this.state.connectors} width={"100%"} height={750} 
							selectedItems ={{
                                
								userHandles: handles
							}}
                            snapSettings={{constraints: SnapConstraints.HideLines}}
                            
							getCustomTool={(action) => {
                                let tool;
                               // handles[1]["visible"] = false

								
								if(diagramInstance.selectedItems.connectors.length === 0 && diagramInstance.selectedItems.nodes.length !== 0){
									if (action === 'solution') {
										tool = new SolutionTool().mouseDown(diagramInstance.commandHandler, diagramInstance)
									}
									else if(action === 'observation'){
										tool = new ObservationTool().mouseDown(diagramInstance.commandHandler, diagramInstance)
								
									}
									return tool;
								} else{
                                    handles[1]["visible"] = false
                                }

							}}
							
							layout={{
								type: "HierarchicalTree",
								horizontalSpacing: 40,
								verticalSpacing: 40,
                                orientation: "TopToBottom",
                                enableAnimation: true,
								margin: { left: 10, right: 0, top: 50, bottom: 0 }
							} //Configrues hierarchical tree layout
							} getNodeDefaults={(obj) => {
								//Sets the default values of nodes
								if (obj.addInfo === undefined){
									var arr = [{eventtype : 'N'}]
									obj.addInfo = arr
								}
								if(obj.annotations === undefined){
									obj.annotations= [{content : ""}]
								}
								let contentArr = [{content: ''}]
								if(obj.annotations.length === 0){
										obj.annotations = contentArr
								}
								
								obj.width =120;
								obj.height = 100;
								//Initialize shape
								obj.shape = {
									type: "Basic",
									shape: "Rectangle",
									cornerRadius: 7
								};
								obj.style.fill = obj.addInfo === undefined ?'#ffeec7' :  obj.addInfo[0].eventtype === 'S' ? "#3583ba" : obj.addInfo[0].eventtype === 'O' ? "#F45342" : '#ffeec7';
                                obj.ports = this.getPorts(obj);
								return obj;
							}} getConnectorDefaults={(connector) => {
								//Sets the default values of connector
								if(connector.id.indexOf("connector") !== -1){
									connector.type = "Orthogonal";
									connector.cornerRadius = 7;
									connector.targetDecorator.height = 10;
									connector.targetDecorator.width = 10;
									connector.style.strokeColor = "#6d6d6d";
									let contentArr = [{content: ''}]
									if(connector.annotations.length === 0 || connector.annotations === undefined){
										connector.annotations = contentArr
									}
								}
								else{
									console.log(connector)
									connector = null
								}
							

							}} dataSourceSettings={{ 	
								id : "id"
							}}
							dragEnter={(args) => {
								let obj = args.element;
								if (obj instanceof Node) {
									console.log(obj)
									let oWidth = obj.width;
									let oHeight = obj.height;
									let ratio = 100 / obj.width;
									obj.width = 100;
									obj.height *= ratio;
									obj.offsetX += (obj.width - oWidth) / 2;
									obj.offsetY += (obj.height - oHeight) / 2;
									obj.style = { fill: "#357BD2", strokeColor: "white" };			
                                }
                                if (obj instanceof Connector){
                                    obj.annotations = [{content : ""}]
                                }
                            }}
                           
							

							>
								<Inject services={[DataBinding, HierarchicalTree ]}/>
								</DiagramComponent>


					</div>
				</div>
                
			</div>
        
      );
    }
}
export default DiagFlow;

