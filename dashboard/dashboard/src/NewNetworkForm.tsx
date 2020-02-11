
import * as React from 'react';
import { newNetwrokEndPoint } from './Config';

class Layer {
    public units: number
    public activation: string
    public input_shape: string | null

    constructor(units: number,activation:string,input_shape:string|null=null) {
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

type State = { name: string, layers:Array<any>};
export class NewNetwork extends React.Component<{},State> {
    constructor(props:any) {
      super(props);
      this.addLayerHandler = this.addLayerHandler.bind(this);
      this.addNetworkHandler = this.addNetworkHandler.bind(this);
      this.state = { 
          name: '', 
          layers:[]
        }
    }
    addNetworkHandler = (event:any) => {
        console.log(`POST:${this.state}`);
        postNetwork(this.state)
            .then((data) => {
                console.log(`Response:${data}`);
            });
        
    }
    addLayerHandler = (event:any) => {
        console.log(`Add layer:${event.target}`);
        let layer:Layer = new Layer(event.target.units,
                          event.target.activation,
                          event.target.input_shape)
        this.setState(
            { name: event.target.name,
              layers:  [...this.state.layers, layer]  
            });
      }
    render() {
      return (
            <div>
            <form>
            <p>Network name:</p>
            <input
            name = 'name'
            type = 'text'
            defaultValue={this.state.name}
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
            <input type="submit" value="Add layer" onChange={this.addLayerHandler}/>
            </form>
            <button onClick ={this.addNetworkHandler}>Add new network</button> 
            </div>
        );
    }
  }