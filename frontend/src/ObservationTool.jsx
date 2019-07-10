class ObservationTool{

    mouseDown(args,diagramInstance) {
        if(diagramInstance.selectedItems.connectors.length === 0){
            if (diagramInstance.selectedItems.nodes.length > 0 && diagramInstance.selectedItems.nodes[0].style.fill !== "#F45342"){
                for(var i in diagramInstance.selectedItems.nodes){
                    diagramInstance.selectedItems.nodes[i].style.fill = "#F45342";
                    diagramInstance.selectedItems.nodes[i].addInfo[0]['eventtype'] = "O";
                }
            args.source = diagramInstance.nodes[diagramInstance.nodes.length - 1];
            args.sourceWrapper = args.source.wrapper;
            this.inAction = true;
            }
            else{
                diagramInstance.selectedItems.nodes[0].style.fill = "#ffeec7";
                diagramInstance.selectedItems.nodes[0].addInfo[0]['eventtype'] = "N";

                args.source = diagramInstance.nodes[diagramInstance.nodes.length - 1];
                args.sourceWrapper = args.source.wrapper;
                this.inAction = true;
            }
        }
    }
}


export default ObservationTool;