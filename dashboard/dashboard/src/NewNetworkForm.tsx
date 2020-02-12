
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
        body: JSON.stringify(data)
        })
    return await response.json()
}

class Network  
{ name?: string |File |null
  layers?:Array<Layer>
}
export class NewNetwork extends React.Component {
      state: Network
      constructor(props:Network) {
        super(props);
        this.state = {  
            name: '', 
            layers:[]
        }
    }
    addNetworkHandler = (event:any) => {
        console.log(`POST:${JSON.stringify(this.state)}`) //State is alwyes empty
        postNetwork(this.state)
            .then((data) => {
                console.log(`Response:${JSON.stringify(data)}`)
            });
        
    }
    addLayerHandler = async (event:any) => {
        console.log(`${JSON.stringify(this.state)}`) //State is alwyes empty
        const data = new FormData(event.target)
             
        let layer:Layer = new Layer(Number(data.get('units')),
                            data.get('activation'),
                            data.get('input_shape'))
        await this.setState(
            { name: data.get('name'),
              layers:  [...this.state.layers, layer]  
            });
        
        console.log(`${JSON.stringify(this.state)}`)
      }
    render() {
      return (
            <div>
            <form  onSubmit={this.addLayerHandler}>
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
            <input type="submit" value="Add layer"/>
            </form>
            <button onClick ={this.addNetworkHandler}>Add new network</button> 
            </div>
        );
    }
  }