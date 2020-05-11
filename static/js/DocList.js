// define class
class DocList extends React.Component {
    constructor(props){
        super(props);
        this.state = {list: true, depth:-1};
        this.items = [];
        this.handleClick = this.handleClick.bind(this);
        this.curr_items = [];
    }
    
    // switch between article and list
    handleClick(item){
        if (item.path != "back"){
            this.curr_items.push(item);
            this.state.depth += 1;
            this.state.list = false;
        }
        else{
            this.curr_items.pop();
            this.state.depth -= 1;
            if (this.state.depth != -1){
                this.state.list = false;
            }
            else{
                this.state.list = true;
            }
        }
        ReactDOM.render(
            <DocList></DocList>,
            document.getElementById('list')
        );
    }
    
    // load the document
    display_document(){
        const list = [];
        list.push(
            <div id = {"display_doc"}>
                <embed src={this.curr_items[this.state.depth].path} width="100%" height="650px" />
                <div><button class ="back_button" onClick = {()=> this.handleClick({path: "back"})}><p>Back</p></button></div>
            </div>
        );
        for (let item of this.curr_items[this.state.depth].docs) {
        list.push(
            <div id = {item.id}>
                <div class = "doc" onClick = {() => this.handleClick(item)}>
                <div><h3>{item.title}</h3></div>
                <div>{item.summery}</div>
                <div><u>(Click to view the full article)</u></div>
                </div>
                <div class = "split"><hr /></div>
            </div>
        );
        }
        return (<div>{list}</div>);
    }
    
    // get json file from backend
    dfs(item){
        this.items.push(item);
        if (item.docs.length == 0){
            return undefined;
        }
        for (let sub_item of item.docs){
            this.dfs(sub_item);
        }
    }
    fetch_list(){
        this.items = [];
        let curr_list = [data.documentations, data.reports, data.blogs];
        for (let list of curr_list){
            for (let item of list){
                this.dfs(item);
            }
        }
    }
    
    // load the list
    generate_list(){
        this.fetch_list(); // get the data of list (json)

        // push to the list tag
        const list = [];
        for (let item of this.items) {
        list.push(
            <div id = {item.id}>
                <div class = "doc" onClick = {() => this.handleClick(item)}>
                <div><h3>{item.title}</h3></div>
                <div>{item.summery}</div>
                <div><u>(Click to view the full article)</u></div>
                </div>
                <div class = "split"><hr /></div>
            </div>
        );
        }
        return (<div>{list}</div>);
    }
    
    render () {
        if (this.state.list){
            return this.generate_list();
        }
        else{
            return this.display_document();
        }
    }
}

// Apply
ReactDOM.render(
    <DocList></DocList>,
    document.getElementById('list')
);