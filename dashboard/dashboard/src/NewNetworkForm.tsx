
import * as React from 'react';

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

type State = { name: string, layers:Array<any>};
export class NewNetwork extends React.Component<{},State> {
    constructor(props:any) {
      super(props);
      this.state = { 
          name: '', 
          layers:[]
        }
    }
    addNetworkHandler = (event:any) => {
      "pass"
    }
    addLayerHandler = (event:any) => {
        let layer:Layer = new Layer(event.target.units,
                          event.target.activation,
                          event.target.input_shape)
        this.setState(
            {name: event.target.name,
            layers:  [...this.state.layers, layer]  
            });
      }
    render() {
      return (
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
        <input type="submit" value="Add network"  onSubmit={this.addNetworkHandler}/>
        <input type="submit" value="Add layer"  onSubmit={this.addLayerHandler}/>
        </form>
        
      );
    }
  }