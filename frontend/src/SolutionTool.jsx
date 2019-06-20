class SolutionTool{

    mouseDown(args,diagramInstance) {
        if(diagramInstance.selectedItems.connectors.length === 0){
            if (diagramInstance.selectedItems.nodes.length > 0 && diagramInstance.selectedItems.nodes[0].backgroundColor !== "#F45342"){
                diagramInstance.selectedItems.nodes[0].backgroundColor = "#3583ba";
            args.source = diagramInstance.nodes[diagramInstance.nodes.length - 1];
            args.sourceWrapper = args.source.wrapper;
            this.inAction = true;
            }
            else{
                diagramInstance.selectedItems.nodes[0].backgroundColor = "#d1cfcf";
                args.source = diagramInstance.nodes[diagramInstance.nodes.length - 1];
                args.sourceWrapper = args.source.wrapper;
                this.inAction = true;
            }
        }
    }
}


export default SolutionTool;