import React, { Component } from 'react';
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.min"
import './header.css'

export default class Search extends Component{

    constructor(props) {
        super(props);
        this.state = {
            search_value: null,
        };
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange({ target }){
        console.log(target.name);
        this.setState({
            search_value: target.value
        });
    }

    render(){
        return(
            <form className="align-right">
                <div className="form-group row">
                    <div className="col-md-8">
                        <input className="form-control"
                               name="search-value"
                               value={this.state.search_value}
                               placeholder="e.g. Leche"
                               onChange={this.handleChange}/>
                    </div>
                    <button type="button" value={this.state.search_value} className="mt-3 mt-md-0 btn btn-primary col-md-4" onClick={this.props.handler}>Buscar</button>
                </div>
            </form>
        )

    }
};
