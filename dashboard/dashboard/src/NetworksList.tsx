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
type State = { networks: Array<string> };
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
                networks.push(<li id={value}>
                                <label>{value}&nbsp;&nbsp;</label>
                                <button id='details' onClick={event => ReactDOM.render(<NetworkDetails params={value}/>, document.getElementById('root'))}>Details</button>
                                <button id='delete' onClick={deleteNetworkHandler(value)}>Delete</button>
                              </li> )
            })
        }
        return networks
      }

    render() {
        return (
            <div>
                <ul>
                    {this.createNetworkList()}
                </ul>
            </div>
        )}
}