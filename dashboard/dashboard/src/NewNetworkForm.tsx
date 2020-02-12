
import * as React from 'react';
import { newNetwrokEndPoint } from './Config';



class Layer {
    public units: number
    public activation: string |File |null
    public input_shape: string | File | null

    constructor(units: number,activation:string|File |null,input_shape:string|File|null=null) {
        this.units = units
        this.activation = activation
        this.input_shape = input_shape
    }
}
async function postNetwork(data:any) {
    const response = await fetch(newNetwrokEndPoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: data
        })
    return await response.json()
}

class Network  
{ name?: string |File |null
  layers?:Array<Layer>
}

export class NewNetwork extends React.Component {
      constructor(props:Network) {
        super(props);
  
    }
  
    addNetworkHandler = (event:any) => {
        console.log(`POST:${localStorage.globalState}`) 
        postNetwork(localStorage.globalState)
            .then((data) => {
                console.log(`Response:${JSON.stringify(data)}`)
            });
            localStorage.clear();  
        
    }

    addLayerHandler = async (event:any) => {
        const data = new FormData(event.target)
        let layer:Layer = new Layer(Number(data.get('units')),
                            data.get('activation'),
                            data.get('input_shape'))
        let network: Network|undefined = undefined                   
        
        if (typeof localStorage.globalState !== 'undefined') {                    
            network = 
                { name: data.get('name'),
                  layers: [... JSON.parse(localStorage.globalState).layers, layer]  
                }
        }
        else {
            network= 
                { name: data.get('name'),
                  layers: [layer]  
                }
        }
        localStorage.setItem("globalState", JSON.stringify(network));    

      }
    render() {
      return (
            <div>
                <form onSubmit={this.addLayerHandler}>
                    <p>Network name:</p>
                    <input
                    name = 'name'
                    type = 'text'
                // defaultValue={this.state.name}
                    />
                    <p>units:</p>
                    <input
                    name = 'units'
                    type = 'text'
                    />
                    <p>activation:</p>
                    <input
                    name = 'activation'
                    type ='text'
                    />
                    <p>input_shape:</p>
                    <input
                    name = 'input_shape'
                    type ='text'
                    />
                    <br></br>
                    <input type="submit" value="Add Layer"/>
                </form>
                <button onClick ={this.addNetworkHandler}>Add new network</button> 
            </div>
        );
    }
  }