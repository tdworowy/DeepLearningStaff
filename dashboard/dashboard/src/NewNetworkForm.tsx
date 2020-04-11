import * as React from 'react';
import { newNetwrokEndPoint } from './Config';
import { Interface } from 'readline';

interface Layer {

}

class DenseLayer implements Layer{
    public layer: string
    public units: number
    public activation: string |File |null
    public input_shape: string | File | null

    constructor( units:number,activation:string|File|null,input_shape:string|File|null=null) {
        this.layer ="Dense"
        this.units = units
        this.activation = activation
        this.input_shape = input_shape
    }
}

class Conv2DLayer implements Layer{
    public layer: string
    public filters: number
    public kernel_size: string |File |null
    public activation: string | File | null
    public input_shape: string | File | null

    constructor( filters:number,kernel_size:string|File|null,activation:string|File|null,input_shape:string|File|null=null) {
        this.layer ="Conv2D"
        this.filters = filters
        this.kernel_size = kernel_size
        this.activation = activation
        this.input_shape = input_shape
    }
}

class MaxPooling2D implements Layer{
    public layer: string
    public pool_size: string |File |null
    public strides: number
    
    constructor( pool_size: string |File |null,strides:number) {
        this.layer ="MaxPooling2D"
        this.pool_size = pool_size
        this.strides = strides
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

class Network { 
   name?: string |File |null
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

    addDenseLayerHandler = async (event:any) => {
        const data = new FormData(event.target)
        let layer:DenseLayer = new DenseLayer(
                            Number(data.get('units')),
                            data.get('activation'),
                            data.get('input_shape'))
        
        this.addLayerHandler(data.get('name'),layer)

    }
    addConv2DLayerHandler = async (event:any) => {
        const data = new FormData(event.target)
        let layer:Conv2DLayer = new Conv2DLayer(
                            Number(data.get('filters')),
                            data.get('kernel_size'),
                            data.get('activation'),
                            data.get('input_shape'))
        
        this.addLayerHandler(data.get('name'),layer)

    }
    addMaxPooling2DLayerHandler = async (event:any) => {
        const data = new FormData(event.target)
        let layer:MaxPooling2D = new MaxPooling2D(
                            data.get('pool_size'),
                            Number(data.get('strides')))
        
        this.addLayerHandler(data.get('name'),layer)

    }

    addLayerHandler = (name:string |File |null,layer:Layer) => {
        
        let network: Network|undefined = undefined                   
        
        if (typeof localStorage.globalState !== 'undefined') {                    
            network = 
                { name: name,
                  layers: [... JSON.parse(localStorage.globalState).layers, layer]  
                }
        }
        else {
            network= 
                { name: name,
                  layers: [layer]  
                }
        }
        localStorage.setItem("globalState", JSON.stringify(network));
        localStorage.setItem("layerName", "undefined");    
      }    

    chooseLayerHandler = (event:any) => {
        const data:any = new FormData(event.target)
        localStorage.setItem("layerName", data.get('layer')) 

    }
    layerTypeForm = () => {
        return (
            <form onSubmit={this.chooseLayerHandler}>
            <div className="row">
            <div className="col-25">
            <label htmlFor ="Layer">Layer:</label>
            </div>
            <div className="col-75">
                    <select
                    name = 'layer'
                    >
                    <option value ='Dense'>Dense</option>
                    <option value ='Conv1D'>Conv1D</option>
                    <option value ='Conv2D'>Conv2D</option>
                    <option value ='SeparableConv1D'>SeparableConv1D</option>
                    <option value ='SeparableConv2D'>SeparableConv2D</option>
                    <option value ='SimpleRNN'>SimpleRNN</option>
                    <option value ='GRU'>GRU</option>
                    <option value ='LSTM'>LSTM</option> 
                    <option value ='MaxPooling1D'>MaxPooling1D</option>
                    <option value ='MaxPooling2D'>MaxPooling2D</option>
                    <option value ='AveragePooling1D'>AveragePooling1D</option>
                    <option value ='AveragePooling2D'>AveragePooling2D</option>
                    <option value ='GlobalMaxPooling1D'>GlobalMaxPooling1D</option>
                    <option value ='GlobalMaxPooling2D'>GlobalMaxPooling2D</option>
                    <option value ='Embedding'>Embedding</option>
                    <option value ='Dropout'>Dropout</option>
                    <option value ='Flatten'>Flatten</option>
                    </select>
           </div>
           </div>
           <input id="choose_layer" type="submit" value="Choose Layer"/>
           </form> 
        )
    }
    
    newDenseLayerForm  = ()  => {
       return (
            <form onSubmit={this.addDenseLayerHandler}>
            <div className="row">
            <div className="col-25">
            <label htmlFor ="name">Network name:</label>
            </div> 
            <div className="col-75">
                    <input
                    name = 'name'
                    type = 'text'
                    defaultValue = {this.getNetworkName()}
                    />
            </div>
            </div>
            <div className="row">
            <div className="col-25">
            <label htmlFor ="units">Units:</label>
            </div> 
            <div className="col-75">
                    <input
                    name = 'units'
                    type = 'text'
                    />
            </div>
            </div>
            <div className="row">
            <div className="col-25">
            <label htmlFor ="activation">Activation:</label>
            </div>
            <div className="col-75">
                    <select
                    name = 'activation'
                    >
                    <option value ='relu'>relu</option>
                    <option value ='softmax'>softmax</option>
                    <option value ='selu'>selu</option>
                    <option value ='softsign'>softsign</option>
                    <option value ='tanh'>tanh</option>
                    <option value ='sigmoid'>sigmoid</option>
                    <option value ='hard_sigmoid'>hard_sigmoid</option>
                    <option value ='exponential'>exponential</option>
                    <option value ='linear'>linear</option>
                    </select>
           </div>
           </div> 
           <div className="row">
           <div className="col-25"> 
           <label htmlFor ="input_shape">Input_shape:</label>
           </div> 
           <div className="col-75">
                    <input
                    name = 'input_shape'
                    type ='text'
                    />
            </div>
            </div>      
                <input id="add_layer" type="submit" value="Add Layer"/>
            </form>
        )
    }
    newConv2DLayerForm  = ()  => {
        return (
             <form onSubmit={this.addConv2DLayerHandler}>
             <div className="row">
             <div className="col-25">
             <label htmlFor ="name">Network name:</label>
             </div> 
             <div className="col-75">
                     <input
                     name = 'name'
                     type = 'text'
                     defaultValue = {this.getNetworkName()}
                     />
             </div>
             </div>
             <div className="row">
             <div className="col-25">
             <label htmlFor ="filters">filters:</label>
             </div> 
             <div className="col-75">
                     <input
                     name = 'filters'
                     type = 'text'
                     />
             </div>
             </div>
             <div className="row">
             <div className="col-25">
             <label htmlFor ="kernel_size">kernel_size:</label>
             </div> 
             <div className="col-75">
                     <input
                     name = 'kernel_size'
                     type = 'text'
                     />
             </div>
             </div>
             <div className="row">
             <div className="col-25">
             <label htmlFor ="activation">Activation:</label>
             </div>
             <div className="col-75">
                     <select
                     name = 'activation'
                     >
                     <option value ='relu'>relu</option>
                     <option value ='softmax'>softmax</option>
                     <option value ='selu'>selu</option>
                     <option value ='softsign'>softsign</option>
                     <option value ='tanh'>tanh</option>
                     <option value ='sigmoid'>sigmoid</option>
                     <option value ='hard_sigmoid'>hard_sigmoid</option>
                     <option value ='exponential'>exponential</option>
                     <option value ='linear'>linear</option>
                     </select>
            </div>
            </div> 
            <div className="row">
            <div className="col-25"> 
            <label htmlFor ="input_shape">Input_shape:</label>
            </div> 
            <div className="col-75">
                     <input
                     name = 'input_shape'
                     type ='text'
                     />
             </div>
             </div>      
                 <input id="add_layer" type="submit" value="Add Layer"/>
             </form>
         )
     } 
     newMaxPooling2DLayerForm  = ()  => {
        return (
             <form onSubmit={this.addMaxPooling2DLayerHandler}>
             <div className="row">
             <div className="col-25">
             <label htmlFor ="name">Network name:</label>
             </div> 
             <div className="col-75">
                     <input
                     name = 'name'
                     type = 'text'
                     defaultValue = {this.getNetworkName()}
                     />
             </div>
             </div>
             <div className="row">
             <div className="col-25">
             <label htmlFor ="pool_size">pool_size:</label>
             </div> 
             <div className="col-75">
                     <input
                     name = 'pool_size'
                     type = 'text'
                     />
             </div>
             </div>
             <div className="row">
             <div className="col-25">
             <label htmlFor ="strides">strides:</label>
             </div> 
             <div className="col-75">
                     <input
                     name = 'strides'
                     type = 'text'
                     />
             </div>
             </div>
                <input id="add_layer" type="submit" value="Add Layer"/>
             </form>
         )
     } 
     chooseFrom(){ //TODO get ride off if else
        if (typeof localStorage.layerName === 'undefined' || localStorage.layerName ===  'undefined') {  
            return this.layerTypeForm()
        }
        else if (localStorage.layerName === 'Dense') {  
            return this.newDenseLayerForm()
        }
        else if (localStorage.layerName === 'Conv2D') {  
            return this.newConv2DLayerForm()
        }
        else if (localStorage.layerName === 'MaxPooling2D') {  
            return this.newMaxPooling2DLayerForm()
        }
     }
     render() {
        return(
            <div className="container">
                {this.chooseFrom()}
                <br/>
                <button id = "add_network_button" onClick ={this.addNetworkHandler}>Add new network</button>
                <button id = "clear_network_button" onClick ={this.clearNetworkHandler}>Clear network</button>
                <br/><br/>
                <textarea id = "new_layer_details" rows={4} cols={50} value={this.getTempNetworkDetails()}></textarea>
            </div>
        )
  } 
}