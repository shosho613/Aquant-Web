import React from 'react';


class TextRep extends React.Component{
    constructor(props){
        super(props)
        this.file = props.file
        this.pagenum = props.pagenum
        this.state = {
            nodes: null,
            connectors: null
        }
    }




    render(){
        return(
            <div>
                <form>

                </form>
            </div>
        )
    }
}

export default TextRep;