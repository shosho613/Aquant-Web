import React from 'react';
import { DiagramComponent, Inject, ComplexHierarchicalTree, DataBinding, SelectorConstraints } from "@syncfusion/ej2-react-diagrams";
import SolutionTool from './SolutionTool';
import ObservationTool from './ObservationTool';

class DiagFlow extends React.Component{

render(){
    let diagramInstance;
    let node = [{
        id: 'node1',
        width: 70,
        height: 70,
        annotations: [{
                content: "Display is black or white, and no icons are shown"
            }]
    }, {
        id: 'node2',
        width: 70,
        height: 70,
        annotations: [{
                content: 'Beep is audible when pressed.'
            }]
    }, {
        id: 'node3',
        width: 70,
        height: 70,
        annotations: [{
                content: 'Change interface PCB'
            }]
    }, {
        id: 'node4',
        width: 70,
        height: 70,
        annotations: [{
                content: 'Change 30 pol cable'
            }]
    }, {
        id: 'node5',
        width: 70,
        height: 70,
        annotations: [{
                content: 'Display Ok?'
            }]
    }, {
        id: 'node6',
        width: 70,
        height: 70,
        annotations: [{
                content: 'Change Display TFT'
            }]
    }
];
let connector = [{
        id: 'connectr',
        sourceID: 'node1',
        targetID: 'node2',
        annotations: [{
            content: "Yes"
        }]
    }, {
        id: 'connectr1',
        sourceID: 'node2',
        targetID: 'node3',
        annotations: [{
            content: "No"
        }]
    }, {
        id: 'connectr3',
        sourceID: 'node2',
        targetID: 'node4',
        annotations: [{
            content: "Yes"
        }]
    }, {
        id: 'connectr4',
        sourceID: 'node4',
        targetID: 'node5',
        annotations: [{
            content: "Yes"
        }]
    }, {
        id: 'connectr5',
        sourceID: 'node5',
        targetID: 'node6',
        annotations: [{
            content: "Yes"
        }]
    }];
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
        backgroundColor: 'red'
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
        backgroundColor: 'blue'
    }
    

    ]
    
 
    return( 
    <DiagramComponent id="diagram" ref={diagram=>(diagramInstance=diagram)} width="100%" height={600} nodes={node} connectors={connector} selectedItems={{
        constraints: SelectorConstraints.UserHandle,
        userHandles: handles
    }} 
//Uses layout to auto-arrange nodes on the diagram page
layout={{
    //Sets layout type
    type: 'ComplexHierarchicalTree',
    orientation: 'TopToBottom'
}} 
//Sets the default properties for nodes and connectors
getNodeDefaults={(obj) => {
    obj.shape = {
        type: 'Text',
        style: {
            color: 'white'
        }
    };
    obj.style = {
        fill: '#d1cfcf',
        strokeColor: 'none',
        strokeWidth: 2
    };
    obj.borderColor = 'white';
    obj.backgroundColor = '#d1cfcf';
    obj.borderWidth = 1;
    obj.shape.margin = {
        left: 5,
        right: 5,
        top: 5,
        bottom: 5
    };
    return obj;
}} getConnectorDefaults={(connector, diagram) => {
    connector.style = {
        strokeColor: '#6BA5D7',
        strokeWidth: 2
    };
    connector.targetDecorator.style.fill = '#6BA5D7';
    connector.targetDecorator.style.strokeColor = '#6BA5D7';
    connector.type = 'Orthogonal';
    return connector;
}}
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
><Inject services={[ComplexHierarchicalTree, DataBinding]}/>
        </DiagramComponent>
        );
    }


}



export default DiagFlow;