import * as React from 'react';
import { networksEndPoint } from './Config';
import { NetworkDetails } from './NetworkDetails';

async function getNetworks() {
    const response = await fetch(networksEndPoint, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'}
        })
    return await response.json()
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
                if(data.Networks != ""){
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
                networks.push(<li>
                                {value}&nbsp;&nbsp;
                                <button onClick={event =>  window.location.href=`/networkDetails#${value}`}>Details</button>
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