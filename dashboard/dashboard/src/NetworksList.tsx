
import * as React from 'react';
import { networksEndPoint } from './Config';


async function getNetworks() {
    const response = await fetch(networksEndPoint, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'}
        })
    return await response.json()
}

type State = { networks: Array<string> };
export class NetworksList extends React.Component<{},State> {
    constructor(props:any) {
      super(props);
      this.state = { 
        networks: []
      }
    }
 
    createNetworkList = () => {
        let networks:Array<JSX.Element> = []

        getNetworks()
        .then((data) => {
            console.log(`Response:${data.Networks}`);
            this.setState({networks:data.Networks})
        });
    
        this.state.networks.forEach(function (value) {
            console.log(value) 
            networks.push(<a href={`http://${value}`}>value</a>)
        })
        return networks
      }

    render() {
        return (
            <div>
            {this.createNetworkList()}
            </div>
        )}
}