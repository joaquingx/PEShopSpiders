import * as React from 'react'
import "bulma/css/bulma.min.css"
import Sidebar from './components/Sidebar'
import { ShowResult } from './components/ShowResult'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
} from "react-router-dom"

export default function App(): JSX.Element {
    return (
        <div>
            <Router>
                <Link to="/cluster">Cluster</Link>
                <Switch>
                    <Route path="/cluster">
                        <Sidebar/>
                        <ShowResult/>
                    </Route>
                </Switch>
            </Router>
        </div>
    )
}
