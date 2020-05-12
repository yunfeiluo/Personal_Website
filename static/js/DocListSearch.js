class DocListSearch extends React.Component {
    constructor(props){
        super(props);
        this.state = {list: true, depth:-1};
        this.items = this.get_method(".", doc_type, " ");
        this.handleClick = this.handleClick.bind(this);
        this.curr_items = [];
    }
    
    // helper functions
    // get json file from backend
    dfs(item, res){
        res.push(item);
        if (item.docs.length == 0){
            return undefined;
        }
        for (let sub_item of item.docs){
            this.dfs(sub_item, res);
        }
    }

    get_method(url, doc_type, queries){
        if (doc_type == "documentations"){
            return data.documentations;
        }
        if (doc_type == "blogs"){
            return data.blogs;
        }
        if (doc_type == "reports"){
            return data.reports;
        }   
        
        let res = [];
        let curr_list = [data.documentations, data.reports, data.blogs];
        
        for (let list of curr_list){
            for (let item of list){
                this.dfs(item, res);
            }
        }
        return res;
    }
    
    // handling events
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
            <DocListSearch></DocListSearch>,
            document.getElementById('list')
        );
    }

    handle_search(){
        let query_term = document.getElementById("search_text").value;
        if (query_term == "blogs"){
            this.items = this.get_method(".", "blogs", query_term);
        }
        else{
            this.items = this.get_method(".", "all", query_term);
        }
        ReactDOM.render(
            <DocListSearch></DocListSearch>,
            document.getElementById('list')
        );
        return false;
    }
    
    // rendor stuff
    // load the document
    display_document(){
        const list = [];
        list.push(
            <div id = {"display_doc"}>
                <embed src={this.curr_items[this.state.depth].path} width="100%" height="650px" />
            </div>
        );
        for (let item of this.curr_items[this.state.depth].docs) {
        list.push(
            <div id = {item.id}>
                <div className = "doc" onClick = {() => this.handleClick(item)}>
                <div><h3>{item.title}</h3></div>
                <div>{item.summery}</div>
                <div><u>(Click to view the full article)</u></div>
                </div>
                <div className = "split"><hr /></div>
            </div>
        );
        }
        list.push(<div><button className ="back_button" onClick = {()=> this.handleClick({path: "back"})}><p>Back</p></button></div>);
        return (<div>{list}</div>);
    }
    
    // load the list
    generate_list(){
        // push to the list tag
        const list = [];
        list.push(
            <div>
            <form onSubmit={() => this.handle_search()} target="curr_iframe">
                <div>
                <input id = "search" type="text" />      
                <input type="button" value="Submit" onClick={() => this.handle_search()}/>
                </div>
            </form>
            <iframe id="curr" name="curr_iframe" style={{display: "none"}}></iframe>
            </div>
        );
        for (let item of this.items) {
        list.push(
            <div id = {item.id}>
                <div className = "doc" onClick = {() => this.handleClick(item)}>
                <div><h3>{item.title}</h3></div>
                <div>{item.summery}</div>
                <div><u>(Click to view the full article)</u></div>
                </div>
                <div className = "split"><hr /></div>
            </div>
        );
        }
        return (<div>{list}</div>);
    }
    
    // rendor funcion
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
    <DocListSearch></DocListSearch>,
    document.getElementById('list')
);