class SolutionTool{

    mouseDown(args,diagramInstance) {
        if(diagramInstance.selectedItems.connectors.length === 0){
            if (diagramInstance.selectedItems.nodes.length > 0 && diagramInstance.selectedItems.nodes[0].style.fill !== "#3583ba"){
                diagramInstance.selectedItems.nodes[0].style.fill = "#3583ba";
                diagramInstance.selectedItems.nodes[0].data['eventtype'] = "Solution";
            args.source = diagramInstance.nodes[diagramInstance.nodes.length - 1];
            args.sourceWrapper = args.source.wrapper;
            this.inAction = true;
            }
            else{
                diagramInstance.selectedItems.nodes[0].style.fill = "#ffeec7";
                diagramInstance.selectedItems.nodes[0].data['eventtype'] = "Disregard";

                args.source = diagramInstance.nodes[diagramInstance.nodes.length - 1];
                args.sourceWrapper = args.source.wrapper;
                this.inAction = true;
            }
        }
    }
}


export default SolutionTool;