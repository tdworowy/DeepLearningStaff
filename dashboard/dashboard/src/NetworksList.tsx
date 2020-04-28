import * as React from 'react';
import { networksEndPoint,deleteNetworkEndPoint } from './Config';
import { NetworkDetails } from './NetworkDetails';
import ReactDOM from 'react-dom';

async function getNetworks() {
    const response = await fetch(networksEndPoint, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'}
        })
    return await response.json()
}
async function deleteNetwork(name:string|File|null) {
    const response = await fetch(deleteNetworkEndPoint, {
        method: 'Delete',
        headers: { 'Content-Type': 'application/json'},
        body:JSON.stringify({'name':name})
        })
    return await response.json()
}
function deleteNetworkHandler(name:string) {
    return () => { 
        console.log(`Delete:${name}`) 
        deleteNetwork(name)
            .then((data) => {
                console.log(`Response:${JSON.stringify(data)}`)
            });
        }
}
interface networkData {
    name:string
    compiled:boolean
    trained:boolean
}
type State = { networks: Array<networkData> };
export class NetworksList extends React.Component<{},State> {
    timer:any 
    
    constructor(props:any) {
      super(props);
      this.state = { 
        networks: []
      }
    }
    componentDidMount(){
        this.timer = setInterval(()=>  getNetworks()
            .then((data) => {
                if(data.Networks !== ""){
                    console.log(`Response:${JSON.stringify(data.Networks)}`)
                    this.setState({networks:data.Networks})
                }
            }), 10000)
       }
       
    createNetworkList = () => {
        let networks:Array<JSX.Element> = []
        if ( this.state.networks.length > 0) {
            this.state.networks.forEach(function (value) {
                console.log(value)
                networks.push(<tr id={value.name}>
                                <td><label>{value.name}</label></td>
                                <td><button id = 'details' onClick={event => ReactDOM.render(<NetworkDetails params={value.name}/>, document.getElementById('root'))}>Details</button></td>
                                <td><button id = 'delete' onClick={deleteNetworkHandler(value.name)}>Delete</button></td>
                                <td id={String(value.compiled)}><label>{String(value.compiled)}</label></td>
                                <td id={String(value.trained)}><label>{String(value.trained)}</label></td>
                              </tr> )
            })
        }
        return networks
      }

    render() {
        return (
            <div>
                <table  title="Networks:">
                <tr>
                    <th>Network name</th>
                    <th>Details</th>
                    <th>Delete</th>
                    <th>Compiled</th>
                    <th>Trained</th>
                </tr>
                    {this.createNetworkList()}
                </table >
            </div>
        )}
}