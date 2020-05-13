class DocListSearch extends React.Component {
    constructor(props){
        super(props);
        this.state = {list: true, depth:-1};
        //this.items = this.get_method(".", doc_type, " ");
        this.items = docs_list;
        this.handleClick = this.handleClick.bind(this);
        this.curr_items = [];
        this.search_attempted = 0;
    }
    
    // helper functions
    // get json file from backend
    get_method(url, queries){
        alert(queries);
        return docs_list;
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
        this.search_attempted += 1;
        let query_term = document.getElementById("search_text").value;
        // send request to backend, get json file back
        this.items = this.get_method(".", query_term);
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
            <div id="search_bar">
            <form onSubmit={() => this.handle_search()} target="curr_iframe">
                <div>
                <input id="search_text" type="text" placeholder="search for documents"/>      
                <input id="search_button" type="button" value="Search" onClick={() => this.handle_search()}/>
                </div>
            </form>
            <iframe id="curr" name="curr_iframe" style={{display: "none"}}></iframe>
            </div>
        );
        if (this.search_attempted > 0){
            list.push(
                <div id="result_bar">
                    <p>Search Results: (attempted: {this.search_attempted})</p>
                </div>
            );
        }
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