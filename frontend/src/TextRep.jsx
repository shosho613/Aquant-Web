import React from 'react';

/**expiremntal component for an alternative view of the data */
class TextRep extends React.Component{
    constructor(props){
        super(props)
        this.file = props.file
        this.pagenum = props.pagenum
        this.state = {
            nodes: null,
            connectors: null
        }
        this.getGraphRep = this.getGraphRep.bind(this);

    }

    componentDidMount(){
        this.getGraphRep()

    }

    getGraphRep(){
        var data = new FormData()
        data.append('pagenum', this.pagenum)
        data.append('file', this.file)
        fetch('http://localhost:5000/GetRawGraph', {
        method: 'POST',
        body: data,
       /* headers:{
          "Access-Control-Allow-Origin" : "*", 
          "Access-Control-Allow-Credentials" : true,
        }*/
      }).then(response => response.json())
      .then(response => {
        console.log(response)
  
      }
      )
    }

    convertNodes = (array) => {
        var nodes = new Map()
        for(var i in array){
            nodes.set(
                String(array[i]["Name"]), array[i]
            )
        }
        return nodes
    }




    render(){
        const nodes = this.state.nodes;
        const connectors = this.state.connectors;

        const items = []

        /*if(nodes != null){
            for (const [nIndex, nValue] of nodes.entries()) {
                items.push(
                    <div class="card row" key={nIndex}>
                    <div class="card-body">
                        <p className="card-text">{String(nValue['Content'])}</p>
                        <button>Make Observation</button>
                        <button>Make Solution</button>
                    </div>
                    </div>
                )
                for(const [cIndex, cValue] of connectors.entries()){
                    if( cValue['sourceID'] === nValue['Name']){
                        console.log(nodes.get(cValue['targetID']))
                        items.push(
                            <div class="card col" >
                            <div class="card-body">
                                <p className="card-text">{"Connected To" + String(nodes.get(cValue['targetID'])['Content'])}</p>
                                <button>Make Observation</button>
                                <button>Make Solution</button>
                            </div>
                            </div>
                        )
                    }
                
                }
            }
        }*/

        return (
            <div className="col">
            {items}
            </div>
        )
            }
    }

export default TextRep;