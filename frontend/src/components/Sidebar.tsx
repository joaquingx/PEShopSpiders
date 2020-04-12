import * as React from 'react'
import 'font-awesome/css/font-awesome.min.css'
import './Sidebar.css'

export default function Sidebar(): JSX.Element{
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
                        <span className="link-text">Search</span>
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
