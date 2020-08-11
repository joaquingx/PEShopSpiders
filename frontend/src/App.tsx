import * as React from 'react'
import "bulma/css/bulma.min.css"
import Sidebar from './components/Sidebar'
import { ShowResult } from './components/ShowResult'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    useLocation,
} from "react-router-dom"

export default function App(): JSX.Element {
    // const query = useQuery();
    return (
        <div>
            <Router>
                <Link to="/cluster">Cluster</Link>
                <Switch>
                    <Route path="/cluster">
                        <Sidebar/>
                        <ShowResult name="adilette" threshold="0.5"/>
                    </Route>
                </Switch>
            </Router>
        </div>
    )
}
