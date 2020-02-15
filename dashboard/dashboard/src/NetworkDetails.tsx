import * as React from 'react';
import { networkDetails,dataSets } from './Config';

export class NetworkDetailsProps {
    name?:string
}

async function getNetworkDetails(networkName:string | undefined) {
    const response = await fetch(networkDetails + networkName, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'}
        })
    return await response.json()
}
async function getDataSets() {
    const response = await fetch(dataSets, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'}
        })
    return await response.json()
}

type State = { name: string | undefined };
export class NetworkDetails extends React.Component<NetworkDetailsProps,State> {

    constructor(props:NetworkDetailsProps) {
        super(props);
        this.state = {name: props.name} 
    
    }

    compileNetworkHandler = () => {

    }
    trainNetworkHandler= () => {

    }
    getDataSources() {
        var dat_sources: Array<string> = []
        getDataSets()
            .then((data) => {
                if(data.Dat_Sources != ""){
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
                    <input id="compile" type="submit" value="Compile network"/>
        </form>
        )
    }
    getForm() {
        let form: any
        getNetworkDetails(this.state.name)
        .then((data) => { 
            if (!data.Compiled) { 
                form = this.compileForm()
            }
            else {
                form = this.trainForm()
            }
        })
        return form
    }
    render() {
        return (
            <div>
                {this.getForm()}
            </div>
        )}
}