import * as React from 'react';
import { newNetwrokEndPoint } from './Config';

class Layer {
    public units: number
    public activation: string |File |null
    public input_shape: string | File | null

    constructor(units:number,activation:string|File|null,input_shape:string|File|null=null) {
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
            this.clearNetworkHandler(undefined)  
    }
    clearNetworkHandler = (event:any) => {
        localStorage.clear();
        const textArea: HTMLInputElement | null = document.getElementById("new_layer_details") as  HTMLInputElement
        if(!!textArea){
            textArea.value = ""
        }
    }
    getNetworkName = () => {
        if (typeof localStorage.globalState !== 'undefined') {   
            return  JSON.parse(localStorage.globalState).name
        }
        else return ""     
    }
    getTempNetworkDetails = () => {
        if (typeof localStorage.globalState !== 'undefined') {   
            return localStorage.globalState
        }
        else return ""     
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
                    Network name:&nbsp;&nbsp;
                        <input
                        name = 'name'
                        type = 'text'
                        defaultValue = {this.getNetworkName()}
                        />
                    <br/>
                    units:&nbsp;&nbsp;
                        <input
                        name = 'units'
                        type = 'text'
                        />
                    <br/>
                    activation:&nbsp;&nbsp;
                        <input
                        name = 'activation'
                        type ='text'
                        />
                    <br/>
                    input_shape:&nbsp;&nbsp;
                        <input
                        name = 'input_shape'
                        type ='text'
                        />
                    <br/>
                    <input id="add_layer" type="submit" value="Add Layer"/>
                </form>
                <button id ="add_netwrok_button" onClick ={this.addNetworkHandler}>Add new network</button>
                <button id="clear_network_button" onClick ={this.clearNetworkHandler}>Clear network</button>
                <br/>
                <textarea id="new_layer_details" rows={4} cols={50} value={this.getTempNetworkDetails()}></textarea>
            </div>
        );
    }
  }