import * as React from 'react'
import {ChangeEvent, useState} from 'react';
import 'font-awesome/css/font-awesome.min.css'
import './Sidebar.css'
import { useHistory } from "react-router-dom";
// import "bootstrap/dist/css/bootstrap.min.css"

export default function Sidebar(): JSX.Element{
    const [searchValue, setSearchValue] = useState("");
    const history = useHistory();
    const changeSearchValue = (event: ChangeEvent<HTMLInputElement>) => {
        console.log(event.target.value);
    }
    return (
        <nav className="navbar">
            <ul className="navbar-nav">
                <li className="logo">
                    <a href="#" className="nav-link">
                        <span className="link-text">Liran</span>
                        <i className="fa fa-size fa-barcode"/>
                    </a>
                </li>
                <li className="nav-item">
                    <a href="#" className="nav-link">
                        <i className="fa fa-size fa-search"/>
                        <input className="link-text search-input"
                               onChange={(e) => setSearchValue(e.target.value) }
                               onKeyPress={(e) => {
                                   if(e.key == "Enter"){
                                        history.push(`/cluster?name=${searchValue}&threshold=0.7`)
                                   }
                               }}>

                        </input>
                    </a>
                </li>
                <li className="nav-item">
                    <a href="#" className="nav-link">
                        <i className="fa fa-fire fa-size"/>
                        <span className="link-text">Hot</span>
                    </a>
                </li>
                <li className="nav-item">
                    <a href="#" className="nav-link">
                        <i className="fa fa-android fa-size"/>
                        <span className="link-text">Tech</span>
                    </a>
                </li>
                <li className="nav-item">
                    <a href="#" className="nav-link">
                        <i className="fa fa-sign-out fa-size exit-icon"/>
                        <span className="link-text">Exit</span>
                    </a>
                </li>
            </ul>
        </nav>
    )
}
