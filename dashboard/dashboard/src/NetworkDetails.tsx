import * as React from 'react';
import { networkDetailsEndPoint,dataSetsEndPoint,compileNetwrokEndPoint,trainNetwrokEndPoint } from './Config';
import { SyncRequestClient } from 'ts-sync-request/dist'

class CompileNetworkData {
    name: string|File|null
    optimizer: string|File|null
    loss: string|File|null
    metrics: Array<String|File|null>

    constructor(name:string|File|null,optimizer:string|File|null,loss:string|File|null,metrics:Array<string|File|null>) {
        this.name = name
        this.optimizer = optimizer
        this.loss = loss
        this.metrics = metrics
    }

}

const sleep = (milliseconds:number) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))}

function getNetworkDetailsSync(networkName:string | undefined) {
     return new SyncRequestClient()
            .addHeader("Content-Type", "application/json")
            .get<Response>(networkDetailsEndPoint + networkName)
   
}
function getDataSetsSync() {
    return new SyncRequestClient()
        .addHeader("Content-Type", "application/json")
        .get<Response>(dataSetsEndPoint)
}

async function compileNetwork(data:any) {
    const response = await fetch(compileNetwrokEndPoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: data
        })
    return await response.json()
}
async function trainNetwork(data:any) {
    const response = await fetch(trainNetwrokEndPoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: data
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
        const compileNetworkData = new CompileNetworkData(
            data.get("name"),
            data.get("optimizer"),
            data.get("loss"),
            [data.get("metrics")]
        )
        const json = JSON.stringify(compileNetworkData)
        console.log(`POST:${json}`) 
        compileNetwork(json)
            .then((response) => {
                console.log(`Response:${JSON.stringify(response)}`)
            });
    }
    trainNetworkHandler = (event:any) => {
        const data = new FormData(event.target)
        const json = JSON.stringify(Object.fromEntries(data))
        console.log(`POST:${json}`)
        trainNetwork(json)
            .then((response) => {
                console.log(`Response:${JSON.stringify(response)}`)
            });
    }
    getDataSources() {
        var dat_sources: Array<string> = []
        var data:any = getDataSetsSync()
        if(data.Dat_Sources !== "") {
               console.log(`Response:${JSON.stringify(data)}`)
               dat_sources = data.Dat_Sources
            }
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
                        type ='number'
                        />
                    <br/>
                    batch_size:&nbsp;&nbsp;
                        <input
                        name = 'batch_size'
                        type ='number'
                        />
                    <br/>
                    input_shape:&nbsp;&nbsp;
                        <input
                        name = 'input_shape'
                        type ='number'
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

    getNetworkDetails() {
       return getNetworkDetailsSync(this.state.name)
    } 
    getForm():any {
        var details:any = this.getNetworkDetails()
        console.log(`Network details in getFrom:${JSON.stringify(details)}`)
        if (details.Compiled === false) {
             return this.compileForm()
        }
        if (details.Trained === false) {
           return this.trainForm()
        }
        else {
            return ("Add training chart")
        }

    }
    render() {
        return (
            <div>
                {this.getForm()}
            </div>
        )}
}
