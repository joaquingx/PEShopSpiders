import * as React from 'react'
import "bulma/css/bulma.min.css"
import Sidebar from './components/Sidebar'
import ShowResult from './components/ShowResult'

export default function App(): JSX.Element {
    return (
        <div>
            <Sidebar/>
            <ShowResult/>
        </div>
    )
}
