import * as React from 'react';
import { networkDetailsEndPoint,dataSetsEndPoint,compileNetwrokEndPoint,trainNetwrokEndPoint } from './Config';

async function getNetworkDetails(networkName:string | undefined) {
    const response = await fetch(networkDetailsEndPoint + networkName, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'}
        })
    return await response.json()
}
async function getDataSets() {
    const response = await fetch(dataSetsEndPoint, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'}
        })
    return await response.json()
}

async function compileNetwork(data:any) {
    const response = await fetch(compileNetwrokEndPoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(data)
        })
    return await response.json()
}
async function trainNetwork(data:any) {
    const response = await fetch(trainNetwrokEndPoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(data)
        })
    return await response.json()
}

export interface ViewProperties {
    params: string
}
interface InetworkDetails {
    Name:string
    Compiled: boolean
    Trained: boolean
}
type State = { name:string, form:any };
export class NetworkDetails extends React.Component<ViewProperties,State> {

    constructor(props:ViewProperties) {
        super(props);
        this.state = {name: this.props.params, form: undefined} 
    }

    compileNetworkHandler = (event:any) => {
        const data = new FormData(event.target)
        compileNetwork(data)
            .then((response) => {
                console.log(`Response:${JSON.stringify(response)}`)
            });
    }
    trainNetworkHandler = (event:any) => {
        const data = new FormData(event.target)
        trainNetwork(data)
            .then((response) => {
                console.log(`Response:${JSON.stringify(response)}`)
            });
    }
    getDataSources() {
        var dat_sources: Array<string> = []
        getDataSets()
            .then((data) => {
                if(data.Dat_Sources !== ""){
                    console.log(`Response:${JSON.stringify(data.Dat_Sources)}`)
                    dat_sources = data.Dat_Sources
                }
            })
        return dat_sources
       }    
    createDataSources = () => {
        let data_sources:Array<JSX.Element> = []
        if ( this.getDataSources().length > 0) {
            this.getDataSources().forEach(function (value) {
                console.log(value) 
                data_sources.push(
                            <option value={value}>
                             {value}
                            </option>)
            })
        }
        return data_sources
      }
 
    compileForm() {
        return (
        <form onSubmit={this.compileNetworkHandler}>
                    Network name:&nbsp;&nbsp;
                        <input
                        readOnly
                        name = 'name'
                        type = 'text'
                        defaultValue = {this.state.name}
                        />
                    <br/>
                    optimizer:&nbsp;&nbsp;
                        <input
                        name = 'optimizer'
                        type = 'text'
                        />
                    <br/>
                    loss:&nbsp;&nbsp;
                        <input
                        name = 'loss'
                        type ='text'
                        />
                    <br/>
                    metrics:&nbsp;&nbsp;
                        <input
                        name = 'metrics'
                        type ='text'
                        />
                    <br/>
                    <input id="compile" type="submit" value="Compile network"/>
        </form>
        )
    }
    
    trainForm() {
        return (
        <form onSubmit={this.trainNetworkHandler}>
                    Network name:&nbsp;&nbsp;
                        <input
                        readOnly
                        name = 'name'
                        type = 'text'
                        defaultValue = {this.state.name}
                        />
                    <br/>
                    data_set:&nbsp;&nbsp;
                        <select
                        name = 'data_set'
                        >
                       {this.createDataSources()} 
                    </select>    
                    <br/>
                    epochs:&nbsp;&nbsp;
                        <input
                        name = 'epochs'
                        type ='text'
                        />
                    <br/>
                    batch_size:&nbsp;&nbsp;
                        <input
                        name = 'batch_size'
                        type ='text'
                        />
                    <br/>
                    input_shape:&nbsp;&nbsp;
                        <input
                        name = 'input_shape'
                        type ='text'
                        />
                    <br/>
                    test_sample_size:&nbsp;&nbsp;
                        <input
                        name = 'test_sample_size'
                        type ='text'
                        />
                    <br/>
                    <input id="train" type="submit" value="Train network"/>
        </form>
        )
    }
    getNetworkDetails =() =>{
        var networkDetails:InetworkDetails = {Name: "",Compiled: false,Trained: false }
        getNetworkDetails(this.state.name)
            .then((data) => {
                console.log(`Network details:${JSON.stringify(data)}`)
                networkDetails = data
            })
        return networkDetails
    } 
  getForm() {
        var details:InetworkDetails = this.getNetworkDetails()
        console.log(`Network details:${JSON.stringify(details)}`)
        if (details.Compiled !== true) { 
             return this.compileForm()
        }
        else {
           return this.trainForm()
        }
    }
    render() {
        return (
            <div>
                {this.getForm()}
            </div>
        )}
}
